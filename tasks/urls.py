from django.urls import path
from . import views

app_name = 'tasks'

urlpatterns = [
    path('business-head/', views.business_head_dashboard, name='business_head_dashboard'),
    path('create/', views.create_task, name='create_task'),
    path('my-tasks/', views.my_tasks, name='my_tasks'),
    path('<int:task_id>/update-status/', views.update_task_status, name='update_task_status'),
    path('<int:task_id>/', views.task_detail, name='task_detail'),
    path('<int:task_id>/delete/', views.delete_task, name='delete_task'),
]