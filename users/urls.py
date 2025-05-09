from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    AddressViewSet,
    ProfileAPIView,
    SendOrResendSMSAPIView,
    UserAPIView,
    UserLoginAPIView,
    UserRegistrationAPIView,
    VerifyPhoneNumberAPIView,
)

app_name = "users"

router = DefaultRouter()
router.register(r"", AddressViewSet)

urlpatterns = [
    path("register/", UserRegistrationAPIView.as_view(), name="user_register"),
    path("login/", UserLoginAPIView.as_view(), name="user_login"),
    path("send-sms/", SendOrResendSMSAPIView.as_view(), name="send_resend_sms"),
    path(
        "verify-phone/", VerifyPhoneNumberAPIView.as_view(), name="verify_phone_number"
    ),
    path("", UserAPIView.as_view(), name="user_detail"),
    path("profile/", ProfileAPIView.as_view(), name="profile_detail"),
    path("profile/address/", include(router.urls)),
]
