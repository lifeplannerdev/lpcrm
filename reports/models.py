from django.contrib.auth.models import AbstractUser, Group, Permission
from django.contrib.auth import get_user_model
from django.conf import settings
from django.db import models
from django.utils import timezone
from cloudinary.models import CloudinaryField
import os

User = get_user_model()


def report_upload_path(instance, filename):
    return os.path.join(
        'daily_reports',
        str(instance.user.id),
        filename
    )


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

    attached_file = CloudinaryField(
        resource_type='auto',
        folder='daily_reports/attachments',
        null=True,
        blank=True,
        verbose_name='Attached File',
        help_text='Upload any relevant file (optional)'
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

    def get_file_name(self):
        if self.attached_file:
            return os.path.basename(self.attached_file.public_id)
        return None

    def get_secure_file_url(self):
        if self.attached_file:
            url = self.attached_file.url
            if url.startswith('http://'):
                url = url.replace('http://', 'https://')
            return url
        return None