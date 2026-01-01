from django.urls import path
from .views import GetMyProfileView, UpdateProfileView, AgentListAPIView

urlpatterns = [
    path('me/', GetMyProfileView.as_view(), name='get_my_profile'),
    path('update/', UpdateProfileView.as_view(), name='update_profile'),
    path('agents/all/', AgentListAPIView.as_view(), name='all-agents'),
]