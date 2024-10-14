from django.contrib import admin
from .models import Task
from projects.models import Project  # Adjust according to your models

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('name', 'group', 'due_date', 'status')  # Customize fields as needed
