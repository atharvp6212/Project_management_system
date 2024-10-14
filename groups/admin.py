from django.contrib import admin
from .models import Group

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'mentor', 'get_members')  # Add get_members to list_display
    search_fields = ('name',)

    def get_members(self, obj):
        return ", ".join([student.username for student in obj.members.all()])  # Join member usernames
    get_members.short_description = 'Members'  # Set a short description for the column header