from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from .forms import UserRegistrationForm, StudentProfileForm, TeacherProfileForm
from django.contrib.auth import authenticate, login as auth_login
from .models import StudentProfile, TeacherProfile, User
from django.contrib.auth.decorators import login_required
from groups.models import Group
from projects.models import Project
from tasks.models import Task
from .forms import UserProfileForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash

def landing_page(request):
    return render(request, 'accounts/landing_page.html')

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            
            # Create profile based on role
            if user.role == 'student':
                StudentProfile.objects.create(user=user)
            elif user.role == 'teacher':
                TeacherProfile.objects.create(user=user)

            login(request, user)
            return redirect('landing_page')  
    else:
        form = UserRegistrationForm()
    
    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            auth_login(request, user)
            if user.role == 'admin':
                return redirect('admin_dashboard')
            elif user.role == 'student':
                return redirect('student_dashboard')
            elif user.role == 'teacher':
                return redirect('teacher_dashboard')
    
    return render(request, 'accounts/login.html')

@login_required
def admin_dashboard(request):
    # Logic for admin dashboard (e.g., display user statistics, manage groups)
    return render(request, 'accounts/admin_dashboard.html')

@login_required
def student_dashboard(request):
    user = request.user
    student_profile = get_object_or_404(StudentProfile, user=user)
    
    # Get the groups this student is part of
    groups = Group.objects.filter(members=user)

    # Initialize project info and tasks
    projects = []
    tasks = Task.objects.filter(assigned_to=user)  # Fetch tasks assigned to this student
    
    for group in groups:
        project = Project.objects.filter(group=group).first()  # Get the first project for each group
        if project:
            projects.append(project)

    if request.method == 'POST':
        project_name = request.POST.get('project_name')
        project_description = request.POST.get('project_description')
        
        if groups.exists():
            group = groups.first()
            Project.objects.create(name=project_name, description=project_description, group=group)
            return redirect('student_dashboard')  # Redirect after saving

    return render(request, 'accounts/student_dashboard.html', {
        'user': user,
        'student_profile': student_profile,
        'groups': groups,
        'projects': projects,
        'tasks': tasks,  # Pass tasks to the template
    })

@login_required
def teacher_dashboard(request):
    user = request.user
    # Fetch groups where the teacher is assigned as a mentor
    groups = Group.objects.filter(mentor__user=user)

    return render(request, 'accounts/teacher_dashboard.html', {
        'user': user,
        'groups': groups,
    })

@login_required
def group_details(request, group_id):
    group = get_object_or_404(Group, id=group_id)

    # Fetch additional information related to the group if needed
    projects = group.project_set.all()  # Assuming there is a related project model
    tasks = group.task_set.all()  # Assuming there is a related task model

    return render(request, 'accounts/group_details.html', {
        'group': group,
        'projects': projects,
        'tasks': tasks,
    })

@login_required
def custom_logout(request):
    logout(request)  # Log out the user
    return redirect('landing_page')

@login_required
def create_user(request):
    if request.method == 'POST':
        role = request.POST.get('role')
        unique_id = request.POST.get('unique_id')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Create user
        user = User.objects.create_user(username=username, email=email, password=password, role=role)

        # Create profile based on role
        if role == 'student':
            StudentProfile.objects.create(user=user, major=unique_id)  # Assuming unique_id is stored as major
        elif role == 'teacher':
            TeacherProfile.objects.create(user=user, department=unique_id)  # Assuming unique_id is stored as department

        return redirect('admin_dashboard')  # Redirect to dashboard after creation

    return render(request, 'accounts/create_user.html')

@login_required
def view_students(request):
    students = User.objects.filter(role='student')
    return render(request, 'accounts/view_students.html', {'students': students})

@login_required
def view_teachers(request):
    teachers = User.objects.filter(role='teacher')
    return render(request, 'accounts/view_teachers.html', {'teachers': teachers})

@login_required
def edit_user(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        user.username = request.POST.get('username')
        user.email = request.POST.get('email')
        user.set_password(request.POST.get('password'))  # Optional: If you want to allow password changes
        user.save()

        # Update profile if necessary
        if user.role == 'student':
            student_profile = get_object_or_404(StudentProfile, user=user)
            student_profile.major = request.POST.get('unique_id')  # Assuming unique_id is stored as major
            student_profile.save()
        elif user.role == 'teacher':
            teacher_profile = get_object_or_404(TeacherProfile, user=user)
            teacher_profile.department = request.POST.get('unique_id')  # Assuming unique_id is stored as department
            teacher_profile.save()

        return redirect('admin_dashboard')

    return render(request, 'accounts/edit_user.html', {'user': user})

@login_required
def profile_management(request):
    user = request.user
    
    if request.method == 'POST':
        # Handle user info update
        if 'update_info' in request.POST:
            user_form = UserProfileForm(request.POST, instance=user)
            if user_form.is_valid():
                user_form.save()  # Save updated user info
                messages.success(request, 'Your profile information was successfully updated!')
                return redirect('profile_management')
            else:
                messages.error(request, 'Please correct the error below.')

        # Handle password change
        elif 'change_password' in request.POST:
            password_form = PasswordChangeForm(request.user, request.POST)
            if password_form.is_valid():
                user = password_form.save()  # Save updated password
                update_session_auth_hash(request, user)  # Important for keeping the user logged in
                messages.success(request, 'Your password was successfully updated!')
                return redirect('profile_management')
            else:
                messages.error(request, 'Please correct the error below.')

    else:
        user_form = UserProfileForm(instance=user)  # Pre-fill form with current data
        password_form = PasswordChangeForm(request.user)  # Form for changing password

    return render(request, 'accounts/profile_management.html', {
        'user_form': user_form,
        'password_form': password_form,
    })