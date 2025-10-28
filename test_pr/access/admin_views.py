from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from accounts.auth import JWTAuthentication
from .serializers import RoleIn, PermissionIn
from .models import Role, Permission, RolePermission, UserRole
from .utils import is_admin
from rest_framework.exceptions import PermissionDenied


class RequireAdminMixin:
    def initial(self, request, *args, **kwargs):
        super().initial(request, *args, **kwargs)
        if not is_admin(request.user):
            raise PermissionDenied('Admins only')


class RoleView(RequireAdminMixin, APIView):
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        roles = list(Role.objects.values('id','name','description'))
        return Response(roles)


    def post(self, request):
        ser = RoleIn(data=request.data)
        ser.is_valid(raise_exception=True)
        role, created = Role.objects.get_or_create(**ser.validated_data)
        if not created:
            return Response({'detail': 'Role exists'}, status=400)
        return Response({'id': role.id, 'name': role.name})


class PermissionCreateView(RequireAdminMixin, APIView):
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        perms = list(Permission.objects.values('id','resource','action','scope'))
        return Response(perms)


    def post(self, request):
        ser = PermissionIn(data=request.data)
        ser.is_valid(raise_exception=True)
        p, created = Permission.objects.get_or_create(**ser.validated_data)
        if not created:
            return Response({'detail':'Permission exists'}, status=400)
        return Response({'id': p.id})


class RolePermissionsView(RequireAdminMixin, APIView):
    authentication_classes = [JWTAuthentication]

    def get(self, request, role_id: int):
        qs = (RolePermission.objects
              .filter(role_id=role_id)
              .select_related('permission'))
        data = [{
            'permission_id': rp.permission_id,
            'resource': rp.permission.resource,
            'action': rp.permission.action,
            'scope': rp.permission.scope,
        } for rp in qs]
        return Response({'role_id': role_id, 'permissions': data})


    def post(self, request, role_id: int):
        perm_id = request.data.get('permission_id')
        if not perm_id:
            return Response({'detail': 'permission_id required'}, status=400)
        RolePermission.objects.get_or_create(role_id=role_id, permission_id=perm_id)
        return Response({'ok': True})


class UserRolesView(RequireAdminMixin, APIView):
    authentication_classes = [JWTAuthentication]

    def get(self, request, user_id: int):
        qs = (UserRole.objects
              .filter(user_id=user_id)
              .select_related('role'))
        data = [{'role_id': ur.role_id, 'name': ur.role.name} for ur in qs]
        return Response({'user_id': user_id, 'roles': data})


    def post(self, request, user_id: int):
        role_id = request.data.get('role_id')
        if not role_id:
            return Response({'detail': 'role_id required'}, status=400)
        UserRole.objects.get_or_create(user_id=user_id, role_id=role_id)
        return Response(status=201)