from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, login

from videoupload.models import Video
from .serializers import CustomUserSerializer,PasswordResetSerializer,PasswordUpdateSerializer
import boto3
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import CustomUser, OTP,  TableJoining
# from .serializers import UserProfileSerializer
from rest_framework import viewsets
from rest_framework import viewsets
from decimal import Decimal
from django.core.mail import send_mail
import random
from django.conf import settings
from rest_framework.permissions import BasePermission
from rest_framework_api_key.permissions import HasAPIKey
from rest_framework.decorators import api_view
from decimal import Decimal

# class RegistrationView(APIView):
#     def post(self, request):
#         serializer = CustomUserSerializer(data=request.data)
#
#         if serializer.is_valid():
#             user = serializer.save()
#
#             # Check if a referral code was provided by the user
#             referral_code = request.data.get('referral_code')
#             if referral_code:
#                 try:
#                     referrer = CustomUser.objects.get(username_code=referral_code)
#
#                     # Determine the level of the new user
#                     if referrer.username_code:
#                         sponsor_username_code = referrer.username_code
#                         try:
#                             sponsor = CustomUser.objects.get(username_code=sponsor_username_code)
#                         except CustomUser.DoesNotExist:
#                             sponsor = None
#
#                         if sponsor:
#                             user_level = sponsor.level + 1
#                         else:
#                             user_level = 1
#                     else:
#                         user_level = 1
#
#                     # Set the level for the new user
#                     user.level = user_level
#                     user.save()
#
#
#
#
#
#
#
#
#                     if referrer.username_code:
#                         sponsor_username_code = referrer.username_code
#                         try:
#                             sponsor = CustomUser.objects.get(username_code=sponsor_username_code)
#                         except CustomUser.DoesNotExist:
#                             sponsor = None
#
#                         if sponsor:
#                             # Define the reward amount based on the level
#                             amount=0.40
#
#                             # Create a TableJoining record for the sponsor at this level
#                             TableJoining.objects.create(uid=sponsor, sponser_id=user, amount=amount,
#                                                         total_amount=sponsor.total_amount)
#
#                             # Update the total_amount for the sponsor
#                             sponsor.total_amount += Decimal(amount)
#                             sponsor.save()
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#                     # Generate income for referrers at different levels
#                     for level in range(1, user_level+1):
#                         # Check if the referrer has a sponsor at this level
#                         if referrer.referral_code:
#                             sponsor_username_code = referrer.referral_code
#                             try:
#                                 sponsor = CustomUser.objects.get(username_code=sponsor_username_code)
#                             except CustomUser.DoesNotExist:
#                                 sponsor = None
#
#                             if sponsor:
#                                 # Define the reward amount based on the level
#                                 if level == 1:
#                                     amount = 0.15
#                                 elif level == 2:
#                                     amount = 0.10
#                                 elif level == 3:
#                                     amount = 0.10
#                                 elif level == 4:
#                                     amount = 0.10
#                                 elif level == 5:
#                                     amount = 0.10
#                                 elif level == 6:
#                                     amount = 0.05
#                                 elif level == 7:
#                                     amount = 0.05
#                                 elif level == 8:
#                                     amount = 0.05
#                                 elif level == 9:
#                                     amount = 0.05
#                                 elif level == 10:
#                                     amount = 0.03
#                                 elif level == 11:
#                                     amount = 0.03
#                                 elif level == 12:
#                                     amount = 0.03
#                                 elif level == 13:
#                                     amount = 0.02
#                                 elif level == 14:
#                                     amount = 0.02
#                                 else:
#                                     amount = 0.0  # Adjust for higher levels as needed
#
#                                 # Create a TableJoining record for the sponsor at this level
#                                 TableJoining.objects.create(uid=sponsor, sponser_id=user, amount=amount,
#                                                             total_amount=sponsor.total_amount)
#
#                                 # Update the total_amount for the sponsor
#                                 sponsor.total_amount += Decimal(amount)
#                                 sponsor.save()
#
#                                 # Set the sponsor as the new referrer for the next level
#                                 referrer = sponsor
#                             else:
#                                 # No sponsor at this level, break out of the loop
#                                 break
#
#                 except CustomUser.DoesNotExist:
#                     pass
#
#             return Response({'message': 'Registration successful'}, status=201)
#
#         return Response(serializer.errors, status=400)
class RegistrationView(APIView):
    def post(self, request):
        serializer = CustomUserSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()

            # Check if a referral code was provided by the user
            referral_code = request.data.get('referral_code', 'admi_1541')

            if referral_code:
                user.referral_code = referral_code
                try:

                    referrer = CustomUser.objects.get(username_code=referral_code)

                    # Determine the level of the new user
                    if referrer.username_code:
                        sponsor_username_code = referrer.username_code
                        try:
                            sponsor = CustomUser.objects.get(username_code=sponsor_username_code)
                        except CustomUser.DoesNotExist:
                            sponsor = None

                        if sponsor:
                            user_level = sponsor.level + 1
                        else:
                            user_level = 1
                    else:
                        user_level = 1

                    # Set the level for the new user
                    user.level = user_level
                    user.save()








                    if referrer.username_code:
                        sponsor_username_code = referrer.username_code
                        try:
                            sponsor = CustomUser.objects.get(username_code=sponsor_username_code)
                        except CustomUser.DoesNotExist:
                            sponsor = None

                        if sponsor:
                            # Define the reward amount based on the level
                            amount=0.40

                            # Create a TableJoining record for the sponsor at this level
                            TableJoining.objects.create(uid=sponsor, sponser_id=user, amount=amount,
                                                        total_amount=sponsor.total_amount)

                            # Update the total_amount for the sponsor
                            sponsor.total_amount += Decimal(amount)
                            sponsor.save()














                    # Generate income for referrers at different levels
                    for level in range(1, user_level+1):
                        # Check if the referrer has a sponsor at this level
                        if referrer.referral_code:
                            sponsor_username_code = referrer.referral_code
                            try:
                                sponsor = CustomUser.objects.get(username_code=sponsor_username_code)
                            except CustomUser.DoesNotExist:
                                sponsor = None

                            if sponsor:
                                # Define the reward amount based on the level
                                if level == 1:
                                    amount = 0.15
                                elif level == 2:
                                    amount = 0.10
                                elif level == 3:
                                    amount = 0.10
                                elif level == 4:
                                    amount = 0.10
                                elif level == 5:
                                    amount = 0.10
                                elif level == 6:
                                    amount = 0.05
                                elif level == 7:
                                    amount = 0.05
                                elif level == 8:
                                    amount = 0.05
                                elif level == 9:
                                    amount = 0.05
                                elif level == 10:
                                    amount = 0.03
                                elif level == 11:
                                    amount = 0.03
                                elif level == 12:
                                    amount = 0.03
                                elif level == 13:
                                    amount = 0.02
                                elif level == 14:
                                    amount = 0.02
                                else:
                                    amount = 0.0  # Adjust for higher levels as needed

                                # Create a TableJoining record for the sponsor at this level
                                TableJoining.objects.create(uid=sponsor, sponser_id=user, amount=amount,
                                                            total_amount=sponsor.total_amount)

                                # Update the total_amount for the sponsor
                                sponsor.total_amount += Decimal(amount)
                                sponsor.save()

                                # Set the sponsor as the new referrer for the next level
                                referrer = sponsor
                            else:
                                # No sponsor at this level, break out of the loop
                                break

                except CustomUser.DoesNotExist:
                    pass

            return Response({'message': 'Registration successful'}, status=201)

        return Response(serializer.errors, status=400)
# {
#     "phone_number":
#         "444444444"
#     ,
#     "name":
#         "This field is required."
#     ,
#     "password":
#         "qwhhjhrr@123"
#     ,
#     "email":
#         "ftyf44545tf@gmail.com"
#     , "referral_code": "admi_9174"
#
# }
# def assign_referral_points(referral, referring_user):
#     # Calculate the points based on the referring user's level
#     referral_level = referring_user.referral.level
#     points = Decimal('0.02') * (2 ** (referral_level - 1))
#
#     # Update the referral's level and points
#     referral.level = referral_level + 1
#     referral.points = points
#     referral.save()
#
from .serializers import ProfileUpdateSerializer

class ProfileUpdateView(APIView):

    def put(self, request):
        user_id = request.data.get('id', None)
        name = request.data.get('name', None)
        bio = request.data.get('bio', None)
        profile_photo = request.data.get('profile_photo', None)

        if user_id is None:
            return Response({'error': 'User ID is required'}, status=400)

        try:
            user = CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            return Response({'error': 'User not found'}, status=404)

        if name is not None:
            user.name = name
        if bio is not None:
            user.bio = bio
        if profile_photo is not None:
            user.profile_photo = profile_photo

        user.save()

        serializer = ProfileUpdateSerializer(user)
        return Response(serializer.data)

from django.shortcuts import get_object_or_404
from django.http import JsonResponse

def user_profile(request):
    user_id = request.GET.get('user_id')

    if user_id is not None:
        user = get_object_or_404(CustomUser, id=user_id)
        referred_users = TableJoining.objects.filter(uid=user)
        referred_users_data = []

        for referred_user in referred_users:
            referred_users_data.append({
                'username': referred_user.sponser_id.name,
                'date': referred_user.created_date,
                'income': referred_user.amount,
                'level': referred_user.sponser_id.level,
            })

        user_profile_data = {
            'username_code': user.username_code,
            'level': user.level,
            'total_income': user.total_amount,
            'referred_users': referred_users_data,
        }

        return JsonResponse(user_profile_data)

    return JsonResponse({'error': 'User not found'}, status=404)
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
                               # Add the user's profile pic if
                                "referral_code":user.referral_code,
                                "username_code":user.username_code,
                                "slug":user.slug,
                                "name": user.name,
                                "phone_number": user.phone_number,
                                "create_date": user.created_date.strftime('%Y-%m-%d'),  # Format the date as needed
                                "status": "1"  # Assuming 'status' is a fixed value
                            }
                        }


            return Response(response_data, status=200)
        return Response({'error': 'Invalid credentials'}, status=401)

from django.db.models import Count
def video_count_per_user(request):
    user_id = request.GET.get('user_id', None)

    if user_id is not None:
        video_count = Video.objects.filter(user_id=user_id).count()
        video_count_dict = {user_id: video_count}
        return JsonResponse(video_count_dict)
    else:
        return JsonResponse({'error': 'user_id parameter is required'}, status=400)
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
