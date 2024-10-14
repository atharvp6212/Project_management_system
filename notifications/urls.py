from django.urls import path
from .views import send_notification, group_chat

urlpatterns = [
    path('send/<int:group_id>/', send_notification, name='send_notification'), 
    path('group/<int:group_id>/chat/', group_chat, name='group_chat'),
]