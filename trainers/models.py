from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator

User = get_user_model()

class Trainer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='trainer_profile')
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
        return f"{self.user.get_full_name() or self.user.username}"

class Student(models.Model):
    BATCH_CHOICES = [
        ('A1', 'A1 (Beginner)'),
        ('A2', 'A2 (Elementary)'),
        ('B1', 'B1 (Intermediate)'),
        ('B2', 'B2 (Upper Intermediate)'),
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
        max_length=2,
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
    admission_date = models.DateField()
    notes = models.TextField(
        blank=True,
        help_text="General notes about the student"
    )
    
    class Meta:
        ordering = ['batch', 'name']
    
    def __str__(self):
        return f"{self.name} ({self.get_batch_display()})"