from rest_framework import serializers
from .models import DailyReport, DailyReportAttachment
from django.urls import reverse


class DailyReportAttachmentSerializer(serializers.ModelSerializer):
    file_url = serializers.SerializerMethodField()
    download_url = serializers.SerializerMethodField()

    class Meta:
        model = DailyReportAttachment
        fields = [
            "id",
            "attached_file",
            "file_url",
            "download_url",
            "original_filename",
            "uploaded_at",
        ]
        read_only_fields = ["uploaded_at"]

    def get_file_url(self, obj):
        """View inline (no forced download)"""
        if obj.attached_file:
            url = obj.attached_file.url
            if url.startswith("http://"):
                url = url.replace("http://", "https://")
            return url
        return None

    def get_download_url(self, obj):
        """Force download with original filename"""
        return obj.get_download_url()


class DailyReportSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source="user.get_full_name", read_only=True)
    reviewed_by_name = serializers.CharField(
        source="reviewed_by.get_full_name", read_only=True
    )
    attachments = DailyReportAttachmentSerializer(many=True, read_only=True)

    # ── Legacy single-file fields kept for backwards compatibility ──────────
    # These always return None now (fields removed from DailyReport).
    # Frontend consumers should migrate to `attachments` instead.
    file_url = serializers.SerializerMethodField()
    view_url = serializers.SerializerMethodField()

    class Meta:
        model = DailyReport
        fields = [
            "id",
            "user",
            "user_name",
            "name",
            "heading",
            "report_text",
            # legacy shims (kept so existing API consumers don't break)
            "file_url",
            "view_url",
            # new multi-attachment field
            "attachments",
            "report_date",
            "status",
            "review_comment",
            "reviewed_by",
            "reviewed_by_name",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "user",
            "status",
            "reviewed_by",
            "review_comment",
            "created_at",
            "updated_at",
        ]

    # Legacy shims — always None; kept so old clients don't crash
    def get_file_url(self, obj):
        attachments = obj.attachments.all()
        if attachments.exists():
            first = attachments.first()
            return first.get_download_url()
        return None

    def get_view_url(self, obj):
        attachments = obj.attachments.all()
        if attachments.exists():
            first = attachments.first()
            if first.attached_file:
                url = first.attached_file.url
                if url.startswith("http://"):
                    url = url.replace("http://", "https://")
                return url
        return None