from django.urls import path
from .admin_views import (
    RoleView, PermissionCreateView, RolePermissionsView, UserRolesView
)

urlpatterns = [
    path('roles/', RoleView.as_view()),
    path('permissions/', PermissionCreateView.as_view()),
    path('roles/<int:role_id>/permissions/', RolePermissionsView.as_view()),
    path('users/<int:user_id>/roles/', UserRolesView.as_view()),
]
