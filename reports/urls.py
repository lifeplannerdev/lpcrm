from django.urls import path
from .views import (
    DailyReportCreateView,
    MyDailyReportsView,
    MyDailyReportUpdateView,
    AllDailyReportsView,
    ReviewDailyReportView,
    AdminReportStatsView,
    DailyReportDetailView,
    ViewReportFileView,
)

urlpatterns = [
    # ── Employee ─────────────────────────────────────────────
    path("reports/create/", DailyReportCreateView.as_view(), name="report-create"),
    path("reports/my/", MyDailyReportsView.as_view(), name="my-reports"),
    path("reports/<int:pk>/edit/", MyDailyReportUpdateView.as_view(), name="report-update"),
    path("reports/<int:pk>/", DailyReportDetailView.as_view(), name="report-detail"),

    # ── Admin ────────────────────────────────────────────────
    path("admin/reports/", AllDailyReportsView.as_view(), name="all-reports"),
    path("admin/reports/<int:pk>/review/", ReviewDailyReportView.as_view(), name="report-review"),
    path("admin/reports/stats/", AdminReportStatsView.as_view(), name="report-stats"),
    path("admin/reports/<int:pk>/view-file/", ViewReportFileView.as_view(), name="report-file"),
]
