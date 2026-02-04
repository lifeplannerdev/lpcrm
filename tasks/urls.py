from django.urls import path
from .views import (
    TaskStatsAPIView,
    EmployeeListAPIView,
    TaskListCreateAPIView,
    TaskDetailAPIView,
    TaskUpdateListCreateAPIView,
    TasksAssignedByMeAPIView,
    TaskStatusUpdateAPIView,
    UpcomingTasksAPIView
)

urlpatterns = [
    # Task Statistics
    path('tasks/stats/', TaskStatsAPIView.as_view(), name='task-stats'),
    path('employees/', EmployeeListAPIView.as_view(), name='employee-list'),
    path('tasks/', TaskListCreateAPIView.as_view(), name='task-list-create'),
    
    # Task Detail, Update, Delete
    path('tasks/<int:pk>/', TaskDetailAPIView.as_view(), name='task-detail'),
    
    # Task Updates (Activity History)
    path('tasks/<int:task_id>/updates/', TaskUpdateListCreateAPIView.as_view(), name='task-updates'),
    
    # Tasks Assigned By Me
    path('tasks/assigned-by-me/', TasksAssignedByMeAPIView.as_view(), name='tasks-assigned-by-me'),
    
    # Task Status Update (Quick status change endpoint)
    path('tasks/<int:pk>/status/', TaskStatusUpdateAPIView.as_view(), name='task-status-update'),
    
    # Upcoming Tasks
    path('upcoming/', UpcomingTasksAPIView.as_view(), name='upcoming-tasks'),
]
