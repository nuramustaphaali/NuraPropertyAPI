# apps/common/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class HealthCheckAPIView(APIView):
    """
    A simple endpoint to verify the API is running and versioning is working.
    """
    def get(self, request):
        return Response({
            "status": "success",
            "message": "NuraPropertyAPI is running smoothly.",
            "data": {
                "version": "v1",
                "region": "Nigeria",
                "currency": "NGN"
            }
        }, status=status.HTTP_200_OK)

# apps/common/views.py
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
# apps/common/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class HomeAPIView(APIView):
    """
    The Custom API Manual/Homepage
    """
    def get(self, request):
        api_manual = {
            "title": "NuraPropertyAPI Documentation",
            "description": "Welcome to the Nura Real Estate API. Below are the core endpoints available for use.",
            "version": "1.0.0",
            "endpoints": {
                "Authentication": [
                    {
                        "method": "POST",
                        "url": "/api/v1/auth/users/",
                        "action": "Register User",
                        "body": {
                            "email": "user@example.com",
                            "full_name": "John Doe",
                            "password": "strongpassword",
                            "re_password": "strongpassword",
                            "city": "Lagos",
                            "address": "123 Street"
                        }
                    },
                    {
                        "method": "POST",
                        "url": "/api/v1/auth/jwt/create/",
                        "action": "Login (Get Tokens)",
                        "body": {
                            "email": "user@example.com",
                            "password": "strongpassword"
                        }
                    }
                ],
                "Profiles": [
                    {
                        "method": "GET",
                        "url": "/api/v1/profiles/me/",
                        "action": "Get My Profile",
                        "headers": {"Authorization": "Bearer <access_token>"}
                    },
                    {
                        "method": "PATCH",
                        "url": "/api/v1/profiles/update/",
                        "action": "Update Profile",
                        "headers": {"Authorization": "Bearer <access_token>"},
                        "body": {
                            "phone_number": "+2348012345678",
                            "about_me": "Experienced Agent",
                            "city": "Abuja"
                        }
                    },
                    {
                        "method": "GET",
                        "url": "/api/v1/profiles/agents/all/",
                        "action": "List All Agents",
                        "headers": {"Authorization": "Bearer <access_token>"}
                    }
                ],
                "Properties": [
                    {
                        "method": "GET",
                        "url": "/api/v1/properties/all/",
                        "action": "List All Properties",
                        "query_params": "?price=100000&city=Lagos&advert_type=FOR_SALE&property_type=HOUSE"
                    },
                    {
                        "method": "POST",
                        "url": "/api/v1/properties/create/",
                        "action": "Create Property (Full)",
                        "headers": {
                            "Authorization": "Bearer <access_token>",
                            "Content-Type": "multipart/form-data" 
                        },
                        "body": {
                            "title": "Luxury Duplex in Lekki Phase 1",
                            "description": "A newly built 5 bedroom detached duplex...",
                            "price": 85000000.00,
                            "advert_type": "FOR_SALE", 
                            "property_type": "HOUSE",
                            "country": "Nigeria",
                            "city": "Lagos",
                            "street_address": "Admiralty Way",
                            "property_number": 12,
                            "postal_code": "105102",
                            "plot_area": 600.50,
                            "total_floors": 2,
                            "bedrooms": 5,
                            "bathrooms": 6.0,
                            "cover_photo": "(File Upload)",
                            "published_status": True
                        },
                        "note": "Use 'multipart/form-data' if uploading cover_photo, otherwise JSON is fine."
                    },
                    {
                        "method": "GET",
                        "url": "/api/v1/properties/details/<slug>/",
                        "action": "Get Property Detail",
                        "example_url": "/api/v1/properties/details/luxury-duplex-in-lekki-phase-1/"
                    },
                    {
                        "method": "PUT",
                        "url": "/api/v1/properties/update/<slug>/",
                        "action": "Update Property",
                        "headers": {"Authorization": "Bearer <access_token>"},
                        "body": {
                            "price": 90000000.00,
                            "title": "Updated Title",
                            "description": "Updated description"
                        }
                    },
                    {
                        "method": "DELETE",
                        "url": "/api/v1/properties/delete/<slug>/",
                        "action": "Delete Property",
                        "headers": {"Authorization": "Bearer <access_token>"}
                    },
                    {
                        "method": "POST",
                        "url": "/api/v1/properties/upload-image/",
                        "action": "Upload Gallery Image (Extra Photos)",
                        "headers": {
                            "Authorization": "Bearer <access_token>",
                            "Content-Type": "multipart/form-data"
                        },
                        "body": {
                            "property": "<property_id_uuid>",
                            "image": "(File Upload)"
                        }
                    }
                ],

                "Search & Discovery": [
                    {
                        "method": "GET",
                        "url": "/api/v1/properties/all/",
                        "action": "Advanced Search (Filtering)",
                        "query_params": "?city=Lagos&price_min=5000000&price_max=100000000&bedrooms_min=3&property_type=HOUSE",
                        "note": "Filters: price_min, price_max, bedrooms_min, city (partial match), advert_type"
                    },
                    {
                        "method": "GET",
                        "url": "/api/v1/properties/all/",
                        "action": "Global Search (Text)",
                        "query_params": "?search=Lekki",
                        "note": "Searches title, description, address, country"
                    },
                    {
                        "method": "POST",
                        "url": "/api/v1/properties/search/saved/",
                        "action": "Save a Search",
                        "headers": {"Authorization": "Bearer <access_token>"},
                        "body": {
                            "title": "My Dream House",
                            "criteria": {"city": "Lagos", "price_max": 50000000}
                        }
                    },
                    {
                        "method": "GET",
                        "url": "/api/v1/properties/search/saved/",
                        "action": "List My Saved Searches",
                        "headers": {"Authorization": "Bearer <access_token>"}
                    },
                    {
                        "method": "DELETE",
                        "url": "/api/v1/properties/search/saved/<uuid>/",
                        "action": "Delete Saved Search",
                        "headers": {"Authorization": "Bearer <access_token>"}
                    }
                ],

                "Scheduling & Appointments": [
                    {
                        "method": "POST",
                        "url": "/api/v1/interactions/schedule/",
                        "action": "Request Property Inspection",
                        "headers": {"Authorization": "Bearer <access_token>"},
                        "body": {
                            "property_id": "<property_uuid>",
                            "inspection_date": "2026-02-15",
                            "inspection_time": "14:30:00",
                            "message": "I'm available all afternoon."
                        }
                    },
                    {
                        "method": "GET",
                        "url": "/api/v1/interactions/my-inspections/",
                        "action": "List My Appointments (Agent or Client)",
                        "headers": {"Authorization": "Bearer <access_token>"},
                        "note": "Returns list of incoming requests (if Agent) or outgoing requests (if Client)"
                    },
                    {
                        "method": "PATCH",
                        "url": "/api/v1/interactions/manage/<inspection_id_uuid>/",
                        "action": "Approve/Reject Inspection (Agent Only)",
                        "headers": {"Authorization": "Bearer <access_token>"},
                        "body": {
                            "status": "CONFIRMED" 
                        },
                        "note": "Valid statuses: CONFIRMED, REJECTED, CANCELLED, COMPLETED"
                    }
                ],
                "Communication & Messaging": [
                    {
                        "method": "POST",
                        "url": "/api/v1/interactions/messages/send/",
                        "action": "Send Private Message",
                        "headers": {"Authorization": "Bearer <access_token>"},
                        "body": {
                            "recipient": "<user_uuid>",
                            "subject": "Inquiry about Lekki House",
                            "body": "Is the price negotiable?",
                            "property": "<property_uuid> (Optional)"
                        }
                    },
                    {
                        "method": "GET",
                        "url": "/api/v1/interactions/messages/inbox/",
                        "action": "Check My Inbox",
                        "headers": {"Authorization": "Bearer <access_token>"}
                    },
                    {
                        "method": "PATCH",
                        "url": "/api/v1/interactions/messages/read/<message_uuid>/",
                        "action": "Mark Message as Read",
                        "headers": {"Authorization": "Bearer <access_token>"}
                    },
                    {
                        "method": "GET",
                        "url": "/api/v1/interactions/announcements/",
                        "action": "View Admin Announcements",
                        "headers": {"Authorization": "Bearer <access_token>"}
                    }
                ]
            },
            "official_docs": {
                "swagger": "/api/docs/",
                "redoc": "/api/redoc/"
            }
        }
        return Response(api_manual, status=status.HTTP_200_OK)