from rest_framework import serializers
from .models import VoxbayCallLog


class VoxbayCallLogSerializer(serializers.ModelSerializer):
    duration_display = serializers.SerializerMethodField()
    conversation_duration_display = serializers.SerializerMethodField()

    class Meta:
        model = VoxbayCallLog
        fields = [
            'id',
            'call_uuid',
            'call_type',
            # Incoming
            'called_number',
            'caller_number',
            'agent_number',
            # Outgoing
            'extension',
            'destination',
            'caller_id',
            # CDR
            'call_status',
            'duration',
            'duration_display',
            'conversation_duration',
            'conversation_duration_display',
            'recording_url',
            'call_start',
            'call_end',
            # Extra
            'dtmf',
            'transferred_number',
            # Meta
            'created_at',
            'updated_at',
        ]
        read_only_fields = fields  # this is a read endpoint

    def get_duration_display(self, obj):
        if not obj.duration:
            return None
        m, s = divmod(obj.duration, 60)
        return f"{m}m {s}s" if m else f"{s}s"

    def get_conversation_duration_display(self, obj):
        if not obj.conversation_duration:
            return None
        m, s = divmod(obj.conversation_duration, 60)
        return f"{m}m {s}s" if m else f"{s}s"


class CallStatsSerializer(serializers.Serializer):
    total             = serializers.IntegerField()
    answered          = serializers.IntegerField()
    missed            = serializers.IntegerField()
    busy              = serializers.IntegerField()
    congestion        = serializers.IntegerField()
    incoming          = serializers.IntegerField()
    outgoing          = serializers.IntegerField()
    avg_duration      = serializers.FloatField()
    success_rate      = serializers.FloatField()


class ClickToCallSerializer(serializers.Serializer):
    uid         = serializers.CharField(max_length=100)
    upin        = serializers.CharField(max_length=100)
    user_no     = serializers.CharField(max_length=50,  help_text="Extension number")
    destination = serializers.CharField(max_length=30,  help_text="Destination mobile number")
    callerid    = serializers.CharField(max_length=30,  help_text="DID number to show as caller ID")
    source      = serializers.CharField(max_length=30,  required=False, allow_blank=True,
                                        help_text="Source mobile (mobile-to-mobile only)")