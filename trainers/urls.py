from django.urls import path
from .views import trainer_dashboard, StudentListView, update_student_notes, add_student, edit_student, delete_student, delete_student2, student_details, attendance_view, get_attendance_detail, quick_mark_attendance


app_name = 'trainers'

urlpatterns = [
    path('dashboard/', trainer_dashboard, name='dashboard'),
    path('students/', StudentListView.as_view(), name='student_list'),
    path('student/<int:student_id>/', student_details, name='student_details'),
    path('update-notes/', update_student_notes, name='update_notes'),
    path('add-student/', add_student, name='add_student'),
    path('edit-student/<int:student_id>/', edit_student, name='edit_student'),
    path('delete-student/', delete_student, name='delete_student'),
    path('delete-student2/<int:student_id>/', delete_student2, name='delete_student2'),
    path('attendance/', attendance_view, name='attendance'),
    path('attendance/detail/', get_attendance_detail, name='attendance_detail'),
    path('attendance/quick-mark/', quick_mark_attendance, name='quick_mark_attendance'),
]