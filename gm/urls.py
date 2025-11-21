from django.urls import path
from . import views

app_name = 'gm'

urlpatterns = [
    path('', views.gm_dashboard, name='dashboard'),
    path('overview/', views.overview_tab, name='overview_tab'),
    path('leads/', views.leads_tab, name='leads_tab'),
    path('assign-lead/', views.gm_assign_lead, name='gm_assign_lead'),
    path('staff/', views.staff_tab, name='staff_tab'),
    path('tasks/', views.tasks_tab, name='tasks_tab'),
    path('reports/', views.reports_tab, name='reports_tab'),
    path('students/', views.students_tab, name='students_tab'),
    path('assign-student/', views.gm_assign_student, name='gm_assign_student'),
    path('delete-student/', views.gm_delete_student, name='gm_delete_student'),
    path('search/', views.search_data, name='search_data'),
    path('tasks/create/', views.create_task, name='create_task'),
    path('tasks/<int:task_id>/update/', views.update_task, name='update_task'),
    path('tasks/<int:task_id>/delete/', views.delete_task, name='delete_task'),
]