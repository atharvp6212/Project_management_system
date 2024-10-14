from django.db import models
from django.conf import settings
from groups.models import Group  # Assuming you have a Group model

class Task(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
    ]

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    assigned_to = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='tasks')  # Assign multiple users
    group = models.ForeignKey(Group, on_delete=models.CASCADE)  # Link to Group
    due_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')  # Status field

    def __str__(self):
        return self.name