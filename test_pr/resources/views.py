from rest_framework.views import APIView
from rest_framework.response import Response
from accounts.auth import JWTAuthentication
from access.utils import authorize
from rest_framework.exceptions import PermissionDenied

PROJECTS = [
    {'id': 1, 'name': 'Alpha', 'owner_id': 1},
    {'id': 2, 'name': 'Beta',  'owner_id': 2},
]
DOCUMENTS = [
    {'id': 10, 'title': 'Spec', 'owner_id': 1},
    {'id': 11, 'title': 'Plan', 'owner_id': 2},
]

class ProjectsView(APIView):
    authentication_classes = [JWTAuthentication]
    def get(self, request):
        try:
            authorize(request.user, 'project', 'read', owner_id=None)
            return Response(PROJECTS)
        except Exception:
            own = [p for p in PROJECTS if p['owner_id'] == request.user.id]
            if own:
                authorize(request.user, 'project', 'read', owner_id=request.user.id)
                return Response(own)
            raise PermissionDenied('Forbidden')


class DocumentsView(APIView):
    authentication_classes = [JWTAuthentication]
    def get(self, request):
        try:
            authorize(request.user, 'document', 'read', owner_id=None)
            return Response(DOCUMENTS)
        except Exception:
            own = [d for d in DOCUMENTS if d['owner_id'] == request.user.id]
            if own:
                authorize(request.user, 'document', 'read', owner_id=request.user.id)
                return Response(own)
            raise PermissionDenied('Forbidden')
