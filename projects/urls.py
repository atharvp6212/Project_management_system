from django.urls import path
from .views import edit_project

urlpatterns = [
    path('edit/<int:project_id>/', edit_project, name='edit_project'),  # New URL pattern for editing projects
]