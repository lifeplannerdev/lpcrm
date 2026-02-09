from django.contrib.auth.models import AbstractUser, Group, Permission
from django.contrib.auth import get_user_model
from django.conf import settings
from django.db import models
from django.utils import timezone
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
        ('BUSINESS_HEAD', 'Business Head'),
        ('BDM', 'Business Development Manager'),
        ('CM', 'Center Manager'),
        ('HR', 'Human Resources'),
        ('FOE', 'FOE Cum TC'),
        ('ACCOUNTS', 'Accounts'), 
    ]

    role = models.CharField(
        max_length=100,
        choices=ROLE_CHOICES,
        db_index=True
    )
    team = models.CharField(max_length=50, blank=True)
    is_active = models.BooleanField(default=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    salary = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    join_date = models.DateField(blank=True, null=True)


    # Resolve auth clashes
    groups = models.ManyToManyField(
        Group,
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name='custom_user_groups',
        related_query_name='user',
    )

    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='custom_user_permissions',
        related_query_name='user',
    )

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

    @property
    def is_business_head(self):
        return self.role == 'BUSINESS_HEAD'

    @property
    def is_cm(self):
        return self.role == 'CM'

    @property
    def is_hr(self):
        return self.role == 'HR'


class ActivityLog(models.Model):
    ACTIVITY_TYPES = [
        ('LEAD_CREATED', 'Lead Created'),
        ('STUDENT_ENROLLED', 'Student Enrolled'),
        ('TASK_COMPLETED', 'Task Completed'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,blank=True)
    activity_type = models.CharField(max_length=50,choices=ACTIVITY_TYPES)
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.description



class MicroWork(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('COMPLETED', 'Completed'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='micro_works'
    )
    job_title = models.CharField(
        max_length=200,
        verbose_name='Job Title',
        help_text='Title of the micro work'
    )
    description = models.TextField(
        verbose_name='Description',
        help_text='Detailed description of the work'
    )
    time_required = models.CharField(
        max_length=100,
        verbose_name='Time Required',
        help_text='Estimated time required (e.g., 2 hours, 30 minutes)'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='PENDING'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Micro Work'
        verbose_name_plural = 'Micro Works'

    def __str__(self):
        return f"{self.job_title} - {self.user.get_full_name()}"

    def mark_completed(self):
        self.status = 'COMPLETED'
        self.completed_at = timezone.now()
        self.save()

    @property
    def is_completed(self):
        return self.status == 'COMPLETED'

    @property
    def completion_time(self):
        if self.completed_at and self.created_at:
            return self.completed_at - self.created_at
        return None

    @property
    def created_date_display(self):
        return self.created_at.strftime('%b %d, %Y')

    @property
    def created_time_display(self):
        return self.created_at.strftime('%I:%M %p')

    @property
    def completed_date_display(self):
        if self.completed_at:
            return self.completed_at.strftime('%b %d, %Y')
        return None

    @property
    def completed_time_display(self):
        if self.completed_at:
            return self.completed_at.strftime('%I:%M %p')
        return None

