from django.db import models
from django.conf import settings  # Import settings to access AUTH_USER_MODEL

class Group(models.Model):
    name = models.CharField(max_length=100)
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='student_groups')  # Change related_name to avoid clash
    mentor = models.ForeignKey('accounts.TeacherProfile', on_delete=models.SET_NULL, null=True)  # Ensure correct reference

    def __str__(self):
        return self.name