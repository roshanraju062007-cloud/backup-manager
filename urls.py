from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),

    # API endpoints
    path('api/login/', views.login_view, name='api_login'),
    path('api/files/', views.api_list_files, name='api_list_files'),
    path('api/files/upload/', views.api_upload_file, name='api_upload_file'),
    path('api/files/<int:pk>/delete/', views.api_delete_file, name='api_delete_file'),
]
