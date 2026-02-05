from rest_framework import serializers
from .models import Lead, ProcessingUpdate, RemarkHistory, LeadAssignment
from accounts.models import User
from django.utils import timezone


class UserSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'first_name', 'last_name']


# Lead Create Serializer - UPDATED TO HANDLE assigned_to
class LeadCreateSerializer(serializers.ModelSerializer):
    assigned_to = serializers.IntegerField(required=False, allow_null=True, write_only=True)
    
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

    def validate_name(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError("Name is required.")
        if len(value) < 3:
            raise serializers.ValidationError("Name must be at least 3 characters long.")
        return value

    def validate_phone(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError("Phone number is required.")
        if not value.isdigit():
            raise serializers.ValidationError("Phone number must contain only digits.")
        if len(value) < 10:
            raise serializers.ValidationError("Phone number must be at least 10 digits.")
        if Lead.objects.filter(phone=value).exists():
            raise serializers.ValidationError("A lead with this phone number already exists.")
        return value
    
    def validate_assigned_to(self, value):
        """Validate that assigned_to user exists and has appropriate role"""
        if value is None:
            return None
        
        try:
            user = User.objects.get(id=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("User not found.")
        
        # Check if user has appropriate role for assignment
        from .permissions import MANAGER_ROLES, EXECUTIVE_ROLES
        ALLOWED_ASSIGNMENT_ROLES = MANAGER_ROLES + EXECUTIVE_ROLES
        
        if user.role not in ALLOWED_ASSIGNMENT_ROLES:
            raise serializers.ValidationError(
                "Can only assign to managers or executives."
            )
        
        if not user.is_active:
            raise serializers.ValidationError("Cannot assign to inactive user.")
        
        return value

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

        return attrs
    
    def create(self, validated_data):
        """Override create to handle assigned_to properly"""
        assigned_to_id = validated_data.pop('assigned_to', None)
        
        # Create the lead
        lead = Lead.objects.create(**validated_data)
        
        # Handle assignment if provided
        if assigned_to_id:
            try:
                assigned_user = User.objects.get(id=assigned_to_id)
                lead.assigned_to = assigned_user
                
                # Set assignment metadata
                request = self.context.get('request')
                if request and request.user:
                    lead.assigned_by = request.user
                lead.assigned_date = timezone.now()
                
                lead.save()
                
                # Create assignment history record
                LeadAssignment.objects.create(
                    lead=lead,
                    assigned_to=assigned_user,
                    assigned_by=request.user if request else None,
                    assignment_type='PRIMARY',
                    notes='Initial assignment during lead creation'
                )
            except User.DoesNotExist:
                # If user not found, just create lead without assignment
                pass
        
        return lead


class LeadAssignmentSerializer(serializers.ModelSerializer):
    assigned_to = UserSimpleSerializer(read_only=True)
    assigned_by = UserSimpleSerializer(read_only=True)
    
    class Meta:
        model = LeadAssignment
        fields = ['id', 'lead', 'assigned_to', 'assigned_by', 'assignment_type', 'notes', 'timestamp']
        read_only_fields = ['timestamp']


# UPDATE THIS SECTION IN YOUR serializers.py

class LeadAssignSerializer(serializers.Serializer):
    """Serializer for assigning leads (both primary and sub-assignment)"""
    lead_id = serializers.IntegerField()
    assigned_to_id = serializers.IntegerField()
    notes = serializers.CharField(required=False, allow_blank=True)
    
    def validate(self, attrs):
        user = self.context['request'].user
        lead_id = attrs.get('lead_id')
        assigned_to_id = attrs.get('assigned_to_id')
        
        # Check if lead exists
        try:
            lead = Lead.objects.get(id=lead_id)
        except Lead.DoesNotExist:
            raise serializers.ValidationError({"lead_id": "Lead not found."})
        
        # Check if assignee exists
        try:
            assignee = User.objects.get(id=assigned_to_id)
        except User.DoesNotExist:
            raise serializers.ValidationError({"assigned_to_id": "User not found."})
        
        # Validation based on user role
        from .permissions import ADMIN_ROLES, OPERATIONS_ROLES, MANAGER_ROLES, EXECUTIVE_ROLES
        
        # ADMIN and OPS can assign to managers or executives
        if user.role in ADMIN_ROLES or user.role in OPERATIONS_ROLES:
            if assignee.role not in MANAGER_ROLES + EXECUTIVE_ROLES:
                raise serializers.ValidationError({
                    "assigned_to_id": "Can only assign to managers or executives."
                })
            attrs['assignment_type'] = 'PRIMARY'
            
        elif user.role in MANAGER_ROLES:
            # Manager can only sub-assign to executives
            if assignee.role not in EXECUTIVE_ROLES:
                raise serializers.ValidationError({
                    "assigned_to_id": "Managers can only assign to executives."
                })
            
            # Manager can only sub-assign leads assigned to them
            if lead.assigned_to != user:
                raise serializers.ValidationError({
                    "lead_id": "You can only sub-assign leads that are assigned to you."
                })
            
            attrs['assignment_type'] = 'SUB'
        else:
            raise serializers.ValidationError("You don't have permission to assign leads.")
        
        attrs['lead'] = lead
        attrs['assignee'] = assignee
        return attrs


class LeadListSerializer(serializers.ModelSerializer):
    assigned_to = UserSimpleSerializer(read_only=True)
    assigned_by = UserSimpleSerializer(read_only=True)
    sub_assigned_to = UserSimpleSerializer(read_only=True)
    sub_assigned_by = UserSimpleSerializer(read_only=True)
    current_handler = UserSimpleSerializer(read_only=True)

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
            'assigned_by',
            'assigned_date',
            'sub_assigned_to',
            'sub_assigned_by',
            'sub_assigned_date',
            'current_handler',
            'created_at',
            'email',
            'location',
        ]


class LeadDetailSerializer(serializers.ModelSerializer):
    assigned_to = UserSimpleSerializer(read_only=True)
    assigned_by = UserSimpleSerializer(read_only=True)
    sub_assigned_to = UserSimpleSerializer(read_only=True)
    sub_assigned_by = UserSimpleSerializer(read_only=True)
    processing_executive = UserSimpleSerializer(read_only=True)
    current_handler = UserSimpleSerializer(read_only=True)
    assignment_history = LeadAssignmentSerializer(many=True, read_only=True)
    
    class Meta:
        model = Lead
        fields = '__all__'
        read_only_fields = (
            'created_at',
            'updated_at',
            'processing_status_date',
            'registration_date',
            'assigned_by',
            'assigned_date',
            'sub_assigned_by',
            'sub_assigned_date',
        )

    def to_internal_value(self, data):
        data = data.copy() if hasattr(data, 'copy') else dict(data)
        
        if 'priority' in data and data['priority']:
            data['priority'] = data['priority'].upper()
        
        if 'status' in data and data['status']:
            data['status'] = data['status'].upper()
        
        if 'source' in data and data['source']:
            data['source'] = data['source'].upper()
        
        return super().to_internal_value(data)

    def update(self, instance, validated_data):
        request = self.context.get('request')

        if 'remarks' in validated_data and instance.remarks != validated_data.get('remarks'):
            RemarkHistory.objects.create(
                lead=instance,
                previous_remarks=instance.remarks,
                new_remarks=validated_data.get('remarks'),
                changed_by=request.user if request else None
            )

        new_status = validated_data.get('status')
        if new_status is not None and not new_status.strip():
            raise serializers.ValidationError({"status": "Status cannot be empty."})

        return super().update(instance, validated_data)


# Processing Update Serializer 
class ProcessingUpdateSerializer(serializers.ModelSerializer):
    changed_by = UserSimpleSerializer(read_only=True)
    
    class Meta:
        model = ProcessingUpdate
        fields = [
            'id',
            'lead',
            'status',
            'changed_by',
            'notes',
            'timestamp',
        ]
        read_only_fields = ('timestamp',)

    def validate_status(self, value):
        if value not in dict(Lead.PROCESSING_STATUS_CHOICES).keys():
            raise serializers.ValidationError("Invalid processing status.")
        return value

    def validate(self, attrs):
        lead = attrs.get('lead')
        changed_by = attrs.get('changed_by')

        if not Lead.objects.filter(id=lead.id).exists():
            raise serializers.ValidationError({"lead": "Lead does not exist."})

        if changed_by and changed_by.role != 'PROCESSING':
            raise serializers.ValidationError({"changed_by": "User must have PROCESSING role to update status."})

        return attrs


# Remark History Serializer 
class RemarkHistorySerializer(serializers.ModelSerializer):
    changed_by = UserSimpleSerializer(read_only=True)
    
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
