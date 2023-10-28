from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework import serializers
# from .models import Referral
# from .models import UserProfile
User = get_user_model()

class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ('phone_number', 'name', 'password', 'email', 'referral_code', 'profile_photo', 'bio')

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
# class ReferralSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Referral
#         fields = '__all__'
# from rest_framework import serializers
class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = User  # Replace with your actual model
        fields = '__all__'  # Serialize all fields of the model
class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()
from .models import OTP, CustomUser


class OTPSerializer(serializers.ModelSerializer):
    class Meta:
        model = OTP
        fields = ('id', 'user', 'otp_value', 'created_at', 'is_used')
class PasswordUpdateSerializer(serializers.Serializer):
    otp = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
class ProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'name', 'bio', 'profile_photo')
# class UserProfileSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = UserProfile
#         fields = '__all__'
# {
# {
# "phone_number":"9823082902",
# "name":"Srutee",
# "password":"Srutee123456",
#
#
# "referral_code":"dsfsdf"
#
# }
#

