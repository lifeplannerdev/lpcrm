from django.urls import path
from .views import (
    TrainerListCreateAPIView,
    TrainerDetailAPIView,
    StudentListCreateAPIView,
    StudentDetailAPIView,
    AttendanceListCreateAPIView,
    AttendanceDetailAPIView,
    QuickMarkAttendanceAPIView,
    AttendanceRecordsAPIView,
    ExportStudentAttendanceAPIView,
    StudentStatsAPIView,
)

app_name = 'academy'

urlpatterns = [
    path('trainers/', TrainerListCreateAPIView.as_view()),
    path('trainers/<int:pk>/', TrainerDetailAPIView.as_view()),

    path('students/stats/', StudentStatsAPIView.as_view()),
    path('students/', StudentListCreateAPIView.as_view()),
    path('students/<int:pk>/', StudentDetailAPIView.as_view()),

    path('attendance/', AttendanceListCreateAPIView.as_view()),
    path('attendance/detail/', AttendanceDetailAPIView.as_view()),
    path('attendance/quick-mark/', QuickMarkAttendanceAPIView.as_view()),
    path('students/<int:student_id>/attendance-records/', AttendanceRecordsAPIView.as_view()),
    path('students/<int:student_id>/export-attendance/', ExportStudentAttendanceAPIView.as_view()),
]
