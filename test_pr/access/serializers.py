from rest_framework import serializers
from .models import Role, Permission

class RoleIn(serializers.ModelSerializer):

    class Meta:
        model = Role
        fields = ('name','description')


class PermissionIn(serializers.ModelSerializer):

    class Meta:
        model = Permission
        fields = ('resource','action','scope')
