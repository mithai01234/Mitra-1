import phonenumbers
from phonenumbers.phonenumberutil import PhoneNumberFormat

import random
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

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
    referral_code = models.CharField(max_length=10, blank=True, null=True)
    password = models.CharField(max_length=128)  # Store the password as a hash.
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_date=models.DateField(auto_now_add=True)
    blocked_users = models.ManyToManyField('self', symmetrical=False, blank=True, related_name='users_blocked_by')
    username_code = models.CharField(max_length=15, blank=True, null=True)
    status = models.IntegerField(default=1)
    email = models.EmailField(unique=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['name']




    def save(self, *args, **kwargs):
        # Generate a referral code if it doesn't already exist
        if not self.username_code:
            self.username_code = f"{self.name[:4]}_{random.randint(1000, 9999)}"

        super(CustomUser, self).save(*args, **kwargs)
    def __str__(self):
        return f'{self.id} '


class OTP(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    otp_value = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)


    def __str__(self):
        return f'{self.user.name} OTP: {self.otp_value}'

class Referral(models.Model):
    id = models.AutoField(primary_key=True)
    uid = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    sponser_id = models.IntegerField()  # Assuming sponser_id is an integer
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.99)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_date = models.DateField(auto_now_add=True)

    def calculate_referral_bonus(self):
        # Define the referral bonus calculation logic here
        # This function will be called when a new referral is added

        # Calculate the bonus for the current referral
        bonus = self.amount

        # Update the user's total_amount
        self.total_amount += bonus
        self.save()

        # Check if there is a sponsor
        if self.sponser_id:
            # Find the sponsor
            sponsor = Referral.objects.filter(uid_referral_code=self.sponser_id).first()
            if sponsor:
                # Calculate the bonus for the sponsor
                sponsor.amount += bonus * 0.20  # You can adjust the percentage as needed
                sponsor.save()

                # Recursively calculate bonuses for higher-level sponsors
                sponsor.calculate_referral_bonus()

    def save(self, *args, **kwargs):
        # Override the save method to calculate referral bonuses
        self.calculate_referral_bonus()
        super(Referral, self).save(*args, **kwargs)