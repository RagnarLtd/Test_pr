from django.db import models

class Role(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.name


class Permission(models.Model):
    SCOPE_CHOICES = (('own','own'),('any','any'))
    resource = models.CharField(max_length=100)
    action = models.CharField(max_length=50)
    scope = models.CharField(max_length=10, choices=SCOPE_CHOICES)

    class Meta:
        unique_together = ('resource','action','scope')

    def __str__(self):
        return f"{self.resource}:{self.action}:{self.scope}"


class RolePermission(models.Model):
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('role','permission')


class UserRole(models.Model):
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user','role')


class RevokedToken(models.Model):
    jti = models.CharField(max_length=64, primary_key=True)
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    revoked_at = models.DateTimeField(auto_now_add=True)
