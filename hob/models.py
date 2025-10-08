from django.db import models
from django.utils import timezone
from accounts.models import User
from leads.models import Lead
from tasks.models import Task

class DailyReport(models.Model):
    """Model for daily performance reports"""
    date = models.DateField(default=timezone.now)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    
    # Lead statistics
    total_leads = models.IntegerField(default=0)
    new_leads = models.IntegerField(default=0)
    converted_leads = models.IntegerField(default=0)
    
    # Task statistics
    tasks_assigned = models.IntegerField(default=0)
    tasks_completed = models.IntegerField(default=0)
    tasks_pending = models.IntegerField(default=0)
    
    # Performance metrics
    conversion_rate = models.FloatField(default=0.0)
    average_response_time = models.DurationField(null=True, blank=True)
    
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-date']
        unique_together = ['date', 'created_by']
    
    def __str__(self):
        return f"Daily Report - {self.date} by {self.created_by.get_full_name()}"

class HOBSetting(models.Model):
    """Settings for HOB dashboard"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    dashboard_layout = models.JSONField(default=dict)
    notification_preferences = models.JSONField(default=dict)
    
    def __str__(self):
        return f"HOB Settings - {self.user.get_full_name()}"

# Create your models here.
