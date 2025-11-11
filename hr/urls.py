from django.urls import path
from . import views

app_name = 'hr'

urlpatterns = [
    path('', views.hr_dashboard, name='dashboard'),
    path('employees/', views.employees, name='employee_list'),
    path('employees/list/', views.employees_list_partial, name='employees_list_partial'),
    path('attendance/', views.attendance_partial, name='attendance_partial'),
    path('penalties/', views.penalties_partial, name='penalties_partial'),
    path('penalties/add/', views.add_penalty, name='add_penalty'),
    path('penalties/delete/<int:penalty_id>/', views.delete_penalty, name='delete_penalty'),
    path('employees/add/', views.add_employee, name='add_employee'),
    path('employees/delete/<int:employee_id>/', views.delete_employee, name='delete_employee'),
]