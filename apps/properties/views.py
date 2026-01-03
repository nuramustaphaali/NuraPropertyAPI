# apps/properties/views.py
from rest_framework import filters, permissions, generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from .models import Property
from .serializers import PropertySerializer, PropertyCreateSerializer
#from .exceptions import PropertyNotFound # Optional custom exception
from drf_spectacular.utils import extend_schema


class PropertyPagination(PageNumberPagination):
    page_size = 10

# apps/properties/views.py
from .filters import PropertyFilter # Import the new filter
@extend_schema(tags=['Properties'])
class PropertyListAPIView(generics.ListAPIView):
    serializer_class = PropertySerializer
    queryset = Property.objects.all().order_by("-created_at")
    pagination_class = PropertyPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = PropertyFilter # <--- USE THE NEW CLASS HERE
    search_fields = ["country", "city", "street_address", "title", "description"]
    ordering_fields = ["created_at", "price"]

@extend_schema(tags=['Properties'])
class PropertyCreateAPIView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PropertyCreateSerializer

    def perform_create(self, serializer):
       # user = self.request.user
        serializer.save(user=self.request.user)

        # In a real app, you might want to log this or send a notification
@extend_schema(tags=['Properties'])
class PropertyDetailView(APIView):
    def get(self, request, slug):
        try:
            property = Property.objects.get(slug=slug)
            property.views += 1
            property.save()
            serializer = PropertySerializer(property, context={"request": request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Property.DoesNotExist:
            return Response({"error": "Property Not Found"}, status=status.HTTP_404_NOT_FOUND)

@extend_schema(tags=['Properties'])
class UpdatePropertyAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, slug):
        try:
            property = Property.objects.get(slug=slug)
            if property.user != request.user:
                return Response(
                    {"error": "You cannot edit a property that doesn't belong to you"},
                    status=status.HTTP_403_FORBIDDEN
                )
            serializer = PropertyCreateSerializer(property, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Property.DoesNotExist:
            return Response({"error": "Property Not Found"}, status=status.HTTP_404_NOT_FOUND)

@extend_schema(tags=['Properties'])
class DeletePropertyAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, slug):
        try:
            property = Property.objects.get(slug=slug)
            if property.user != request.user:
                return Response(
                    {"error": "You cannot delete a property that doesn't belong to you"},
                    status=status.HTTP_403_FORBIDDEN
                )
            property.delete()
            return Response({"message": "Property deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Property.DoesNotExist:
            return Response({"error": "Property Not Found"}, status=status.HTTP_404_NOT_FOUND)

# apps/properties/views.py
from rest_framework.parsers import MultiPartParser, FormParser
from .serializers import PropertyImageSerializer

@extend_schema(tags=['Media'])
class UploadPropertyImageView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser] # Allows file uploads

    def post(self, request):
        data = request.data
        property_id = data.get("property")
        
        # Verify ownership
        try:
            property_obj = Property.objects.get(id=property_id)
            if property_obj.user != request.user:
                return Response(
                    {"error": "You cannot add images to a property you do not own."},
                    status=status.HTTP_403_FORBIDDEN
                )
        except Property.DoesNotExist:
            return Response({"error": "Property not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = PropertyImageSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# apps/properties/views.py (add at the bottom)
from .models import PropertySearch
from .serializers import PropertySearchSerializer

@extend_schema(tags=['Properties'])
class SavedSearchListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PropertySearchSerializer

    def get_queryset(self):
        return PropertySearch.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

@extend_schema(tags=['Properties'])
class SavedSearchDeleteView(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = PropertySearch.objects.all()
    lookup_field = "id"

    def get_queryset(self):
        # Ensure user can only delete their own
        return PropertySearch.objects.filter(user=self.request.user)


