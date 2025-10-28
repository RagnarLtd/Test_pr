import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE','test_pr.settings')
django.setup()

from accounts.models import User
from access.models import Role, Permission, RolePermission, UserRole

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

# admin
for p in perm_objs:
    RolePermission.objects.get_or_create(role=admin, permission=p)

# manager
for p in perm_objs:
    if p.resource=='project' and ((p.action in ('read','create') and p.scope=='any') or p.scope=='own'):
        RolePermission.objects.get_or_create(role=manager, permission=p)
    if p.resource=='document' and p.action=='read' and p.scope=='own':
        RolePermission.objects.get_or_create(role=manager, permission=p)

# viewer
for p in perm_objs:
    if p.resource=='document' and p.action=='read' and p.scope=='any':
        RolePermission.objects.get_or_create(role=viewer, permission=p)

if not User.objects.filter(email='admin@example.com').exists():
    u = User(email='admin@example.com', first_name='Admin'); u.set_password('Admin1234!'); u.save();
    UserRole.objects.get_or_create(user=u, role=admin)
if not User.objects.filter(email='testuser1@example.com').exists():
    u = User(email='alice@example.com', first_name='testuser1'); u.set_password('testuser1!'); u.save();
    UserRole.objects.get_or_create(user=u, role=manager)
if not User.objects.filter(email='testuser2@example.com').exists():
    u = User(email='bob@example.com', first_name='testuser2'); u.set_password('testuser2!'); u.save();
    UserRole.objects.get_or_create(user=u, role=viewer)

print("Seed done")
