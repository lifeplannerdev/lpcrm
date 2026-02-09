from rest_framework import serializers
from .models import DailyReport

#  Daily Report Serializer
class DailyReportSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source="user.get_full_name", read_only=True)
    file_url = serializers.SerializerMethodField()
    view_url = serializers.SerializerMethodField()  # NEW: Add view URL
    reviewed_by_name = serializers.CharField(source="reviewed_by.get_full_name", read_only=True)
    
    class Meta:
        model = DailyReport
        fields = [
            "id",
            "user",
            "user_name",
            "name",
            "heading",
            "report_text",
            "attached_file",
            "file_url",
            "view_url",  # NEW: Add to fields
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
    
    def get_file_url(self, obj):
        """URL for downloading the file"""
        request = self.context.get("request")
        if obj.attached_file and request:
            return request.build_absolute_uri(obj.attached_file.url)
        return None
    
    def get_view_url(self, obj):
        """URL for viewing the file inline (NEW METHOD)"""
        request = self.context.get("request")
        if obj.attached_file and request:
            # Build URL to the view-file endpoint
            from django.urls import reverse
            view_path = reverse('view-report-file', kwargs={'pk': obj.id})
            return request.build_absolute_uri(view_path)
        return None
