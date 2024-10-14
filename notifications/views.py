from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Notification
from groups.models import Group  # Assuming you have a Group model

@login_required
def send_notification(request, group_id):
    group = get_object_or_404(Group, id=group_id)

    if request.method == 'POST':
        message = request.POST.get('message')

        # Send notification to all group members including the mentor
        for member in group.members.all():
            Notification.objects.create(user=member, message=f'{request.user.username}: {message}')

        # Optionally notify the mentor as well
        if group.mentor:
            Notification.objects.create(user=group.mentor.user, message=f'{request.user.username}: {message}')

        return redirect('group_chat', group_id=group.id)  # Redirect back to chat or group page

    return render(request, 'notifications/send_notification.html', {'group': group})

@login_required
def view_notifications(request):
    notifications = Notification.objects.filter(user=request.user).order_by('-timestamp')

    return render(request, 'notifications/view_notifications.html', {
        'notifications': notifications,
    })
    
@login_required
def group_chat(request, group_id):
    group = get_object_or_404(Group, id=group_id)

    # Fetch messages for this group (chat messages)
    messages = Notification.objects.filter(is_chat_message=True).filter(user__in=group.members.all()).order_by('-timestamp')

    if request.method == 'POST':
        message = request.POST.get('message')

        # Send notification to all group members including the mentor
        for member in group.members.all():
            if member != request.user:  # Prevent sending a notification to the sender
                Notification.objects.create(user=member, message=f'{request.user.username}: {message}', is_chat_message=True)

        # Optionally notify the mentor as well
        if group.mentor:
            Notification.objects.create(user=group.mentor.user, message=f'{request.user.username}: {message}', is_chat_message=True)

        return redirect('group_chat', group_id=group.id)  # Redirect back to chat page

    return render(request, 'notifications/group_chat.html', {
        'group': group,
        'messages': messages,
    })