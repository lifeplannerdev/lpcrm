import threading
from .models import ActivityLog

# ── Thread-local storage for current request user ─────────────────────────────
_thread_locals = threading.local()


def set_current_user(user):
    """Called by CurrentUserMiddleware on every request."""
    _thread_locals.current_user = user


def get_current_user():
    """Returns the user attached to the current request thread, or None."""
    return getattr(_thread_locals, 'current_user', None)


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
                              If not passed, falls back to the current request
                              user captured by CurrentUserMiddleware.
        entity_id    (int)  : PK of the related object
        entity_name  (str)  : Display name (lead name, task title, etc.)
        metadata     (dict) : Extra context (old/new values, status etc.)
    """
    # If no user explicitly passed, fall back to thread-local request user
    if user is None:
        user = get_current_user()

    ActivityLog.objects.create(
        user=user,
        action=action,
        entity_type=entity_type,
        entity_id=entity_id,
        entity_name=entity_name,
        description=description,
        metadata=metadata or {},
    )