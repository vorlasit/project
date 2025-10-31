from . import views
from django.urls import path
from django.contrib.auth import views as auth_views
from .form import LoginForm  

urlpatterns = [
    
    path('registernonelog/', views.registernonelog, name='registernonelog'),
    path('select-group/<int:user_id>/', views.select_group_view, name='select_group'),
    
    path('register/', views.register_view, name='register'), 
    path('loin/', auth_views.LoginView.as_view(template_name='login.html',authentication_form=LoginForm), name='login'),
    path('edit/', views.edit_user, name='edit_user'), 
    path("settings/", views.settings_view, name="settings"),
    path('user/<int:pk>/edit/', views.edit_user_list, name='edit_user_list'), 
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('users/', views.user_list_view, name='user_list'),  
    path('groups/', views.group_list_view, name='group_list'),
    path('groups/add/', views.group_create_view, name='group_create'),
    path('groups/<int:group_id>/edit/', views.group_edit_view, name='group_edit'),
    path('groups/<int:group_id>/delete/', views.group_delete_view, name='group_delete'), 
     
 
]
 