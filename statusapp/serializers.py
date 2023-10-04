from rest_framework import serializers
from .models import Statusapp

class StatusappSerializer(serializers.ModelSerializer):
    class Meta:
        model = Statusapp
        fields = '__all__'
