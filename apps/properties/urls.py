# apps/properties/urls.py
from django.urls import path
from .views import (
    PropertyListAPIView, PropertyCreateAPIView, PropertyDetailView, 
    UpdatePropertyAPIView, DeletePropertyAPIView,
    SavedSearchListCreateView, SavedSearchDeleteView, 
    UploadPropertyImageView
)

urlpatterns = [
    path("all/", PropertyListAPIView.as_view(), name="all-properties"),
    path("create/", PropertyCreateAPIView.as_view(), name="property-create"),
    path("details/<slug:slug>/", PropertyDetailView.as_view(), name="property-details"),
    path("update/<slug:slug>/", UpdatePropertyAPIView.as_view(), name="property-update"),
    path("delete/<slug:slug>/", DeletePropertyAPIView.as_view(), name="property-delete"),
    path("upload-image/", UploadPropertyImageView.as_view(), name="upload-property-image"),
    path("search/saved/", SavedSearchListCreateView.as_view(), name="saved-search-list"),
    path("search/saved/<uuid:id>/", SavedSearchDeleteView.as_view(), name="saved-search-delete"),
]