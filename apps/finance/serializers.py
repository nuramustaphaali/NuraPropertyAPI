# apps/finance/serializers.py
from rest_framework import serializers
from .models import Transaction

class TransactionSerializer(serializers.ModelSerializer):
    user_name = serializers.ReadOnlyField(source="user.full_name")
    property_title = serializers.ReadOnlyField(source="property.title")

    class Meta:
        model = Transaction
        fields = [
            "id", "transaction_id", "user", "user_name", 
            "property", "property_title", "amount", "currency", 
            "payment_method", "description", "status", "note", "created_at"
        ]
        read_only_fields = ["transaction_id", "status", "user"]

# apps/finance/serializers.py (Append this)
from .models import Deal

class DealSerializer(serializers.ModelSerializer):
    property_title = serializers.ReadOnlyField(source="property.title")
    agent_name = serializers.ReadOnlyField(source="agent.full_name")
    client_name = serializers.ReadOnlyField(source="client.full_name")

    class Meta:
        model = Deal
        fields = [
            "id", "property", "property_title", 
            "agent", "agent_name", 
            "client", "client_name",
            "final_price", "commission_percentage", "commission_amount", 
            "date_closed", "deal_description"
        ]
        read_only_fields = ["agent", "commission_amount", "date_closed"]
