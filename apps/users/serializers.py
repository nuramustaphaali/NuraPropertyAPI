# apps/users/serializers.py
from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from rest_framework import serializers

User = get_user_model()

class CreateUserSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        model = User
        fields = ['id', 'email', 'full_name', 'password', 'city', 'address', 'profile_photo']