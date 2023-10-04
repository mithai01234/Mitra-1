# serializers.py

from rest_framework import serializers
from .models import Follow
class RelationshipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = '__all__'
