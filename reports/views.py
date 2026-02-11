from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils.timezone import now
from rest_framework.permissions import IsAuthenticated
from .models import DailyReport, DailyReportAttachment
from .serializers import DailyReportSerializer
from .permissions import REPORT_REVIEWERS, IsReportReviewer, IsReportOwner
from rest_framework.pagination import PageNumberPagination
from rest_framework.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
import cloudinary.utils
from django.db.models import Case, When, Value, IntegerField


class DailyReportPagination(PageNumberPagination):
    page_size = 50
    page_size_query_param = "page_size"
    max_page_size = 50


class DailyReportCreateView(generics.CreateAPIView):
    serializer_class = DailyReportSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(
            user=self.request.user,
            status="pending",
        )


class MyDailyReportsView(generics.ListAPIView):
    serializer_class = DailyReportSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = DailyReportPagination

    def get_queryset(self):
        return DailyReport.objects.filter(
            user=self.request.user
        ).prefetch_related("attachments").order_by("-report_date")


class MyDailyReportUpdateView(generics.UpdateAPIView):
    serializer_class = DailyReportSerializer
    permission_classes = [IsAuthenticated, IsReportOwner]
    queryset = DailyReport.objects.all()

    def perform_update(self, serializer):
        report = self.get_object()
        if report.status != "pending":
            raise PermissionDenied(
                "Approved or rejected reports cannot be edited."
            )
        serializer.save()


class AllDailyReportsView(generics.ListAPIView):
    serializer_class = DailyReportSerializer
    permission_classes = [IsReportReviewer]
    pagination_class = DailyReportPagination

    def get_queryset(self):
        qs = DailyReport.objects.select_related(
            "user", "reviewed_by"
        ).prefetch_related("attachments")

        status = self.request.query_params.get("status")
        user = self.request.query_params.get("user")
        date = self.request.query_params.get("date")

        if status:
            qs = qs.filter(status=status)
        if user:
            qs = qs.filter(user__id=user)
        if date:
            qs = qs.filter(report_date=date)

        # Pending first
        qs = qs.annotate(
            status_order=Case(
                When(status="pending", then=Value(0)),
                When(status="rejected", then=Value(1)),
                When(status="approved", then=Value(2)),
                default=Value(3),
                output_field=IntegerField(),
            )
        ).order_by("status_order", "-report_date", "-created_at")

        return qs


class ReviewDailyReportView(APIView):
    permission_classes = [IsReportReviewer]

    def patch(self, request, pk):
        report = get_object_or_404(DailyReport, pk=pk)

        status_value = request.data.get("status")
        comment = request.data.get("review_comment", "")

        if status_value not in ["approved", "rejected"]:
            return Response({"error": "Invalid status"}, status=400)

        report.status = status_value
        report.review_comment = comment
        report.reviewed_by = request.user
        report.save()

        serializer = DailyReportSerializer(
            report, context={"request": request}
        )
        return Response(serializer.data)


class AdminReportStatsView(APIView):
    permission_classes = [IsReportReviewer]

    def get(self, request):
        today = now()
        qs = DailyReport.objects.all()

        return Response(
            {
                "total": qs.count(),
                "today": qs.filter(report_date=today.date()).count(),
                "this_month": qs.filter(
                    report_date__year=today.year,
                    report_date__month=today.month,
                ).count(),
                "approved": qs.filter(status="approved").count(),
                "pending": qs.filter(status="pending").count(),
                "rejected": qs.filter(status="rejected").count(),
            }
        )


class DailyReportDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        report = get_object_or_404(
            DailyReport.objects.prefetch_related("attachments"), pk=pk
        )

        if (
            report.user != request.user
            and request.user.role not in REPORT_REVIEWERS
        ):
            return Response({"error": "Permission denied"}, status=403)

        serializer = DailyReportSerializer(
            report, context={"request": request}
        )
        return Response(serializer.data)


class ViewReportFileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        report = get_object_or_404(
            DailyReport.objects.prefetch_related("attachments"), pk=pk
        )

        # Permission check
        if (
            report.user != request.user
            and request.user.role not in REPORT_REVIEWERS
        ):
            return Response({"error": "Permission denied"}, status=403)

        attachments = report.attachments.all()

        if not attachments.exists():
            return Response(
                {"error": "No file attached to this report"}, status=404
            )

        attachment_data = []
        for att in attachments:
            view_url = att.attached_file.url if att.attached_file else None
            if view_url and view_url.startswith("http://"):
                view_url = view_url.replace("http://", "https://")

            attachment_data.append(
                {
                    "id": att.id,
                    "file_name": att.original_filename,
                    "view_url": view_url,
                    "download_url": att.get_download_url(),
                }
            )

        first = attachment_data[0]

        return JsonResponse(
            {
                # Legacy single-file fields (first attachment) — kept for
                # backwards compatibility with existing frontend consumers
                "file_name": first["file_name"],
                "view_url": first["view_url"],
                # New multi-attachment field
                "attachments": attachment_data,
                "report_name": report.name,
            }
        )