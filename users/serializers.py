from dj_rest_auth.registration.serializers import RegisterSerializer
from django.conf import settings
from django_countries.serializer_fields import CountryField
from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import gettext as _
from rest_framework.validators import UniqueValidator
from phonenumber_field.serializerfields import PhoneNumberField

from .models import (
    PhoneNumber, 
    Profile,
    Address
    
    )


from .exceptions import (
    InvalidCredentialsException,
    AccountDisabledException,
    AccountNotRegisteredException,
    
    )



User = get_user_model()


class UserRegistrationSerializer(RegisterSerializer):
    """
    Serializer for registrating new users using email or phone number.
    """
    
    username = None
    first_name = serializers.CharField(required=True, write_only=True)
    last_name = serializers.CharField(required=True, write_only=True)
    phone_number = PhoneNumberField(
        required = False,
        write_only=True,
        validators=[
            UniqueValidator(
                queryset=PhoneNumber.objects.all(),
                message=_("A user is already registered with this phone number.")
            )
        ]
    )
    email = serializers.EmailField(required=False)
    
    def validate(self, validated_data):
        email = validated_data.get('email', None)
        phone_number = validated_data.get("phone_number", None)
        
        if not (email or phone_number):
            raise serializers.ValidationError(_("Enter an email or a phone number."))
        
        if validated_data["password1"] != validated_data["password2"]:
            raise serializers.ValidationError(_("The two password fields didn't match."))
        
        return validated_data
    
    
    def get_cleaned_data_extra(self):
        """
        Returns a dictionary of extra cleaned data.
        """
        return {
            "phone_number": self.validated_data.get("phone_number", ""),
            "first_name": self.validated_data.get("first_name", ""),
            "last_name": self.validated_data.get("last_name", ""),
        }
        
    def create_extra(self, user, validated_data):
        user.first_name = validated_data.get("first_name")
        user.last_name = validated_data.get("last_name")
        user.save()
        
        phone_number = validated_data.get("phone_number")
        
        if phone_number:
            PhoneNumber.objects.create(user=user, phone_number=phone_number)
            user.save()
            
    def custom_signup(self, request, user):
        self.create_extra(user, self.get_cleaned_data_extra())
        


class UserLoginSerializer(serializers.Serializer):
    """
    Serializer to login users with email or phone number
    """    
    
    phone_number = PhoneNumberField(required=False, allow_blank=True)
    email = serializers.EmailField(required=False, allow_blank=True)
    password = serializers.CharField(write_only=True, style={"input_type":"password"})
    
    
    def _validate_phone_email(self, phone_number, email, password):
        
        if email and password:
            user = authenticate(username=email, password=password)
        elif str(phone_number) and password:
            user = authenticate(username=str(phone_number),password=password)
        else:
            raise serializers.ValidationError(_("Enter an email or a phone number."))
        
        return user
    
    
    def validate(self, attrs):
        phone_number = attrs.get("phone_number", None)
        email = attrs.get("email", None)
        password = attrs.get("password", None)
        
        user = self._validate_phone_email(phone_number, email, password)
        
        if not user:
            raise InvalidCredentialsException()

        if not user.is_active:
            raise AccountDisabledException()
        
        if email:
            email_address = user.emailaddress_set.filter(email=user.email, verified=True).exists()
            if not email_address:
                raise serializers.ValidationError(_("Email address is not verified."))
            
        else:
            if not user.phone.is_verified:
                raise serializers.ValidationError(_("Phone number is not verified."))
            
        attrs["user"] = user
        return attrs


    
class PhoneNumberSerializer(serializers.ModelSerializer):
    """
    Serializer for phone number
    """
    
    phone_number = PhoneNumberField()
    
    class Meta:
        model = PhoneNumber
        fields = ["phone_number"]
        
    def validate_phone_number(self, value):
        try:
            queryset = User.objects.get(phone__phone_number=value) 
            if queryset.phone.is_verified:
                raise serializers.ValidationError(_("Phone number is already verified."))
            
        except User.DoesNotExist:
            raise AccountNotRegisteredException()
        
        return value
    

    
class VerifyPhoneNumberSerializer(serializers.Serializer):
    """
    Serializer to verify phone number
    """
    
    phone_number = PhoneNumberField()
    verification_code = serializers.CharField(max_length=settings.TOKEN_LENGTH)
    
    def validate_phone_number(self, value):
        queryset = User.objects.filter(phone__phone_number=value)
        if not queryset.exists():
            raise AccountNotRegisteredException()
        return value
    
    def validate(self, attrs):
        phone_number = str(attrs.get("phone_number"))
        verification_code = attrs.get("otp")
        
        queryset = PhoneNumber.objects.get(phone__phone_number=phone_number)
        
        queryset.check_verification(security_code=verification_code)
        return attrs
    

    
class ProfileSerializer(serializers.ModelSerializer):
    """
    Serializer class to serialize the user Profile model
    """

    class Meta:
        model = Profile
        fields = (
            "avatar",
            "bio",
            "created_at",
            "updated_at",
        ) 
        
        
class AddressReadOnlySerializer(CountryField, serializers.ModelSerializer):
    """
    Serializer class to seralize Address model
    """

    user = serializers.CharField(source="user.get_full_name", read_only=True)

    class Meta:
        model = Address
        fields = "__all__"
        
        
class UserSerializer(serializers.ModelSerializer):
    """
    Serializer class to seralize User model
    """

    profile = ProfileSerializer(read_only=True)
    phone_number = PhoneNumberField(source="phone", read_only=True)
    addresses = AddressReadOnlySerializer(read_only=True, many=True)

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "phone_number",
            "first_name",
            "last_name",
            "is_active",
            "profile",
            "addresses",
        )
        

class ShippingAddressSerializer(CountryField, serializers.ModelSerializer):
    """
    Serializer class to seralize address of type shipping

    For shipping address, automatically set address type to shipping
    """

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Address
        fields = "__all__"
        read_only_fields = ("address_type",)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["address_type"] = "S"

        return representation
    
    

class BillingAddressSerializer(CountryField, serializers.ModelSerializer):
    """
    Serializer class to seralize address of type billing

    For billing address, automatically set address type to billing
    """

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Address
        fields = "__all__"
        read_only_fields = ("address_type",)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["address_type"] = "B"

        return representation
        
            
        
        
    




