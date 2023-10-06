from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, login
from .serializers import CustomUserSerializer,ReferralSerializer,PasswordResetSerializer,PasswordUpdateSerializer
import boto3
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import CustomUser,OTP
# from .serializers import UserProfileSerializer
from rest_framework import viewsets
from rest_framework import viewsets

from django.core.mail import send_mail
import random
from django.conf import settings

from rest_framework.decorators import api_view
class RegistrationView(APIView):
    def post(self, request):
        serializer = CustomUserSerializer(data=request.data)

        print(request.data, "============")
        if serializer.is_valid():
            user = serializer.save()

            refresh = RefreshToken.for_user(user)

            response_data = {
                'refresh': str(refresh)
                ,
                'access': str(refresh.access_token),
            }
            return Response(response_data, status=201)
        return Response(serializer.errors, status=400)



class LoginView(APIView):
    def post(self, request):
        phone = request.data.get('phone_number')
        password = request.data.get('password')

        user = authenticate(request, phone_number=phone,password=password)

        if user:
            refresh = RefreshToken.for_user(user)

            response_data = {
                            "status": "success",
                            "message": "Customer logged in successfully",
                            "User": {
                                "id": str(user.id),
                               # Add the user's profile pic if available
                                "name": user.name,
                                "phone_number": user.phone_number,
                                "create_date": user.created_date.strftime('%Y-%m-%d'),  # Format the date as needed
                                "status": "1"  # Assuming 'status' is a fixed value
                            }
                        }


            return Response(response_data, status=200)
        return Response({'error': 'Invalid credentials'}, status=401)


@api_view(['POST'])
def request_password_reset(request):
    serializer = PasswordResetSerializer(data=request.data)

    if serializer.is_valid():
        email = serializer.validated_data['email']

        try:
            otp = generate_otp()  # Generate the OTP
            user = CustomUser.objects.get(email=email)
            send_otp_to_email(email, otp)  # Send the OTP to the user's email
            create_or_update_otp(user, otp)  # Create or update the OTP record
            return Response({"message": "OTP sent to your email"}, status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            return Response({"message": "Email not found"}, status=status.HTTP_404_NOT_FOUND)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def verify_otp(request):
    otp_value = request.data.get('otp')

    try:
        otp_obj = OTP.objects.get(otp_value=otp_value, is_used=False)
        user = otp_obj.user

        # Mark OTP as used
        otp_obj.is_used = True
        otp_obj.save()

        return Response({'message': 'OTP verified successfully', 'otp': otp_value}, status=status.HTTP_200_OK)
    except OTP.DoesNotExist:
        return Response({'error': 'Invalid OTP or OTP already used'}, status=status.HTTP_400_BAD_REQUEST)
    except CustomUser.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
# {
# "otp":"200739","new_passwod":"qwer"}

@api_view(['POST'])
def update_password(request):
    serializer = PasswordUpdateSerializer(data=request.data)

    if serializer.is_valid():
        otp_value = serializer.validated_data.get('otp')
        new_password = serializer.validated_data.get('new_password')

        try:
            # Check if the OTP is valid and marked as in use
            otp_obj = OTP.objects.get(otp_value=otp_value, is_used=True)

            # Get the user ID associated with the OTP
            user_id = otp_obj.user_id

            # Retrieve the user based on user_id
            user = CustomUser.objects.get(id=user_id)

            # Set and hash the new password for the user
            user.set_password(new_password)
            user.save()

            return Response({'message': 'Password updated successfully'}, status=status.HTTP_200_OK)

        except OTP.DoesNotExist:
            return Response({'error': 'Invalid OTP or OTP not marked as in use'}, status=status.HTTP_400_BAD_REQUEST)
        except CustomUser.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
def generate_otp():
    return ''.join([str(random.randint(0, 9)) for _ in range(6)])


def send_otp_to_email(email, otp):
    subject = "Password Reset OTP"
    message = f"Your OTP for password reset is: {otp}"
    from_email = settings.EMAIL_HOST_USER  # Replace with your email configuration
    recipient_list = [email]
    send_mail(subject, message, from_email, recipient_list, fail_silently=False)


def create_or_update_otp(user, otp):
    otp_obj, created = OTP.objects.get_or_create(user=user)

    # Check if the OTP is being created for the first time or is being updated
    if not created:
        # If the OTP record already exists, reset is_used to False
        otp_obj.is_used = False

    otp_obj.otp_value = otp
    otp_obj.save()
