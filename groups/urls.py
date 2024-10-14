from django.urls import path
from .views import create_group

urlpatterns = [
    path('create/', create_group, name='create_group'),
]