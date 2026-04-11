from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver

from .models import Penalty, AttendanceDocument
from accounts.utils import log_activity


def _user_label(user):
    if not user:
        return 'Unknown'
    return user.get_full_name() or user.username


# ── Penalty Signals ───────────────────────────────────────────────────────────

@receiver(pre_save, sender=Penalty)
def capture_penalty_old_state(sender, instance, **kwargs):
    if instance.pk:
        try:
            old = Penalty.objects.get(pk=instance.pk)
            instance._old_penalty_amount = old.amount
            instance._old_penalty_act    = old.act
        except Penalty.DoesNotExist:
            instance._old_penalty_amount = None
            instance._old_penalty_act    = None
    else:
        instance._old_penalty_amount = None
        instance._old_penalty_act    = None


@receiver(post_save, sender=Penalty)
def log_penalty_activity(sender, instance, created, **kwargs):
    staff_name = _user_label(instance.user)
    label      = f"Penalty — {staff_name}"

    if created:
        log_activity(
            action='PENALTY_ISSUED',
            entity_type='Penalty',
            entity_id=instance.pk,
            entity_name=staff_name,
            description=f'Penalty of ₹{instance.amount} issued to "{staff_name}" for: {instance.act}.',
            metadata={
                'amount': instance.amount,
                'month':  instance.month,
                'act':    instance.act,
                'date':   str(instance.date),
            },
        )
    else:
        log_activity(
            action='PENALTY_UPDATED',
            entity_type='Penalty',
            entity_id=instance.pk,
            entity_name=staff_name,
            description=f'Penalty for "{staff_name}" updated. Amount: ₹{instance.amount}.',
            metadata={
                'old_amount': getattr(instance, '_old_penalty_amount', None),
                'new_amount': instance.amount,
                'month':      instance.month,
            },
        )


@receiver(post_delete, sender=Penalty)
def log_penalty_deleted(sender, instance, **kwargs):
    staff_name = _user_label(instance.user)
    log_activity(
        action='PENALTY_DELETED',
        entity_type='Penalty',
        entity_id=instance.pk,
        entity_name=staff_name,
        description=f'Penalty of ₹{instance.amount} for "{staff_name}" was deleted.',
    )


# ── AttendanceDocument Signals ────────────────────────────────────────────────

@receiver(post_save, sender=AttendanceDocument)
def log_attendance_doc_activity(sender, instance, created, **kwargs):
    if created:
        log_activity(
            action='ATTENDANCE_DOC_UPLOADED',
            entity_type='AttendanceDocument',
            entity_id=instance.pk,
            entity_name=instance.name,
            description=f'Attendance document "{instance.name}" uploaded for {instance.month}.',
            metadata={
                'month': instance.month,
                'date':  str(instance.date),
            },
        )


@receiver(post_delete, sender=AttendanceDocument)
def log_attendance_doc_deleted(sender, instance, **kwargs):
    log_activity(
        action='ATTENDANCE_DOC_DELETED',
        entity_type='AttendanceDocument',
        entity_id=instance.pk,
        entity_name=instance.name,
        description=f'Attendance document "{instance.name}" for {instance.month} was deleted.',
    )