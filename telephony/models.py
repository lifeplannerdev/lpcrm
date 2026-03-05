from django.db import models

class VoxbayCallLog(models.Model):
    call_uuid = models.CharField(max_length=100, null=True, blank=True)
    caller_number = models.CharField(max_length=20, null=True, blank=True)
    agent_number = models.CharField(max_length=20, null=True, blank=True)
    call_status = models.CharField(max_length=50, null=True, blank=True)
    duration = models.IntegerField(null=True, blank=True)
    recording_url = models.TextField(null=True, blank=True)
    call_start = models.DateTimeField(null=True, blank=True)
    call_end = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.caller_number} - {self.call_status}"