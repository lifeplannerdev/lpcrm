from django.urls import path
from . import views

app_name = 'tasks'

urlpatterns = [
    
    path('my-tasks/', views.my_tasks, name='my_tasks'),
    path('my-tasks-ajax/', views.my_tasks_ajax, name='my_tasks_ajax'),
    path('<int:task_id>/update-status/', views.update_task_status, name='update_task_status'),
    path('<int:task_id>/', views.task_detail, name='task_detail'),
    
]