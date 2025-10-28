
from accounts.models import User
from access.models import Role, Permission, RolePermission, UserRole

def bootstrap_rbac():
    admin = Role.objects.get_or_create(name='admin', defaults={'description':'Administrator'})[0]
    manager = Role.objects.get_or_create(name='manager')[0]
    viewer = Role.objects.get_or_create(name='viewer')[0]

    perms = [
        ('project','read','any'),
        ('project','create','any'),
        ('project','update','own'),
        ('project','delete','own'),
        ('document','read','own'),
        ('document','read','any'),
    ]
    perm_objs = []
    for r,a,s in perms:
        perm_objs.append(Permission.objects.get_or_create(resource=r, action=a, scope=s)[0])

    for p in perm_objs:
        RolePermission.objects.get_or_create(role=admin, permission=p)

    for p in perm_objs:
        if p.resource=='project' and ((p.action in ('read','create') and p.scope=='any') or p.scope=='own'):
            RolePermission.objects.get_or_create(role=manager, permission=p)
        if p.resource=='document' and p.action=='read' and p.scope=='own':
            RolePermission.objects.get_or_create(role=manager, permission=p)

    for p in perm_objs:
        if p.resource=='document' and p.action=='read' and p.scope=='any':
            RolePermission.objects.get_or_create(role=viewer, permission=p)

    return admin, manager, viewer


def create_user(email, password, first_name='Test'):
    u = User.objects.create(email=email, first_name=first_name)
    u.set_password(password)
    u.save()
    return u
