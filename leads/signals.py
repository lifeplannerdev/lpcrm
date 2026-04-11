from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver

from .models import Lead, LeadAssignment, FollowUp
from accounts.utils import log_activity


# ── Helpers ──────────────────────────────────────────────────────────────────

def _user_label(user):
    if not user:
        return 'Unknown'
    return user.get_full_name() or user.username


# ── Lead Signals ─────────────────────────────────────────────────────────────

@receiver(pre_save, sender=Lead)
def capture_lead_old_state(sender, instance, **kwargs):
    """Snapshot old field values before save for change detection."""
    if instance.pk:
        try:
            old = Lead.objects.get(pk=instance.pk)
            instance._old_status             = old.status
            instance._old_processing_status  = old.processing_status
            instance._old_assigned_to        = old.assigned_to_id
            instance._old_sub_assigned_to    = old.sub_assigned_to_id
            instance._old_remarks            = old.remarks
        except Lead.DoesNotExist:
            instance._old_status             = None
            instance._old_processing_status  = None
            instance._old_assigned_to        = None
            instance._old_sub_assigned_to    = None
            instance._old_remarks            = None
    else:
        instance._old_status             = None
        instance._old_processing_status  = None
        instance._old_assigned_to        = None
        instance._old_sub_assigned_to    = None
        instance._old_remarks            = None


@receiver(post_save, sender=Lead)
def log_lead_activity(sender, instance, created, **kwargs):
    label = instance.name

    if created:
        log_activity(
            action='LEAD_CREATED',
            entity_type='Lead',
            entity_id=instance.pk,
            entity_name=label,
            description=f'New lead "{label}" was created.',
            metadata={
                'phone':    instance.phone,
                'source':   instance.source,
                'status':   instance.status,
                'priority': instance.priority,
            },
        )
        return  # Skip change checks on creation

    # ── Status changed ───────────────────────────────────────────────────────
    if getattr(instance, '_old_status', None) != instance.status:
        log_activity(
            action='LEAD_STATUS_CHANGED',
            entity_type='Lead',
            entity_id=instance.pk,
            entity_name=label,
            description=(
                f'Lead "{label}" status changed from '
                f'{instance._old_status} → {instance.status}.'
            ),
            metadata={
                'old_status': instance._old_status,
                'new_status': instance.status,
            },
        )

    # ── Processing status changed ────────────────────────────────────────────
    if getattr(instance, '_old_processing_status', None) != instance.processing_status:
        log_activity(
            action='LEAD_PROCESSING_UPDATED',
            entity_type='Lead',
            entity_id=instance.pk,
            entity_name=label,
            description=(
                f'Lead "{label}" processing status changed from '
                f'{instance._old_processing_status} → {instance.processing_status}.'
            ),
            metadata={
                'old_processing_status': instance._old_processing_status,
                'new_processing_status': instance.processing_status,
            },
        )

    # ── Assigned to changed ──────────────────────────────────────────────────
    if getattr(instance, '_old_assigned_to', None) != instance.assigned_to_id:
        assignee = _user_label(instance.assigned_to)
        log_activity(
            action='LEAD_ASSIGNED',
            entity_type='Lead',
            entity_id=instance.pk,
            entity_name=label,
            description=f'Lead "{label}" was assigned to "{assignee}".',
            metadata={'assigned_to': assignee},
        )

    # ── Sub-assigned to changed ──────────────────────────────────────────────
    if getattr(instance, '_old_sub_assigned_to', None) != instance.sub_assigned_to_id:
        if instance.sub_assigned_to:
            sub = _user_label(instance.sub_assigned_to)
            log_activity(
                action='LEAD_SUB_ASSIGNED',
                entity_type='Lead',
                entity_id=instance.pk,
                entity_name=label,
                description=f'Lead "{label}" was sub-assigned to "{sub}".',
                metadata={'sub_assigned_to': sub},
            )
        else:
            log_activity(
                action='LEAD_UNASSIGNED',
                entity_type='Lead',
                entity_id=instance.pk,
                entity_name=label,
                description=f'Lead "{label}" sub-assignment was removed.',
            )

    # ── Remarks changed ──────────────────────────────────────────────────────
    if getattr(instance, '_old_remarks', None) != instance.remarks:
        log_activity(
            action='LEAD_REMARK_UPDATED',
            entity_type='Lead',
            entity_id=instance.pk,
            entity_name=label,
            description=f'Remarks updated for lead "{label}".',
            metadata={
                'old_remarks': instance._old_remarks,
                'new_remarks': instance.remarks,
            },
        )


@receiver(post_delete, sender=Lead)
def log_lead_deleted(sender, instance, **kwargs):
    log_activity(
        action='LEAD_DELETED',
        entity_type='Lead',
        entity_id=instance.pk,
        entity_name=instance.name,
        description=f'Lead "{instance.name}" ({instance.phone}) was deleted.',
    )


# ── FollowUp Signals ─────────────────────────────────────────────────────────

@receiver(pre_save, sender=FollowUp)
def capture_followup_old_state(sender, instance, **kwargs):
    if instance.pk:
        try:
            old = FollowUp.objects.get(pk=instance.pk)
            instance._old_fu_status       = old.status
            instance._old_converted       = old.converted_to_lead
        except FollowUp.DoesNotExist:
            instance._old_fu_status  = None
            instance._old_converted  = False
    else:
        instance._old_fu_status  = None
        instance._old_converted  = False


@receiver(post_save, sender=FollowUp)
def log_followup_activity(sender, instance, created, **kwargs):
    label = instance.name or instance.phone_number

    if created:
        log_activity(
            action='FOLLOWUP_CREATED',
            entity_type='FollowUp',
            entity_id=instance.pk,
            entity_name=label,
            user=instance.assigned_to,
            description=f'Follow-up created for "{label}" on {instance.follow_up_date}.',
            metadata={
                'type':     instance.followup_type,
                'priority': instance.priority,
                'date':     str(instance.follow_up_date),
            },
        )
        return

    # ── Status changed ───────────────────────────────────────────────────────
    if getattr(instance, '_old_fu_status', None) != instance.status:
        log_activity(
            action='FOLLOWUP_STATUS_CHANGED',
            entity_type='FollowUp',
            entity_id=instance.pk,
            entity_name=label,
            user=instance.assigned_to,
            description=(
                f'Follow-up for "{label}" status changed from '
                f'{instance._old_fu_status} → {instance.status}.'
            ),
            metadata={
                'old_status': instance._old_fu_status,
                'new_status': instance.status,
            },
        )

    # ── Converted to lead ────────────────────────────────────────────────────
    if not getattr(instance, '_old_converted', False) and instance.converted_to_lead:
        log_activity(
            action='FOLLOWUP_CONVERTED',
            entity_type='FollowUp',
            entity_id=instance.pk,
            entity_name=label,
            user=instance.assigned_to,
            description=f'Follow-up for "{label}" was converted to a lead.',
        )


@receiver(post_delete, sender=FollowUp)
def log_followup_deleted(sender, instance, **kwargs):
    label = instance.name or instance.phone_number
    log_activity(
        action='FOLLOWUP_DELETED',
        entity_type='FollowUp',
        entity_id=instance.pk,
        entity_name=label,
        description=f'Follow-up for "{label}" was deleted.',
    )