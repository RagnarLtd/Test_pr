from rest_framework import serializers
from .models import User

class RegisterIn(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(min_length=8, max_length=128, write_only=True)
    password2 = serializers.CharField(write_only=True)
    first_name = serializers.CharField(required=False, allow_blank=True)
    last_name = serializers.CharField(required=False, allow_blank=True)

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError('Passwords do not match')
        if User.objects.filter(email=attrs['email']).exists():
            raise serializers.ValidationError('Email already registered')
        return attrs


class UserOut(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','email','first_name','last_name','is_active')


class LoginIn(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


class ProfileUpdate(serializers.Serializer):
    first_name = serializers.CharField(required=False, allow_blank=True)
    last_name = serializers.CharField(required=False, allow_blank=True)

