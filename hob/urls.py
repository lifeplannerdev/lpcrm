from django.urls import path
from . import views

app_name = 'hob'

urlpatterns = [
    path('', views.hob_dashboard, name='dashboard'),
    path('overview/', views.overview_tab, name='overview_tab'),
    path('leads/', views.leads_tab, name='leads_tab'),
    path('staff/', views.staff_tab, name='staff_tab'),
    path('tasks/', views.tasks_tab, name='tasks_tab'),
    path('reports/', views.reports_tab, name='reports_tab'),
    path('search/', views.search_data, name='search_data'),
    path('tasks/create/', views.create_task, name='create_task'),
    path('tasks/<int:task_id>/delete/', views.delete_task, name='delete_task'),
]