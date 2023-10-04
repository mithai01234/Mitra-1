
from .views import *
from django.urls import path

urlpatterns = [
    # path('backend/dashboard', dashboard , name="backend/dashboard"),
    path('register/', RegistrationView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),


    path('request-password-reset/', request_password_reset, name='request_password_reset'),
    path('verify-otp/', verify_otp, name='verify_otp'),
    path('update-password/', update_password, name='update_password'),
]


