import phonenumbers
from django.utils.text import slugify
from phonenumbers.phonenumberutil import PhoneNumberFormat
from decimal import Decimal
import random
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

# class User(models.Model):
#     id = models.AutoField(primary_key=True)
#     phone_number = models.CharField(max_length=15, unique=True)  # You can adjust the max_length as needed.
#     name = models.CharField(max_length=255)
#     referral_code = models.CharField(max_length=10, blank=True, null=True)
#     password = models.CharField(max_length=128)  # Store the password as a hash.
#     is_active = models.BooleanField(default=True)
#     is_staff = models.BooleanField(default=False)
#     created_date = models.DateField(auto_now_add=True)
#     blocked_users = models.ManyToManyField('self', symmetrical=False, blank=True, related_name='users_blocked_by')
#     username_code = models.CharField(unique=True, max_length=15, blank=True, null=True)
#     status = models.IntegerField(default=1)
#     email = models.EmailField(unique=True)
#     slug = models.CharField(max_length=15, blank=True, unique=True, null=True)
#     # Fields and attributes for the `CustomUser` model
#
#     class Meta:
#         app_label = 'registration'

class CustomUserManager(BaseUserManager):
    def create_user(self, phone_number, password=None, name=None, referral_code=None, **extra_fields):
        if not phone_number:
            raise ValueError('The phone number field must be set')
        user = self.model(phone_number=phone_number, name=name, referral_code=referral_code, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password=None, name=None, referral_code=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(phone_number, password, name, referral_code, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    id= models.AutoField(primary_key=True)
    phone_number = models.CharField(max_length=15, unique=True)  # You can adjust the max_length as needed.
    name = models.CharField(max_length=255)
    bio=models.CharField(max_length=255,default='')
    profile_photo=models.ImageField(upload_to='videos/', null=True, blank=True)
    referral_code = models.CharField(max_length=10, blank=True, null=True)
    password = models.CharField(max_length=128)  # Store the password as a hash.
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_date=models.DateField(auto_now_add=True)
    blocked_users = models.ManyToManyField('self', symmetrical=False, blank=True, related_name='users_blocked_by')
    username_code = models.CharField(unique=True,max_length=15, blank=True, null=True)
    status = models.IntegerField(default=1)
    email = models.EmailField(unique=True)
    slug = models.CharField(max_length=15, blank=True,unique=True, null=True)
    objects = CustomUserManager()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    level = models.PositiveIntegerField(default=1)
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['name']

    def update_total_amount(self, amount):
        self.total_amount += Decimal(amount)
        self.save()



    def save(self, *args, **kwargs):
        if not self.username_code:
            self.username_code = f"{self.name[:4]}_{random.randint(1000, 9999)}"
        if not self.slug:
            self.slug = f"{random.randint(1000, 9999)}"

        super(CustomUser, self).save(*args, **kwargs)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.id} '


class OTP(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    otp_value = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)


    def __str__(self):
        return f'{self.user.name} OTP: {self.otp_value}'

# class Referral(models.Model):
#     id = models.AutoField(primary_key=True)
#     uid = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
#     sponser_id = models.IntegerField()  # Assuming sponser_id is an integer
#     amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.99)
#     total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
#     created_date = models.DateField(auto_now_add=True)
#
#     def calculate_referral_bonus(self):
#         # Define the referral bonus calculation logic here
#         # This function will be called when a new referral is added
#
#         # Calculate the bonus for the current referral
#         bonus = self.amount
#
#         # Update the user's total_amount
#         self.total_amount += bonus
#         self.save()
#
#         # Check if there is a sponsor
#         if self.sponser_id:
#             # Find the sponsor
#             sponsor = Referral.objects.filter(uid_referral_code=self.sponser_id).first()
#             if sponsor:
#                 # Calculate the bonus for the sponsor
#                 sponsor.amount += bonus * 0.20  # You can adjust the percentage as needed
#                 sponsor.save()
#
#                 # Recursively calculate bonuses for higher-level sponsors
#                 sponsor.calculate_referral_bonus()
#
#     def save(self, *args, **kwargs):
#         # Override the save method to calculate referral bonuses
#         self.calculate_referral_bonus()
#         super(Referral, self).save(*args, **kwargs)
class TableJoining(models.Model):
    uid = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='referral_rewards_received')
    sponser_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='referral_rewards_given')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'Reward from {self.sponser_id} to {self.uid}'

    class Meta:
        verbose_name_plural = 'TableJoining'
# def assign_referral_points(user, referring_user):
#     # Calculate the points based on the referring user's level
#     referral_level = referring_user.referral.level
#     points = Decimal('0.02') * (2 ** (referral_level - 1))
#
#     # Update the user's level and points
#     user.referral.level = referral_level + 1
#     user.referral.points = points
#     user.referral.save()
#
# def register_user_with_referral_code(username, referral_code):
#     try:
#         referred_user = CustomUser.objects.get(username=username)
#     except CustomUser.DoesNotExist:
#         # Handle the case where the referred user does not exist
#         return
#
#     try:
#         referring_user = CustomUser.objects.get(referral_code=referral_code)
#     except CustomUser.DoesNotExist:
#         # If there's no referring user with the given referral_code, assign level 1 to the referred user
#         referred_user.referral.level = 1
#         referred_user.referral.points = Decimal('0.02')
#         referred_user.referral.save()
#     else:
#         # If there's a referring user, assign points and increase levels accordingly
#         assign_referral_points(referred_user, referring_user)
#
#     # Create a Referral record for the registered user
#     Referral.objects.create(user=referred_user)

# Usage example:
# Assuming you have a registered user with the username 'new_user' and a referral code 'referrer_code'
class Joining(models.Model):
    uid = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    sponser_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sponsored_users')
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.99)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_date = models.DateField(auto_now_add=True)

class Reward(models.Model):
    uid = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    sponser_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sponsored_rewards')
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_date = models.DateField(auto_now_add=True)


