# apps/interactions/serializers.py
from rest_framework import serializers
from .models import PropertyInspection
from apps.properties.serializers import PropertySerializer

class InspectionSerializer(serializers.ModelSerializer):
    property_title = serializers.ReadOnlyField(source="property.title")
    property_slug = serializers.ReadOnlyField(source="property.slug")
    client_name = serializers.ReadOnlyField(source="user.full_name")
    client_email = serializers.ReadOnlyField(source="user.email")
    agent_name = serializers.ReadOnlyField(source="agent.full_name")

    class Meta:
        model = PropertyInspection
        fields = [
            "id", "property", "property_title", "property_slug", 
            "user", "client_name", "client_email",
            "agent", "agent_name",
            "inspection_date", "inspection_time", "message", "status", "created_at"
        ]
        read_only_fields = ["user", "agent", "status"]

# apps/interactions/serializers.py (Append this)
from .models import Message, Announcement

class MessageSerializer(serializers.ModelSerializer):
    sender_name = serializers.ReadOnlyField(source="sender.full_name")
    recipient_name = serializers.ReadOnlyField(source="recipient.full_name")
    property_title = serializers.ReadOnlyField(source="property.title")

    class Meta:
        model = Message
        fields = ["id", "sender", "sender_name", "recipient", "recipient_name", "property", "property_title", "subject", "body", "is_read", "created_at"]
        read_only_fields = ["sender", "is_read"]

class AnnouncementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Announcement
        fields = ["id", "title", "body", "created_at"]