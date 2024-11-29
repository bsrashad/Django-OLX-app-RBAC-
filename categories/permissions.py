from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAdminOrReadOnly(BasePermission):
    """
    Custom permission to only allow admins to edit or delete.
    """

    def has_permission(self, request, view):
        # Check if the request method is in the SAFE_METHODS (GET, HEAD, OPTIONS)
        if request.method in SAFE_METHODS:
            return True
        # Otherwise, only allow if the user is an admin
        return request.user and request.user.is_staff
