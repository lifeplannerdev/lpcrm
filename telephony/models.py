from django.db import models

class CallLog(models.Model):
    call_id = models.CharField(max_length=100, unique=True)
    caller_number = models.CharField(max_length=20)
    agent_number = models.CharField(max_length=20)
    status = models.CharField(max_length=50)
    duration = models.IntegerField(null=True, blank=True)
    recording_url = models.URLField(null=True, blank=True)
    raw_data = models.JSONField(null=True, blank=True)  # store full response
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.caller_number} - {self.status}"
