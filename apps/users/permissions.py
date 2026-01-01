# apps/users/permissions.py
from rest_framework import permissions

class IsSuperUser(permissions.BasePermission):
    """
    Allows access only to superusers.
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_superuser)

class IsAgent(permissions.BasePermission):
    """
    Allows access only to Agents.
    """
    def has_permission(self, request, view):
        # We check if they are logged in AND if the is_agent flag is True
        return bool(request.user and request.user.is_authenticated and request.user.is_agent)

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` or `user` attribute.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Instance must have an attribute named `user` or `agent` (we check both to be safe)
        if hasattr(obj, 'user'):
            return obj.user == request.user
        if hasattr(obj, 'agent'):
            return obj.agent == request.user
            
        return False