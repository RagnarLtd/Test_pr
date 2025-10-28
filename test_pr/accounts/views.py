from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.db import transaction
from .models import User
from .serializers import RegisterIn, LoginIn, UserOut, ProfileUpdate
from .auth import create_access_token, create_refresh_token, JWTAuthentication
from access.models import RevokedToken
from accounts.permissions import IsAuthenticated401
import jwt, os

class RegisterView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        ser = RegisterIn(data=request.data)
        ser.is_valid(raise_exception=True)
        data = ser.validated_data
        with transaction.atomic():
            u = User(email=data['email'], first_name=data.get('first_name',''), last_name=data.get('last_name',''))
            u.set_password(data['password'])
            u.save()
        return Response(UserOut(u).data)


class LoginView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        ser = LoginIn(data=request.data)
        ser.is_valid(raise_exception=True)
        email = ser.validated_data['email']
        pwd = ser.validated_data['password']
        try:
            u = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'detail':'Invalid credentials'}, status=401)
        if not u.is_active or not u.check_password(pwd):
            return Response({'detail':'Invalid credentials'}, status=401)
        return Response({
            'access_token': create_access_token(u.id),
            'refresh_token': create_refresh_token(u.id),
            'token_type': 'bearer'
        })


class LogoutView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        auth = request.META.get('HTTP_AUTHORIZATION','')
        if auth.startswith('Bearer '):
            payload = jwt.decode(auth.split(' ',1)[1],
                                 os.getenv('JWT_SECRET','dev'),
                                 algorithms=[os.getenv('JWT_ALG','HS256')])
            RevokedToken.objects.get_or_create(jti=payload.get('jti'), user=request.user)
        return Response({'ok': True})


class ProfileView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]


    def get(self, request):
        return Response(UserOut(request.user).data)


    def patch(self, request):
        ser = ProfileUpdate(data=request.data, partial=True)
        ser.is_valid(raise_exception=True)
        for k,v in ser.validated_data.items():
            setattr(request.user, k, v)
        request.user.save(update_fields=list(ser.validated_data.keys()))
        return Response(UserOut(request.user).data)


    def delete(self, request):
        request.user.is_active = False
        request.user.save(update_fields=['is_active'])
        return Response({'ok': True})
