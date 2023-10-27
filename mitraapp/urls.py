
from .views import *
from django.urls import path

urlpatterns = [
    path('backend/dashboard', dashboard , name="backend/dashboard"),
    path('backend/userlist/user_profile/<int:myid>/', user_profile, name='userlist/user_profile'),
    path('backend/userlist/share_income/<int:myid>/', share_income, name='userlist/share_income'),
]


