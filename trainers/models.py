from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator

User = get_user_model()


class Trainer(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='trainer_profile'
    )

    drive_link = models.URLField(
        blank=True,
        help_text="Link to trainer's Google Drive folder"
    )

    STATUS_CHOICES = [
        ('ACTIVE', 'Active'),
        ('ON_LEAVE', 'On Leave'),
        ('INACTIVE', 'Inactive'),
    ]

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='ACTIVE'
    )

    def __str__(self):
        return self.user.get_full_name() or self.user.username


class Student(models.Model):
    BATCH_CHOICES = [
        ('A1', 'A1 (Beginner)'),
        ('A2', 'A2 (Elementary)'),
        ('B1', 'B1 (Intermediate)'),
        ('B2', 'B2 (Upper Intermediate)'),
        ('A1 ONLINE', 'A1 (Online)'),
        ('A2 ONLINE', 'A2 (Online)'),
        ('B1 ONLINE', 'B1 (Online)'),
        ('B2 ONLINE', 'B2 (Online)'),
        ('ONLINE', 'Online'),
        ('A1 EXAM PREPERATION', 'A1 (Exam Preparation)'),
        ('A2 EXAM PREPERATION', 'A2 (Exam Preparation)'),
        ('B1 EXAM PREPERATION', 'B1 (Exam Preparation)'),
        ('B2 EXAM PREPERATION', 'B2 (Exam Preparation)'),
    ]

    STATUS_CHOICES = [
        ('ACTIVE', 'Active'),
        ('PAUSED', 'Paused'),
        ('COMPLETED', 'Completed'),
        ('DROPPED', 'Dropped'),
    ]

    name = models.CharField(
        max_length=100,
        validators=[MinLengthValidator(3)]
    )

    batch = models.CharField(
        max_length=200,
        choices=BATCH_CHOICES
    )

    trainer = models.ForeignKey(
        Trainer,
        on_delete=models.PROTECT,
        related_name='students'
    )

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='ACTIVE'
    )

    admission_date = models.DateField(
        help_text="Admission date"
    )

    start_date = models.DateField(
        blank=True,
        null=True,
        help_text="Course start date"
    )

    end_date = models.DateField(
        blank=True,
        null=True,
        help_text="Course end date"
    )

    notes = models.TextField(
        blank=True,
        help_text="General notes about the student"
    )

    email = models.EmailField(
        blank=True,
        null=True,
        help_text="Student's email address"
    )

    phone_number = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        help_text="Student's phone number"
    )

    drive_link = models.URLField(
        blank=True,
        null=True,
        help_text="Google Drive folder link for student materials"
    )

    # Manual entry (no choices)
    student_class = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        help_text="Class type for the student (manual entry)"
    )

    class Meta:
        ordering = ['batch', 'name']

    def __str__(self):
        return f"{self.name} ({self.get_batch_display()})"


class Attendance(models.Model):
    STATUS_CHOICES = [
        ('PRESENT', 'Present'),
        ('ABSENT', 'Absent'),
        ('NO_SESSION', 'No Session'),
    ]

    date = models.DateField()

    trainer = models.ForeignKey(
        Trainer,
        on_delete=models.CASCADE,
        related_name='attendance_records'
    )

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name='attendance_records'
    )

    status = models.CharField(
        max_length=15,
        choices=STATUS_CHOICES,
        default='PRESENT'
    )

    marked_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        unique_together = ['date', 'student']
        ordering = ['-date', 'student__name']
        indexes = [
            models.Index(fields=['date', 'trainer']),
        ]

    def __str__(self):
        return f"{self.student.name} - {self.date} - {self.status}"
