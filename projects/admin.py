from django.contrib import admin
from .models import Project  # Import your Project model

@admin.register(Project)  # Register the Project model
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'group')  # Customize what fields to display in the admin list view
    search_fields = ('name', 'description')  # Enable searching by project name or description