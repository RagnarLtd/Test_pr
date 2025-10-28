import os, time, uuid, jwt
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from accounts.models import User
from access.models import RevokedToken

JWT_SECRET = os.getenv('JWT_SECRET','dev')
JWT_ALG = os.getenv('JWT_ALG','HS256')
ACCESS_TTL_MIN = int(os.getenv('ACCESS_TTL_MIN','30'))
REFRESH_TTL_DAYS = int(os.getenv('REFRESH_TTL_DAYS','7'))


class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth = request.META.get('HTTP_AUTHORIZATION','')
        if not auth.startswith('Bearer '):
            return None
        token = auth.split(' ',1)[1]
        try:
            payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALG])
        except Exception:
            raise AuthenticationFailed('Invalid token')
        if RevokedToken.objects.filter(pk=payload.get('jti','')).exists():
            raise AuthenticationFailed('Token revoked')
        try:
            user = User.objects.get(pk=int(payload['sub']))
        except Exception:
            raise AuthenticationFailed('User not found')
        if not user.is_active:
            raise AuthenticationFailed('Inactive user')
        return (user, None)

    def authenticate_header(self, request):
        return 'Bearer'


def _encode(payload: dict, ttl_seconds: int) -> str:
    now = int(time.time())
    payload = { **payload, 'date': now, 'exp': now+ttl_seconds, 'jti': uuid.uuid4().hex }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALG)


def create_access_token(user_id: int) -> str:
    return _encode({'sub': str(user_id), 'typ': 'access'}, ACCESS_TTL_MIN*60)


def create_refresh_token(user_id: int) -> str:
    return _encode({'sub': str(user_id), 'typ': 'refresh'}, REFRESH_TTL_DAYS*86400)
