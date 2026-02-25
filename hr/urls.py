from django.urls import path
from .views import (
    PenaltyListCreateAPI, 
    PenaltyDetailAPI, 
    AttendanceDocumentAPI, 
    AttendanceDocumentDeleteAPI,
    StaffListAPI,
    StaffDetailAPI
)

urlpatterns = [
    path("penalties/", PenaltyListCreateAPI.as_view(), name="penalty-list-create"),
    path("penalties/<int:pk>/", PenaltyDetailAPI.as_view(), name="penalty-detail"),
    path("attendance/", AttendanceDocumentAPI.as_view(), name="attendance-list-create"),
    path("attendance/<int:pk>/", AttendanceDocumentDeleteAPI.as_view(), name="attendance-detail"),
    path("staffs/", StaffListAPI.as_view(), name="staff-list"),
    path("staffs/<int:pk>/", StaffDetailAPI.as_view(), name="staff-detail"),
]
