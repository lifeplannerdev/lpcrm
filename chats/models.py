from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


class Conversation(models.Model):
    CONVERSATION_TYPE = (
        ("DIRECT", "Direct"),
        ("GROUP", "Group"),
    )

    type = models.CharField(max_length=10, choices=CONVERSATION_TYPE)
    name = models.CharField(max_length=255, blank=True, null=True) 
    participants = models.ManyToManyField(User)
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="created_conversations"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.type} - {self.id}"


class Message(models.Model):
    conversation = models.ForeignKey(     
        Conversation,
        on_delete=models.CASCADE,
        related_name="messages"
    )
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender} → {self.conversation.id}"