from django.db import models
from django.conf import settings

class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # User receiving the notification
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)  # Automatically set the timestamp
    is_read = models.BooleanField(default=False)  # To track if the notification has been read
    is_chat_message = models.BooleanField(default=False)  # Flag for chat messages

    def __str__(self):
        return f'Notification for {self.user.username}: {self.message}'