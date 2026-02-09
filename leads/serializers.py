from rest_framework import serializers
from .models import Lead, ProcessingUpdate, RemarkHistory, LeadAssignment
from accounts.models import User
from django.utils import timezone
from .permissions import ADMIN_ROLES, OPERATIONS_ROLES, MANAGER_ROLES, EXECUTIVE_ROLES


class UserSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'first_name', 'last_name']


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
        if len(value) < 3:
            raise serializers.ValidationError("Name must be at least 3 characters long.")
        return value

    def validate_phone(self, value):
        value = value.strip()
        if not value.isdigit():
            raise serializers.ValidationError("Phone number must contain only digits.")
        if len(value) < 10:
            raise serializers.ValidationError("Phone number must be at least 10 digits.")
        if Lead.objects.filter(phone=value).exists():
            raise serializers.ValidationError("A lead with this phone number already exists.")
        return value

    def validate_assigned_to(self, value):
        if value is None:
            return None

        request = self.context.get('request')
        creator = getattr(request, 'user', None)

        try:
            assignee = User.objects.get(id=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("Assigned user not found.")

        if not assignee.is_active:
            raise serializers.ValidationError("Cannot assign to inactive user.")

        # ADM_EXEC → self only
        if creator and creator.role == 'ADM_EXEC':
            if assignee != creator:
                raise serializers.ValidationError(
                    "Admission Executives can assign leads only to themselves."
                )

        # FOE → self only
        elif creator and creator.role == 'FOE':
            if assignee != creator:
                raise serializers.ValidationError(
                    "Front Office Executives can assign leads only to themselves."
                )

        # ADM_MANAGER → self, FOE, or ADM_EXEC
        elif creator and creator.role == 'ADM_MANAGER':
            if assignee != creator and assignee.role not in ['ADM_EXEC', 'FOE']:
                raise serializers.ValidationError(
                    "Admission Managers can assign leads to themselves, Front Office Executives, or Admission Executives."
                )

        # Other MANAGER_ROLES (CM, BDM) → executives only
        elif creator and creator.role in MANAGER_ROLES and creator.role != 'ADM_MANAGER':
            if assignee.role not in EXECUTIVE_ROLES:
                raise serializers.ValidationError(
                    "Managers can assign leads to executives only."
                )

        # ADMIN / OPS → managers or executives
        elif creator and (creator.role in ADMIN_ROLES or creator.role in OPERATIONS_ROLES):
            if assignee.role not in MANAGER_ROLES + EXECUTIVE_ROLES:
                raise serializers.ValidationError(
                    "Admins can assign leads only to managers or executives."
                )
        
        else:
            raise serializers.ValidationError("You do not have permission to assign leads.")

        return value

    def validate(self, attrs):
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
        assigned_to_id = validated_data.pop('assigned_to', None)
        request = self.context.get('request')
        creator = getattr(request, 'user', None)

        lead = Lead.objects.create(**validated_data)

        if assigned_to_id:
            assignee = User.objects.get(id=assigned_to_id)
            lead.assigned_to = assignee
            lead.assigned_by = creator
            lead.assigned_date = timezone.now()
            lead.save()

            LeadAssignment.objects.create(
                lead=lead,
                assigned_to=assignee,
                assigned_by=creator,
                assignment_type='PRIMARY',
                notes='Initial assignment during lead creation'
            )

        return lead


class LeadAssignmentSerializer(serializers.ModelSerializer):
    assigned_to = UserSimpleSerializer(read_only=True)
    assigned_by = UserSimpleSerializer(read_only=True)

    class Meta:
        model = LeadAssignment
        fields = ['id', 'lead', 'assigned_to', 'assigned_by', 'assignment_type', 'notes', 'timestamp']
        read_only_fields = ['timestamp']


class LeadAssignSerializer(serializers.Serializer):
    lead_id = serializers.IntegerField()
    assigned_to_id = serializers.IntegerField()
    notes = serializers.CharField(required=False, allow_blank=True)

    def validate(self, attrs):
        user = self.context['request'].user

        try:
            lead = Lead.objects.get(id=attrs['lead_id'])
        except Lead.DoesNotExist:
            raise serializers.ValidationError({"lead_id": "Lead not found."})

        try:
            assignee = User.objects.get(id=attrs['assigned_to_id'])
        except User.DoesNotExist:
            raise serializers.ValidationError({"assigned_to_id": "User not found."})

        # ADMIN / OPS
        if user.role in ADMIN_ROLES or user.role in OPERATIONS_ROLES:
            if assignee.role not in MANAGER_ROLES + EXECUTIVE_ROLES:
                raise serializers.ValidationError({
                    "assigned_to_id": "Can only assign to managers or executives."
                })
            attrs['assignment_type'] = 'PRIMARY'

        # ADM_MANAGER → can assign to FOE or ADM_EXEC
        elif user.role == 'ADM_MANAGER':
            if assignee.role not in ['ADM_EXEC', 'FOE']:
                raise serializers.ValidationError({
                    "assigned_to_id": "Admission Managers can only assign to Front Office Executives or Admission Executives."
                })
            if lead.assigned_to != user:
                raise serializers.ValidationError({
                    "lead_id": "You can only sub-assign leads assigned to you."
                })
            attrs['assignment_type'] = 'SUB'

        # Other MANAGER_ROLES (CM, BDM) → executives only
        elif user.role in MANAGER_ROLES and user.role != 'ADM_MANAGER':
            if assignee.role not in EXECUTIVE_ROLES:
                raise serializers.ValidationError({
                    "assigned_to_id": "Managers can only assign to executives."
                })
            if lead.assigned_to != user:
                raise serializers.ValidationError({
                    "lead_id": "You can only sub-assign leads assigned to you."
                })
            attrs['assignment_type'] = 'SUB'

        # ADM_EXEC → self only
        elif user.role == 'ADM_EXEC':
            if assignee != user:
                raise serializers.ValidationError({
                    "assigned_to_id": "Admission Executives can assign leads only to themselves."
                })
            attrs['assignment_type'] = 'PRIMARY'

        # FOE → self only
        elif user.role == 'FOE':
            if assignee != user:
                raise serializers.ValidationError({
                    "assigned_to_id": "Front Office Executives can assign leads only to themselves."
                })
            attrs['assignment_type'] = 'PRIMARY'

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
