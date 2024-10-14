from django.urls import path
from .views import landing_page, register, login_view, admin_dashboard, student_dashboard, teacher_dashboard, create_user, view_students, view_teachers, edit_user, custom_logout, group_details, profile_management

urlpatterns = [
    path('', landing_page, name='landing_page'),
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('admin/dashboard/', admin_dashboard, name='admin_dashboard'),
    path('student/dashboard/', student_dashboard, name='student_dashboard'),
    path('teacher/dashboard/', teacher_dashboard, name='teacher_dashboard'),
    path('admin/create-user/', create_user, name='create_user'),
    path('admin/view-students/', view_students, name='view_students'),  
    path('admin/view-teachers/', view_teachers, name='view_teachers'),  
    path('admin/edit-user/<int:user_id>/', edit_user, name='edit_user'),
    path('logout/', custom_logout, name='logout'),
    path('group/<int:group_id>/details/', group_details, name='group_details'),
    path('profile/', profile_management, name='profile_management'),
]