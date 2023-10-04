from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser,Referral,OTP

class CustomUserAdmin(UserAdmin):
    list_display = ('phone_number','username_code','status', 'name', 'referral_code', 'is_active', 'is_staff')
    list_filter = ('is_active', 'is_staff')
    search_fields = ('phone_number', 'name', 'referral_code')
    ordering = ('phone_number',)

    fieldsets = (
        (None, {'fields': ('phone_number', 'email', 'password','status')}),
        ('Personal Info', {'fields': ('name', 'username_code','referral_code')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone_number', 'name', 'email','referral_code', 'password1', 'password2'),
        }),
    )

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Referral)

admin.site.register(OTP)
# {
#     "phone_number":
#         "56565656"
#     ,
#     "name":
#         "dfdfdfffdired."
#     ,
#     "password":
#         "admin@gmail.com",
#     "email": "mithai01234@gmail.com"
#
# }