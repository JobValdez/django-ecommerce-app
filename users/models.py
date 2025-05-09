from django.db import models
from django.conf import settings
from twilio.rest import Client
from django.utils import timezone
from rest_framework.exceptions import NotAcceptable
from twilio.base.exceptions import TwilioRestException
from django.utils.translation import gettext_lazy as _
from django.utils.crypto import get_random_string
from django_countries.fields import CountryField
from django.contrib.auth import get_user_model
from phonenumber_field.modelfields import PhoneNumberField


User = get_user_model()

class PhoneNumber(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='phone_number')
    phone_number = PhoneNumberField(unique=True)
    security_code = models.CharField(max_length=100)
    is_verified = models.BooleanField(default=False)
    sent = models.DateTimeField(null=True)
    
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return self.phone_number
    
    def generate_security_code(self):
        """
        Returns a random digit security code, default length = 6
        """
        
        token_length = getattr(settings, 'TOKEN_LENGTH', 6)
        return get_random_string(length=token_length, allowed_chars='0123456789')
    
    
    def is_security_code_expired(self):
        """
        Checks if the security code has expired
        """
        
        expiration_date = self.sent + timezone.timedelta(minutes=settings.TOKEN_EXPIRE_MINUTES)
        return expiration_date <= timezone.now()
    
    
    def send_confirmation(self):
        """
        Sends the confirmation code to the user
        """
        twilio_account_sid = getattr(settings, 'TWILIO_ACCOUNT_SID')
        twilio_auth_token = getattr(settings, 'TWILIO_AUTH_TOKEN')
        twilio_phone_number = getattr(settings, 'TWILIO_PHONE_NUMBER')
        
        self.security_code = self.generate_security_code()
        
        if all([twilio_account_sid, twilio_auth_token, twilio_phone_number]):
            try:
                twilio_client = Client(twilio_account_sid, twilio_auth_token)
                twilio_client.messages.create(
                    body=f"Your verification code is {self.security_code}",
                    to=str(self.phone_number),
                    from_=twilio_phone_number
                )
                self.sent = timezone.now()
                self.save()
                
            except TwilioRestException as e:
                print(e)
                return False
            
    
    def check_verification(self, security_code):
        """
        Checks if the security code is valid
        """
        
        if all([self.security_code == security_code, not self.is_verified, not self.is_security_code_expired() ]):
            self.is_verified = True
            self.save()
            
        else:
            raise NotAcceptable(
                _( 
                    "Your security code is wrong, expired or this phone is verified before."
                )
            )
            
class Profile(models.Model):
    user = models.OneToOneField(User, related_name="profile", on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to="avatar", blank=True)
    bio = models.CharField(max_length=200, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return self.user.get_full_name()
            



class Address(models.Model):
    # Address options
    BILLING = "B"
    SHIPPING = "S"

    ADDRESS_CHOICES = ((BILLING, _("billing")), (SHIPPING, _("shipping")))

    user = models.ForeignKey(User, related_name="addresses", on_delete=models.CASCADE)
    address_type = models.CharField(max_length=1, choices=ADDRESS_CHOICES)
    default = models.BooleanField(default=False)
    country = CountryField()
    city = models.CharField(max_length=100)
    street_address = models.CharField(max_length=100)
    apartment_address = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return self.user.get_full_name()

    
