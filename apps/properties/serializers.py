# apps/properties/serializers.py
from rest_framework import serializers
from .models import Property
from apps.profiles.serializers import ProfileSerializer



# apps/properties/serializers.py
from .models import Property, PropertyImage # Import PropertyImage

class PropertyImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyImage
        fields = ["id", "property", "image"]



class PropertySerializer(serializers.ModelSerializer):
    profile = serializers.SerializerMethodField()
    final_property_price = serializers.SerializerMethodField()
    images = PropertyImageSerializer(many=True, read_only=True) # <--- ADD THIS LINE

    class Meta:
        model = Property
        fields = [
            "id", "user", "profile", "title", "slug", "ref_code",
            "description", "country", "city", "postal_code",
            "street_address", "property_number", "price", "tax",
            "final_property_price", "plot_area", "total_floors",
            "bedrooms", "bathrooms", "advert_type", "property_type",
            "cover_photo", "published_status", "views", 
            "images" # <--- ADD THIS TO FIELDS
        ]

    def get_profile(self, obj):
        # Returns the Agent's profile info who posted this property
        return ProfileSerializer(obj.user.profile).data

    def get_final_property_price(self, obj):
        return obj.final_property_price

class PropertyCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        exclude = ["updated_at", "pkid"]

# apps/properties/serializers.py (add at the bottom)

from .models import PropertySearch

class PropertySearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertySearch
        fields = ["id", "title", "criteria", "created_at"]