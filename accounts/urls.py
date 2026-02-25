# accounts/urls.py
from django.urls import path
from .views import (
    RegisterAPIView,
    LoginAPIView,
    RefreshTokenAPIView,
    LogoutAPIView,
    CurrentUserAPIView,  # ✅ NEW
    DashboardStatsAPIView,
    RecentActivitiesAPIView,
    StaffListView,
    StaffDetailView,
    StaffCreateView,
    StaffUpdateView,
    StaffDeleteView,
    StaffByTeamView,
)

urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('token/refresh/', RefreshTokenAPIView.as_view(), name='token_refresh'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
    path('user/me/', CurrentUserAPIView.as_view(), name='current_user'),
    path('stats/', DashboardStatsAPIView.as_view(), name='dashboard_stats'),
    path('activities/', RecentActivitiesAPIView.as_view(), name='recent_activities'),
    path('staff/', StaffListView.as_view(), name='staff_list'),
    path('staff/<int:pk>/', StaffDetailView.as_view(), name='staff_detail'),
    path('staff/create/', StaffCreateView.as_view(), name='staff_create'),
    path('staff/<int:pk>/update/', StaffUpdateView.as_view(), name='staff_update'),
    path('staff/<int:pk>/delete/', StaffDeleteView.as_view(), name='staff_delete'),
    path('staff/by-team/', StaffByTeamView.as_view(), name='staff_by_team'),
]