# apps/interactions/views.py
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import PropertyInspection
from .serializers import InspectionSerializer
from apps.properties.models import Property
from drf_spectacular.utils import extend_schema


@extend_schema(tags=['Interactions'])
class ScheduleInspectionView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        data = request.data
        property_id = data.get("property_id")
        inspection_date = data.get("inspection_date")
        inspection_time = data.get("inspection_time")
        message = data.get("message", "")

        try:
            property_obj = Property.objects.get(id=property_id)
        except Property.DoesNotExist:
            return Response({"error": "Property not found"}, status=status.HTTP_404_NOT_FOUND)

        # Prevent agent from booking their own property
        if property_obj.user == request.user:
            return Response({"error": "You cannot book an inspection for your own property"}, status=status.HTTP_400_BAD_REQUEST)

        inspection = PropertyInspection.objects.create(
            user=request.user,
            property=property_obj,
            agent=property_obj.user, # The agent is the property owner
            inspection_date=inspection_date,
            inspection_time=inspection_time,
            message=message
        )
        
        serializer = InspectionSerializer(inspection)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

@extend_schema(tags=['Interactions'])
class MyInspectionsListView(generics.ListAPIView):
    """
    Returns inspections where the user is EITHER the client OR the agent.
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = InspectionSerializer

    def get_queryset(self):
        user = self.request.user
        # If I am the agent, show me who is coming. If I am the client, show me where I am going.
        return PropertyInspection.objects.filter(models.Q(user=user) | models.Q(agent=user))

from django.db import models # Need to import Q for the query above to work

@extend_schema(tags=['Interactions'])
class ManageInspectionView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, id):
        inspection = get_object_or_404(PropertyInspection, id=id)
        
        # Only the Agent (owner) can approve/reject
        if request.user != inspection.agent:
             return Response({"error": "Only the assigned agent can manage this request"}, status=status.HTTP_403_FORBIDDEN)

        status_update = request.data.get("status")
        if status_update not in ["CONFIRMED", "REJECTED", "COMPLETED", "CANCELLED"]:
             return Response({"error": "Invalid status"}, status=status.HTTP_400_BAD_REQUEST)

        inspection.status = status_update
        inspection.save()
        
        return Response({"message": f"Inspection status updated to {status_update}"}, status=status.HTTP_200_OK)

# apps/interactions/views.py (Append this)
from .models import Message, Announcement
from .serializers import MessageSerializer, AnnouncementSerializer

# --- Messaging Views ---

@extend_schema(tags=['Interactions'])
class SendMessageView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        data = request.data
        # Auto-assign sender
        serializer = MessageSerializer(data=data)
        if serializer.is_valid():
            serializer.save(sender=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
@extend_schema(tags=['Interactions'])
class InboxListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = MessageSerializer

    def get_queryset(self):
        # Return messages where I am the recipient
        return Message.objects.filter(recipient=self.request.user)

@extend_schema(tags=['Interactions'])
class MarkMessageReadView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, id):
        message = get_object_or_404(Message, id=id)
        if message.recipient != request.user:
            return Response({"error": "Not your message"}, status=status.HTTP_403_FORBIDDEN)
        
        message.is_read = True
        message.save()
        return Response({"message": "Marked as read"}, status=status.HTTP_200_OK)

# --- Announcement Views ---

@extend_schema(tags=['Interactions'])
class AnnouncementListView(generics.ListCreateAPIView):
    queryset = Announcement.objects.filter(is_active=True)
    serializer_class = AnnouncementSerializer
    permission_classes = [permissions.IsAuthenticated] # Or AllowAny if public

    def perform_create(self, serializer):
        # Only admins can create announcements
        if not self.request.user.is_superuser:
            raise permissions.PermissionDenied("Only admins can create announcements")
        serializer.save()