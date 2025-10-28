from django.urls import path
from .views import ProjectsView, DocumentsView

urlpatterns = [
    path('projects/', ProjectsView.as_view()),
    path('documents/', DocumentsView.as_view()),
]
