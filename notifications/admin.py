from django.contrib import admin
from .models import Notification  # Adjust according to your models

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'timestamp', 'is_read')  # Customize fields as needed