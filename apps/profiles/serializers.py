# apps/profiles/serializers.py
from rest_framework import serializers
from .models import Profile

class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username")
    full_name = serializers.CharField(source="user.full_name")
    email = serializers.EmailField(source="user.email")
    is_agent = serializers.BooleanField(source="user.is_agent")

    class Meta:
        model = Profile
        fields = [
            "username", "full_name", "email", "id", "phone_number",
            "about_me", "license_number", "profile_photo", "city", 
            "is_buyer", "is_seller", "is_agent", "rating", "num_reviews"
        ]
        
class UpdateProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["phone_number", "about_me", "license_number", "city", "is_buyer", "is_seller", "is_agent"]