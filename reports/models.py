from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone
from cloudinary.models import CloudinaryField
import urllib.parse

User = get_user_model()


class DailyReport(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='daily_reports',
        db_index=True
    )
    name = models.CharField(
        max_length=200,
        verbose_name='Report Name',
        help_text='Give a title to your daily report'
    )
    heading = models.CharField(
        max_length=300,
        verbose_name='Report Heading',
        help_text='Brief summary of your daily report'
    )
    report_text = models.TextField(
        verbose_name='Daily Update',
        help_text='Share your daily progress and updates'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    report_date = models.DateField(
        default=timezone.now,
        db_index=True
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        db_index=True
    )
    reviewed_by = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='reviewed_reports'
    )
    review_comment = models.TextField(blank=True)

    class Meta:
        ordering = ['-report_date', '-created_at']
        verbose_name = 'Daily Report'
        verbose_name_plural = 'Daily Reports'

    def __str__(self):
        return f"{self.name} - {self.user.get_full_name()} - {self.report_date}"

    @property
    def is_today_report(self):
        return self.report_date == timezone.now().date()


class DailyReportAttachment(models.Model):
    report = models.ForeignKey(
        DailyReport,
        on_delete=models.CASCADE,
        related_name='attachments'
    )
    attached_file = CloudinaryField(
        resource_type='auto',
        folder='daily_reports/attachments',
    )
    original_filename = models.CharField(max_length=255, null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def get_download_url(self):
        """
        Returns a Cloudinary URL that forces the browser to download the file
        with the original filename.

        ✅ FIX 2: Cloudinary ignores fl_attachment as a query-string parameter.
        It must be inserted as a *transformation segment* inside the URL path,
        between the version/upload part and the public_id part.

        Correct format:
          https://res.cloudinary.com/<cloud>/raw/upload/fl_attachment:<name>/<version>/<public_id>

        We achieve this by replacing the first occurrence of "/upload/" with
        "/upload/fl_attachment:<encoded_name>/" in the raw Cloudinary URL.
        """
        if not self.attached_file:
            return None

        url = self.attached_file.url
        if url.startswith('http://'):
            url = url.replace('http://', 'https://')

        filename = self.original_filename or "download"

        # Cloudinary requires colons and slashes to be percent-encoded in the
        # fl_attachment value; use urllib.parse.quote with safe='' to be safe.
        encoded_name = urllib.parse.quote(filename, safe='')

        # Insert the transformation right after "/upload/"
        # e.g. ".../upload/v123/public_id" → ".../upload/fl_attachment:my_file.pdf/v123/public_id"
        if '/upload/' in url:
            url = url.replace('/upload/', f'/upload/fl_attachment:{encoded_name}/', 1)

        return url

    def __str__(self):
        return f"Attachment for {self.report.name}"
