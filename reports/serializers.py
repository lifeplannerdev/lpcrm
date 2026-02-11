from rest_framework import serializers
from .models import DailyReport, DailyReportAttachment


class DailyReportAttachmentSerializer(serializers.ModelSerializer):
    view_url = serializers.SerializerMethodField()
    download_url = serializers.SerializerMethodField()

    class Meta:
        model = DailyReportAttachment
        fields = [
            "id",
            "attached_file",
            "view_url",
            "download_url",
            "original_filename",
            "uploaded_at",
        ]
        read_only_fields = ["uploaded_at"]

    def get_view_url(self, obj):
        if obj.attached_file:
            url = obj.attached_file.url
            if url.startswith("http://"):
                url = url.replace("http://", "https://")
            return url
        return None

    def get_download_url(self, obj):
        return obj.get_download_url()


class DailyReportSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source="user.get_full_name", read_only=True)
    reviewed_by_name = serializers.CharField(
        source="reviewed_by.get_full_name", read_only=True
    )
    attachments = DailyReportAttachmentSerializer(many=True, read_only=True)
    file_url = serializers.SerializerMethodField()
    view_url = serializers.SerializerMethodField()

    class Meta:
        model = DailyReport
        fields = [
            "id", "user", "user_name", "name", "heading", "report_text",
            "file_url", "view_url",   # legacy shims kept for backwards compat
            "attachments",
            "report_date", "status", "review_comment",
            "reviewed_by", "reviewed_by_name",
            "created_at", "updated_at",
        ]
        read_only_fields = [
            "user", "status", "reviewed_by", "review_comment",
            "created_at", "updated_at",
        ]

    def get_file_url(self, obj):
        first = obj.attachments.first()
        return first.get_download_url() if first else None

    def get_view_url(self, obj):
        first = obj.attachments.first()
        if first and first.attached_file:
            url = first.attached_file.url
            return url.replace("http://", "https://") if url.startswith("http://") else url
        return None

    def _save_attachments(self, report, files):
        for file in files:
            # ✅ FIX 1: Capture the original filename BEFORE handing the file
            # object to Cloudinary. After CloudinaryField processes the upload,
            # file.name becomes the Cloudinary public_id, not the original name.
            original_name = file.name  # e.g. "my_report.pdf"

            DailyReportAttachment.objects.create(
                report=report,
                attached_file=file,          # Cloudinary upload happens here
                original_filename=original_name,  # saved before it's mutated
            )

    def create(self, validated_data):
        request = self.context.get("request")
        files = request.FILES.getlist("attached_files") if request else []
        report = DailyReport.objects.create(**validated_data)
        self._save_attachments(report, files)
        return report

    def update(self, instance, validated_data):
        request = self.context.get("request")
        files = request.FILES.getlist("attached_files") if request else []

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Append new files (existing ones are kept as-is)
        self._save_attachments(instance, files)
        return instance
