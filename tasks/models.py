from django.db import models
from django.utils import timezone
from accounts.models import User


class Task(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
        ('OVERDUE', 'Overdue'),
    ]

    PRIORITY_CHOICES = [
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium'),
        ('HIGH', 'High'),
        ('URGENT', 'Urgent'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()

    assigned_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='assigned_tasks'
    )

    assigned_to = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='tasks'
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='PENDING'
    )

    priority = models.CharField(
        max_length=20,
        choices=PRIORITY_CHOICES,
        default='MEDIUM'
    )

    deadline = models.DateField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-priority', '-created_at']
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['priority']),
            models.Index(fields=['assigned_to']),
            models.Index(fields=['deadline']),
            models.Index(fields=['assigned_to', 'status']),
            models.Index(fields=['completed_at']),
        ]

    def save(self, *args, **kwargs):
        if self.status == 'COMPLETED' and not self.completed_at:
            self.completed_at = timezone.now()
        elif self.status != 'COMPLETED':
            self.completed_at = None
        super().save(*args, **kwargs)

    @property
    def is_overdue(self):
        if self.status in ['COMPLETED', 'CANCELLED']:
            return False
        return timezone.now() > self.deadline

    @classmethod
    def update_overdue_tasks(cls):
        overdue_tasks = cls.objects.filter(
            deadline__lt=timezone.now(),
            status__in=['PENDING', 'IN_PROGRESS']
        )

        from .models import TaskUpdate

        for task in overdue_tasks:
            TaskUpdate.objects.create(
                task=task,
                updated_by=task.assigned_by,
                previous_status=task.status,
                new_status='OVERDUE',
                notes='Automatically marked as overdue'
            )
            task.status = 'OVERDUE'
            task.save(update_fields=['status', 'updated_at'])


class TaskUpdate(models.Model):
    """Model to track task status updates and notes"""
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='updates')
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE)
    previous_status = models.CharField(max_length=20, choices=Task.STATUS_CHOICES)
    new_status = models.CharField(max_length=20, choices=Task.STATUS_CHOICES)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.task.title} - {self.previous_status} → {self.new_status}"