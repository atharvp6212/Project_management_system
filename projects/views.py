from django.shortcuts import render, get_object_or_404, redirect
from .models import Project
from .forms import ProjectForm  # Assuming you have a form for Project
from django.contrib.auth.decorators import login_required

@login_required
def edit_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect('student_dashboard')  # Redirect after saving
    else:
        form = ProjectForm(instance=project)

    return render(request, 'projects/edit_project.html', {'form': form})