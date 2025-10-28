from django.urls import path, include
from django.http import JsonResponse

def health(_):
    return JsonResponse({'status':'ok'})

urlpatterns = [
    path('health/', health),
    path('api/auth/', include('accounts.urls')),
    path('api/admin/', include('access.urls')),
    path('api/resources/', include('resources.urls')),
]
