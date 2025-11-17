from django.urls import path
from .views import trainer_dashboard, StudentListView, update_student_notes, add_student

app_name = 'trainers'

urlpatterns = [
    path('dashboard/', trainer_dashboard, name='dashboard'),
    path('students/', StudentListView.as_view(), name='student_list'),
    path('update-notes/', update_student_notes, name='update_notes'),
    path('add-student/', add_student, name='add_student'),
]