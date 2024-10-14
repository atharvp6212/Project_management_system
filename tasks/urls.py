from django.urls import path
from .views import manage_tasks, change_task_status

urlpatterns = [
    path('manage/', manage_tasks, name='manage_tasks'),  # New URL pattern for managing tasks
    path('change-status/<int:task_id>/', change_task_status, name='change_task_status'),
]