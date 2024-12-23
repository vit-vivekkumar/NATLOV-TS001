from rest_framework.permissions import BasePermission


class IsAdminOrReadOnly(BasePermission):
    """
    Custom permission to allow only admin users to edit, others can only read.
    """

    def has_permission(self, request, view):
        # SAFE_METHODS = GET, HEAD, OPTIONS
        if request.method in ("GET", "HEAD", "OPTIONS"):
            return True
        # Allow only admin users to modify
        return request.user and request.user.is_staff
