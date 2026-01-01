# apps/common/urls.py
from django.urls import path
from .views import HealthCheckAPIView

urlpatterns = [
    path('health/', HealthCheckAPIView.as_view(), name='health-check'),
]