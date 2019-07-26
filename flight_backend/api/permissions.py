from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    """
    Set object level permission in order to restrict access to owners of the issue alone.
    """
    def has_object_permission(self, request, view, obj):
        if request.user == obj:
            return True
        return False
