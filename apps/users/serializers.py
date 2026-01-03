# apps/users/serializers.py
from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer, UserSerializer as BaseUserSerializer
from rest_framework import serializers

User = get_user_model()

class CreateUserSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        model = User
        fields = ['id', 'email', 'full_name', 'password', 'city', 'address', 'is_agent', 'profile_photo']

# ADD THIS CLASS to handle "GET /me/" correctly
class CustomUserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        model = User
        # We explicitly include is_agent so the frontend can check the role
        fields = ['id', 'email', 'full_name', 'city', 'address', 'is_agent', 'profile_photo']