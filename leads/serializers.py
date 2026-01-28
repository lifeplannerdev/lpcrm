from rest_framework import serializers
from .models import Lead, ProcessingUpdate, RemarkHistory


#  Lead Create Serializer 
class LeadCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lead
        fields = [
            'name',
            'phone',
            'email',
            'source',
            'custom_source',
            'priority',
            'program',
            'location',
            'remarks',
            'status',
            'assigned_to', 
        ]


    def validate(self, attrs):
        # Normalize fields to uppercase
        for field in ['source', 'status', 'priority']:
            if attrs.get(field):
                attrs[field] = attrs[field].upper()

        if attrs.get('source') == 'OTHER' and not attrs.get('custom_source'):
            raise serializers.ValidationError({
                "custom_source": "This field is required when source is OTHER."
            })

        if attrs.get('status') in ['REGISTERED', 'COMPLETED']:
            raise serializers.ValidationError({
                "status": "Cannot create a lead directly with this status."
            })

        # ADD VALIDATION FOR assigned_to
        assigned_to = attrs.get('assigned_to')
        if assigned_to and assigned_to.role not in ['ADM_MANAGER', 'ADM_EXEC']:
            raise serializers.ValidationError({
                "assigned_to": "User must have ADM_MANAGER or ADM_EXEC role."
            })

        return attrs
    
    def create(self, validated_data):
        # Set assigned_date if assigned_to is provided
        if validated_data.get('assigned_to'):
            validated_data['assigned_date'] = timezone.now()
        return super().create(validated_data)




#  Lead List Serializer 
class LeadListSerializer(serializers.ModelSerializer):
    assigned_to_name = serializers.CharField(source='assigned_to.username', read_only=True)
    assigned_to_id = serializers.IntegerField(source='assigned_to.id', read_only=True, allow_null=True)

    class Meta:
        model = Lead
        fields = [
            'id',
            'name',
            'phone',
            'status',
            'priority',
            'program',
            'source',
            'processing_status',
            'assigned_to',           
            'assigned_to_name',       
            'assigned_to_id',         
            'assigned_date',          
            'created_at',
            'email',
            'location',
        ]


#  Lead Detail Serializer 

class LeadDetailSerializer(serializers.ModelSerializer):
    assigned_to_name = serializers.CharField(source='assigned_to.username', read_only=True)
    
    class Meta:
        model = Lead
        fields = '__all__'
        read_only_fields = (
            'created_at',
            'updated_at',
            'processing_status_date',
            'registration_date',
            'assigned_date', 
        )

    def validate_assigned_to(self, value):
        """Validate that assigned user has correct role"""
        if value and value.role not in ['ADM_MANAGER', 'ADM_EXEC']:
            raise serializers.ValidationError(
                "User must have ADM_MANAGER or ADM_EXEC role."
            )
        return value


    def update(self, instance, validated_data):
        request = self.context.get('request')

        # Track assignment changes
        if 'assigned_to' in validated_data:
            old_assigned = instance.assigned_to
            new_assigned = validated_data.get('assigned_to')
            
            if old_assigned != new_assigned:
                # Update assigned_date when assignment changes
                validated_data['assigned_date'] = timezone.now()

        # Track remarks changes (existing code)
        if 'remarks' in validated_data and instance.remarks != validated_data.get('remarks'):
            RemarkHistory.objects.create(
                lead=instance,
                previous_remarks=instance.remarks,
                new_remarks=validated_data.get('remarks'),
                changed_by=request.user if request else None
            )

        # Validate non-empty status
        new_status = validated_data.get('status')
        if new_status is not None and not new_status.strip():
            raise serializers.ValidationError({"status": "Status cannot be empty."})

        return super().update(instance, validated_data)


#  Remark History Serializer 
class RemarkHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = RemarkHistory
        fields = [
            'id',
            'lead',
            'previous_remarks',
            'new_remarks',
            'changed_by',
            'changed_at',
        ]
        read_only_fields = ('changed_at',)

    def validate_changed_by(self, value):
        if not value:
            raise serializers.ValidationError("Changed by must be provided.")
        return value

