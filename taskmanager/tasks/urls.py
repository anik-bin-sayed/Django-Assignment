from django.urls import path
from . import views

urlpatterns = [
    path('', views.task_list, name = "task_list"),
    path('create/', views.task_create, name = "task_create"),
    path('task-details/<int:id>/', views.task_details, name = "task_details"),
    path('update/<int:id>/', views.update_task, name = "update_task"),
    path('delete/<int:id>/', views.delete_task.as_view(), name = "delete_task"),

    path('profile/', views.user_profile, name = 'user_profile'),

    path('register/', views.register, name = 'register'),
    path('login/', views.user_login, name = 'login'),
    path('logout/', views.user_logout, name = 'user_logout'),
]
