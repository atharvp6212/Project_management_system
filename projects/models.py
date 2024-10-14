from django.db import models
from django.conf import settings

class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    group = models.ForeignKey('groups.Group', on_delete=models.CASCADE)  # Link to Group

    def __str__(self):
        return self.name