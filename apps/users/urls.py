# apps/users/urls.py
from django.urls import path
from .views import agent_only_view

urlpatterns = [
    path('test-agent/', agent_only_view, name='test-agent'),
]