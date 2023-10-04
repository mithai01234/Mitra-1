
from .views import *
from django.urls import path

urlpatterns = [
    path('backend/dashboard', dashboard , name="backend/dashboard"),
]


