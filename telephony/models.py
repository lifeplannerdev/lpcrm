from django.db import models


class VoxbayCallLog(models.Model):
    CALL_TYPE_CHOICES = [
        ('incoming', 'Incoming'),
        ('outgoing', 'Outgoing'),
    ]

    call_uuid       = models.CharField(max_length=100, null=True, blank=True, db_index=True)
    call_type       = models.CharField(max_length=10, choices=CALL_TYPE_CHOICES, null=True, blank=True)
    called_number   = models.CharField(max_length=30, null=True, blank=True)   # DID number (calledNumber)
    caller_number   = models.CharField(max_length=30, null=True, blank=True)   # Customer number (callerNumber)
    agent_number    = models.CharField(max_length=50, null=True, blank=True)   # AgentNumber / name
    extension       = models.CharField(max_length=50, null=True, blank=True)   # Source extension
    destination     = models.CharField(max_length=30, null=True, blank=True)   # Destination number
    caller_id       = models.CharField(max_length=30, null=True, blank=True)   # callerid (DID used)
    call_status             = models.CharField(max_length=20, null=True, blank=True)   # ANSWERED, BUSY, etc.
    duration                = models.IntegerField(null=True, blank=True)               # totalCallDuration / duration (seconds)
    conversation_duration   = models.IntegerField(null=True, blank=True)               # conversationDuration (seconds)
    recording_url           = models.TextField(null=True, blank=True)
    call_start              = models.DateTimeField(null=True, blank=True)
    call_end                = models.DateTimeField(null=True, blank=True)
    dtmf                = models.CharField(max_length=100, null=True, blank=True)   # DTMF input sequence
    transferred_number  = models.CharField(max_length=200, null=True, blank=True)   # transferredNumber
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes  = [
            models.Index(fields=['call_status']),
            models.Index(fields=['call_type']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        if self.call_type == 'outgoing':
            return f"OUT {self.extension} → {self.destination} [{self.call_status}]"
        return f"IN  {self.caller_number} → {self.called_number} [{self.call_status}]"