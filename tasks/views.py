from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Task
from .forms import TaskForm  
from groups.models import Group  

@login_required
def manage_tasks(request):
    user = request.user
    # Get groups this student is part of
    groups = Group.objects.filter(members=user)

    # Fetch tasks for all members in the groups this student belongs to
    tasks = Task.objects.filter(group__in=groups)

    # Fetch tasks assigned specifically to the logged-in user
    user_tasks = tasks.filter(assigned_to=user)
    other_tasks = tasks.exclude(assigned_to=user)

    if request.method == 'POST':
        task_name = request.POST.get('task_name')
        task_description = request.POST.get('task_description')
        assigned_to_ids = request.POST.getlist('assigned_to')  # Get list of assigned user IDs
        due_date = request.POST.get('due_date')

        # Assuming you want to associate the task with the first group this student is part of
        group = groups.first()  # Get the first group for this student

        if group:
            # Create the task instance and save it with the associated group
            task = Task.objects.create(
                name=task_name,
                description=task_description,
                due_date=due_date,
                group=group  # Set the group here
            )
            
            # Assign members to the task
            task.assigned_to.set(assigned_to_ids)
        
        return redirect('manage_tasks')  # Redirect after saving

    return render(request, 'tasks/manage_tasks.html', {
        'user_tasks': user_tasks,
        'other_tasks': other_tasks,
        'groups': groups,
    })
    
@login_required
def change_task_status(request, task_id):
    if request.method == 'POST':
        status = request.POST.get('status')
        task = get_object_or_404(Task, id=task_id)

        # Ensure that only the assigned user can change the status
        if request.user in task.assigned_to.all():
            task.status = status
            task.save()
        
        return redirect('manage_tasks')  # Redirect back after updating status