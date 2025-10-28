from rest_framework.exceptions import PermissionDenied
from .models import UserRole, RolePermission

def user_permissions(user):
    rp = (RolePermission.objects
          .filter(role__in=UserRole.objects.filter(user=user).values('role_id'))
          .select_related('permission'))
    return [(x.permission.resource, x.permission.action, x.permission.scope) for x in rp]


def authorize(user, resource: str, action: str, owner_id: int | None = None):
    perms = user_permissions(user)
    if (resource, action, 'any') in perms:
        return
    if owner_id is not None and (resource, action, 'own') in perms and owner_id == user.id:
        return
    raise PermissionDenied('Forbidden')


def is_admin(user) -> bool:
    from .models import UserRole, Role
    return UserRole.objects.filter(user=user, role__name='admin').exists()
