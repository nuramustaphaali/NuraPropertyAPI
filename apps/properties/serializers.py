# apps/properties/serializers.py
from rest_framework import serializers
from .models import Property, PropertyImage, PropertySearch
from apps.profiles.serializers import ProfileSerializer

class PropertyImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyImage
        fields = ["id", "property", "image"]

class PropertySerializer(serializers.ModelSerializer):
    profile = serializers.SerializerMethodField()
    final_property_price = serializers.SerializerMethodField()
    images = PropertyImageSerializer(many=True, read_only=True)
    user_name = serializers.ReadOnlyField(source='user.full_name') # Handy for frontend
    
    class Meta:
        model = Property
        fields = [
            'id', 
            'user', 
            'user_name',
            'profile',  # <--- Added this so get_profile works
            'title', 
            'slug', 
            'ref_code', 
            'description',
            'country', 
            'city', 
            'postal_code', 
            'street_address', 
            'property_number',
            'price', 
            'final_property_price', # <--- Added this
            'tax', 
            'plot_area', 
            'total_floors', 
            'bedrooms', 
            'bathrooms',
            'advert_type', 
            'property_type', 
            'cover_photo', 
            'published_status', 
            'views', 
            'images', 
            'created_at', 
            'updated_at'
        ]
        read_only_fields = ['user', 'slug', 'ref_code', 'views']

    def get_profile(self, obj):
        # Returns the Agent's profile info who posted this property
        return ProfileSerializer(obj.user.profile).data

    def get_final_property_price(self, obj):
        return obj.final_property_price

class PropertyCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        exclude = ["updated_at", "pkid"]
        # CRITICAL FIX: This line prevents the "user field is required" error
        read_only_fields = ["user", "slug", "ref_code", "views"]

class PropertySearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertySearch
        fields = ["id", "title", "criteria", "created_at"]