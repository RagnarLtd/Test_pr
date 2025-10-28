from rest_framework.permissions import BasePermission
from rest_framework.exceptions import AuthenticationFailed

class IsAuthenticated401(BasePermission):

    def has_permission(self, request, view):
        user = getattr(request, "user", None)
        if user and getattr(user, "is_authenticated", False):
            return True
        raise AuthenticationFailed('Authentication credentials were not provided.')
