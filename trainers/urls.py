from django.urls import path
from .views import (
    TrainerListCreateAPIView,
    TrainerDetailAPIView,
    TrainerUserListAPIView, 
    StudentListCreateAPIView,
    StudentDetailAPIView,
    AttendanceListCreateAPIView,
    AttendanceDetailAPIView,
    QuickMarkAttendanceAPIView,
    AttendanceRecordsAPIView,
    AttendanceStudentsAPIView, 
    ExportStudentAttendanceAPIView,
    StudentStatsAPIView,
)

urlpatterns = [
    path('trainers/', TrainerListCreateAPIView.as_view(), name='trainer-list-create'),
    path('trainers/<int:pk>/', TrainerDetailAPIView.as_view(), name='trainer-detail'),
    path('trainer-users/', TrainerUserListAPIView.as_view(), name='trainer-user-list'),
    path('students/', StudentListCreateAPIView.as_view(), name='student-list-create'),
    path('students/<int:pk>/', StudentDetailAPIView.as_view(), name='student-detail'),
    path('attendance/', AttendanceListCreateAPIView.as_view(), name='attendance-list-create'),
    path('attendance/detail/', AttendanceDetailAPIView.as_view(), name='attendance-detail'),
    path('attendance/quick-mark/', QuickMarkAttendanceAPIView.as_view(), name='attendance-quick-mark'),
    path('attendance/students/', AttendanceStudentsAPIView.as_view(), name='attendance-students'), 
    path('attendance/student/<int:student_id>/', AttendanceRecordsAPIView.as_view(), name='attendance-student-records'),
    path('attendance/export/<int:student_id>/', ExportStudentAttendanceAPIView.as_view(), name='export-student-attendance'),
    path('stats/students/', StudentStatsAPIView.as_view(), name='student-stats'),
]
