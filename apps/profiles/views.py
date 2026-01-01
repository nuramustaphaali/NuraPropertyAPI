# apps/profiles/views.py
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Profile
from .serializers import ProfileSerializer, UpdateProfileSerializer

class GetMyProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        user_profile = Profile.objects.get(user=user)
        serializer = ProfileSerializer(user_profile, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)

class UpdateProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request):
        user = request.user
        user_profile = Profile.objects.get(user=user)
        serializer = UpdateProfileSerializer(user_profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AgentListAPIView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Profile.objects.filter(is_agent=True)
    serializer_class = ProfileSerializer