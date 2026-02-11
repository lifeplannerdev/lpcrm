from django.contrib import admin
from .models import CallLog

@admin.register(CallLog)
class CallLogAdmin(admin.ModelAdmin):
    list_display = ("call_id", "caller_number", "agent_number", "status", "duration", "created_at")
    search_fields = ("caller_number", "agent_number", "call_id")
