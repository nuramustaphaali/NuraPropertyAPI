# apps/finance/views.py
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import Transaction
from .serializers import TransactionSerializer
from apps.users.permissions import IsAgent # Import custom permission from Phase 4
from drf_spectacular.utils import extend_schema


@extend_schema(tags=['Finance'])
class ReportPaymentView(APIView):
    """
    User submits a record of offline payment.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = TransactionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(tags=['Finance'])
class MyTransactionHistoryView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TransactionSerializer

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)

@extend_schema(tags=['Finance'])
class VerifyPaymentView(APIView):
    """
    Only Agents/Admins can mark a transaction as VERIFIED.
    """
    # Assuming IsAgent allows Agents or Superusers
    permission_classes = [permissions.IsAuthenticated, IsAgent] 

    def patch(self, request, transaction_id):
        # We find by the human-readable transaction_id (TX-...)
        transaction = get_object_or_404(Transaction, transaction_id=transaction_id)
        
        action = request.data.get("action") # "VERIFY" or "REJECT"
        note = request.data.get("note", "")

        if action == "VERIFY":
            transaction.status = Transaction.Status.VERIFIED
        elif action == "REJECT":
            transaction.status = Transaction.Status.FAILED
        else:
            return Response({"error": "Invalid action. Use VERIFY or REJECT"}, status=status.HTTP_400_BAD_REQUEST)
        
        transaction.note = note
        transaction.save()
        
        return Response({"message": f"Transaction {transaction.transaction_id} marked as {transaction.status}"}, status=status.HTTP_200_OK)

# apps/finance/views.py (Append this)
from .models import Deal
from .serializers import DealSerializer
from apps.properties.models import Property

@extend_schema(tags=['Finance'])
class CreateDealView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        data = request.data
        property_id = data.get("property")
        client_email = data.get("client_email") # We identify client by email
        
        # 1. Validate Property Ownership
        try:
            property_obj = Property.objects.get(id=property_id)
        except Property.DoesNotExist:
            return Response({"error": "Property not found"}, status=status.HTTP_404_NOT_FOUND)

        if property_obj.user != request.user:
             return Response({"error": "You can only close deals for your own properties"}, status=status.HTTP_403_FORBIDDEN)

        # 2. Find Client
        client_user = User.objects.filter(email=client_email).first()
        if not client_user:
             return Response({"error": "Client email not found in system"}, status=status.HTTP_404_NOT_FOUND)

        # 3. Create Deal
        serializer = DealSerializer(data=data)
        if serializer.is_valid():
            serializer.save(agent=request.user, client=client_user)
            
            # 4. Mark Property as Sold (Unpublished)
            property_obj.published_status = False
            property_obj.save()
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# apps/finance/views.py (Append this at the bottom)
from django.db.models import Sum, Count
from apps.properties.models import Property
from apps.users.models import User

@extend_schema(tags=['Analytics'])
class KPIAnalyticsView(APIView):
    """
    Returns high-level stats for the Admin Dashboard.
    """
    permission_classes = [permissions.IsAdminUser] # Super Admin Only

    def get(self, request):
        total_users = User.objects.count()
        total_properties = Property.objects.count()
        total_deals = Deal.objects.count()
        total_revenue = Deal.objects.aggregate(Sum('final_price'))['final_price__sum'] or 0
        total_commissions = Deal.objects.aggregate(Sum('commission_amount'))['commission_amount__sum'] or 0

        return Response({
            "total_users": total_users,
            "total_properties": total_properties,
            "total_deals_closed": total_deals,
            "total_revenue_volume": total_revenue,
            "total_commissions_generated": total_commissions
        }, status=status.HTTP_200_OK)

@extend_schema(tags=['Analytics'])
class AgentPerformanceView(APIView):
    """
    Returns stats for the currently logged-in Agent.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        my_properties = Property.objects.filter(user=user)
        
        total_listings = my_properties.count()
        total_views = my_properties.aggregate(Sum('views'))['views__sum'] or 0
        deals_closed = Deal.objects.filter(agent=user).count()
        earned_commission = Deal.objects.filter(agent=user).aggregate(Sum('commission_amount'))['commission_amount__sum'] or 0

        return Response({
            "agent_name": user.full_name,
            "total_listings": total_listings,
            "total_property_views": total_views,
            "deals_closed": deals_closed,
            "earned_commission": earned_commission
        }, status=status.HTTP_200_OK)