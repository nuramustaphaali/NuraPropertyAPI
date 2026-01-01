# apps/users/views.py
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from .permissions import IsAgent

@api_view(['GET'])
@permission_classes([IsAgent])
def agent_only_view(request):
    return Response(
        {"message": f"Hello Agent {request.user.full_name}, you have access!"},
        status=status.HTTP_200_OK
    )