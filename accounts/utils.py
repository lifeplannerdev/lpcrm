from .models import ActivityLog


def log_activity(
    action,
    entity_type,
    description,
    user=None,
    entity_id=None,
    entity_name='',
    metadata=None,
):
    """
    Create an ActivityLog entry.

    Args:
        action       (str)  : One of ActivityLog.ACTION_CHOICES keys
        entity_type  (str)  : "Lead" | "Task" | "FollowUp" | "Staff" | "MicroWork"
        description  (str)  : Human-readable sentence shown in the feed
        user         (User) : The user who performed the action (None = system)
        entity_id    (int)  : PK of the related object
        entity_name  (str)  : Display name (lead name, task title, etc.)
        metadata     (dict) : Extra context (old/new values, status etc.)
    """
    ActivityLog.objects.create(
        user=user,
        action=action,
        entity_type=entity_type,
        entity_id=entity_id,
        entity_name=entity_name,
        description=description,
        metadata=metadata or {},
    )