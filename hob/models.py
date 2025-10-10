from django.db import models
from django.utils import timezone
from accounts.models import User
from leads.models import Lead
from tasks.models import Task


class HOBSetting(models.Model):
    """Settings for HOB dashboard"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    dashboard_layout = models.JSONField(default=dict)
    notification_preferences = models.JSONField(default=dict)
    
    def __str__(self):
        return f"HOB Settings - {self.user.get_full_name()}"

# Create your models here.
