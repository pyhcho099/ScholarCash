from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Public
    path('', views.index, name='index'),
    
    # Auth
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='index'), name='logout'),
    
    # Student
    path('student/dashboard/', views.student_dashboard, name='student_dashboard'),
    path('student/buy/<int:item_id>/', views.purchase_item, name='purchase_item'),
    
    # Admin Custom Panel
    path('admin-panel/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-panel/users/', views.admin_users, name='admin_users'),
    path('admin-panel/inventory/', views.admin_inventory, name='admin_inventory'),
    path('admin-panel/logs/', views.admin_logs, name='admin_logs'),
    path('admin-panel/settings/', views.admin_settings, name='admin_settings'),
]
