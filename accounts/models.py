from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.utils import timezone
from django.db import models
from cloudinary.models import CloudinaryField
import os

class User(AbstractUser):
    ROLE_CHOICES = [
        ('ADMIN', 'General Manager'),
        ('OPS', 'Operations Manager'),
        ('ADM_MANAGER', 'Admission Manager'),
        ('ADM_EXEC', 'Admission Executive'),
        ('PROCESSING', 'Processing Executive'),
        ('MEDIA', 'Media Team'),
        ('TRAINER', 'Trainer'),  
        ('BUSINESS_HEAD', 'Business Head')
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    team = models.CharField(max_length=50, blank=True)

    # Add these lines to resolve clashes
    groups = models.ManyToManyField(
        Group,
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name="custom_user_groups",  
        related_query_name="user",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name="custom_user_permissions",  
        related_query_name="user",
    )

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

    @property
    def is_business_head(self):
        return self.role == 'BUSINESS_HEAD'    




class DailyReport(models.Model):
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='daily_reports'
    )
    name = models.CharField(
        max_length=200,
        verbose_name="Report Name",
        help_text="Give a title to your daily report"
    )
    heading = models.CharField(
        max_length=300,
        verbose_name="Report Heading", 
        help_text="Brief summary of your daily report"
    )
    report_text = models.TextField(
        verbose_name="Daily Update",
        help_text="Share your daily progress and updates"
    )
    # Cloudinary field for file uploads
    attached_file = CloudinaryField(
        resource_type='auto',  # Handles any file type
        folder='daily_reports/attachments',
        null=True,
        blank=True,
        verbose_name="Attached File",
        help_text="Upload any relevant file (optional)"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    report_date = models.DateField(default=timezone.now)
    
    class Meta:
        ordering = ['-report_date', '-created_at']
        verbose_name = "Daily Report"
        verbose_name_plural = "Daily Reports"
    
    def __str__(self):
        return f"{self.name} - {self.user.get_full_name()} - {self.report_date}"
    
    @property
    def is_today_report(self):
        return self.report_date == timezone.now().date()
    
    def get_file_name(self):
        """Returns the original file name"""
        if self.attached_file:
            # Cloudinary stores original filename in metadata
            return os.path.basename(self.attached_file.public_id)
        return None