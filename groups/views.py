from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import GroupCreationForm
from accounts.models import User

@login_required
def create_group(request):
    # Get previously selected members from GET
    selected_members = request.GET.getlist('selected_members')

    # Handle search query
    search_query = request.GET.get('search', '')
    if search_query:
        students = User.objects.filter(
            role='student',
            username__icontains=search_query
        ) | User.objects.filter(
            role='student',
            studentprofile__major__icontains=search_query
        )
    else:
        students = User.objects.filter(role='student')

    # Initialize the form
    if request.method == 'POST' and 'create_group' in request.POST:
        form = GroupCreationForm(request.POST)
        if form.is_valid():
            group = form.save(commit=False)
            group.save()
            group.members.set(form.cleaned_data['members'])  # Assign members
            return redirect('admin_dashboard')
    else:
        form = GroupCreationForm()  # Ensure form is available for GET requests as well

    return render(request, 'groups/create_group.html', {
        'form': form,  # Pass the form to the template
        'students': students,
        'selected_members': selected_members,
        'search_query': search_query
    })
