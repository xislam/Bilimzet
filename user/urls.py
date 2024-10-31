from django.urls import path

from user.api.api_login import LoginOrRegisterView
from user.api.api_password_reset import PasswordResetView
from user.api.api_profile import UserProfileUpdateView, UserProfileDetailView, UserProfileDeleteView, \
    UserPasswordUpdateView, AdditionalInfoView
from user.api.api_register import RegistrationView
from user.api.api_request_password_reset import RequestPasswordResetView
from user.api.api_verification_number import PhoneNumberVerificationView, PhoneNumberCheckView, \
    RequestVerificationCodeView, TokenObtainView, PasswordUpdateView

urlpatterns = [
    path('register/', RegistrationView.as_view(), name='register'),
    path('verify-phone/', PhoneNumberVerificationView.as_view(), name='verify_phone'),
    path('check-phone/', PhoneNumberCheckView.as_view(), name='phone-number-check'),
    path('additional-info/', AdditionalInfoView.as_view(), name='additional-info'),
    path('login/', LoginOrRegisterView.as_view(), name='login'),
    path('profile/update/', UserProfileUpdateView.as_view(), name='profile-update'),
    path('profile/', UserProfileDetailView.as_view(), name='user-profile-detail'),
    path('user/delete/', UserProfileDeleteView.as_view(), name='user-delete'),
    path('request-password-reset/', RequestPasswordResetView.as_view(), name='request-password-reset'),
    path('password-reset/', PasswordResetView.as_view(), name='password-reset'),
    path('user/update-password/', UserPasswordUpdateView.as_view(), name='user-update-password'),
    path('auth/request-verification/', RequestVerificationCodeView.as_view(), name='request-verification'),
    path('auth/token/', TokenObtainView.as_view(), name='token-obtain'),
    path('auth/update-password/', PasswordUpdateView.as_view(), name='update-password'),

]
