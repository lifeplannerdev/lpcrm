from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver
from tasks.models import Task
from accounts.utils import log_activity
 
 
@receiver(pre_save, sender=Task)
def capture_task_old_state(sender, instance, **kwargs):
    if instance.pk:
        try:
            instance._old_task_status = Task.objects.get(pk=instance.pk).status
        except Task.DoesNotExist:
            instance._old_task_status = None
    else:
        instance._old_task_status = None
 
 
@receiver(post_save, sender=Task)
def log_task_activity(sender, instance, created, **kwargs):
    label    = instance.title
    assignee = instance.assigned_to.get_full_name() or instance.assigned_to.username if instance.assigned_to else 'Unknown'
    assigner = instance.assigned_by.get_full_name() or instance.assigned_by.username if instance.assigned_by else 'Unknown'
 
    if created:
        log_activity(
            action='TASK_CREATED',
            entity_type='Task',
            entity_id=instance.pk,
            entity_name=label,
            user=instance.assigned_by,   # ← The person who created the task
            description=f'Task "{label}" created by "{assigner}" and assigned to "{assignee}".',
            metadata={'priority': instance.priority, 'deadline': str(instance.deadline), 'assigned_to': assignee},
        )
        return
 
    old_status = getattr(instance, '_old_task_status', None)
 
    if old_status is None or old_status == instance.status:
        # General update — attribute to assigner
        log_activity(
            action='TASK_UPDATED',
            entity_type='Task',
            entity_id=instance.pk,
            entity_name=label,
            user=instance.assigned_by,   # ← FIXED
            description=f'Task "{label}" was updated.',
            metadata={'status': instance.status, 'priority': instance.priority},
        )
        return
 
    if instance.status == 'COMPLETED':
        log_activity(
            action='TASK_COMPLETED',
            entity_type='Task',
            entity_id=instance.pk,
            entity_name=label,
            user=instance.assigned_to,   # ← The assignee completed it
            description=f'Task "{label}" was marked completed by "{assignee}".',
            metadata={'completed_at': str(instance.completed_at)},
        )
    elif instance.status == 'CANCELLED':
        log_activity(
            action='TASK_CANCELLED',
            entity_type='Task',
            entity_id=instance.pk,
            entity_name=label,
            user=instance.assigned_by,   # ← Manager cancelled it
            description=f'Task "{label}" was cancelled.',
        )
    elif instance.status == 'OVERDUE':
        log_activity(
            action='TASK_OVERDUE',
            entity_type='Task',
            entity_id=instance.pk,
            entity_name=label,
            user=None,   # System auto-marked, no specific user
            description=f'Task "{label}" is overdue. Deadline was {instance.deadline}.',
            metadata={'deadline': str(instance.deadline), 'assigned_to': assignee},
        )
    else:
        log_activity(
            action='TASK_STATUS_CHANGED',
            entity_type='Task',
            entity_id=instance.pk,
            entity_name=label,
            user=instance.assigned_to,   # ← Assignee changed status
            description=f'Task "{label}" status changed from {old_status} → {instance.status}.',
            metadata={'old_status': old_status, 'new_status': instance.status},
        )
 
 
@receiver(post_delete, sender=Task)
def log_task_deleted(sender, instance, **kwargs):
    log_activity(
        action='TASK_DELETED',
        entity_type='Task',
        entity_id=instance.pk,
        entity_name=instance.title,
        user=instance.assigned_by,
        description=f'Task "{instance.title}" was deleted.',
    )