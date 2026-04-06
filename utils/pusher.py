# utils/pusher.py
import pusher
from django.conf import settings

def get_pusher_client():
    try:
        return pusher.Pusher(
            app_id=settings.PUSHER_APP_ID,
            key=settings.PUSHER_KEY,
            secret=settings.PUSHER_SECRET,
            cluster=settings.PUSHER_CLUSTER,
            ssl=True
        )
    except Exception as e:
        print(f"[Pusher] Init failed: {e}")
        return None

pusher_client = get_pusher_client()

def trigger_pusher(channel: str, event: str, data: dict):
    if not pusher_client:
        return
    try:
        pusher_client.trigger(channel, event, data)
    except Exception as e:
        print(f"[Pusher] Trigger error: {e}")


# ── Task helpers ──────────────────────────────────────

def notify_task_assigned(task, assigned_by):
    trigger_pusher(
        channel=f"private-user-{task.assigned_to.id}",
        event="task.assigned",
        data={
            "task_id":          task.id,
            "title":            task.title,
            "priority":         task.priority,
            "deadline":         str(task.deadline),
            "assigned_by_id":   assigned_by.id,
            "assigned_by_name": assigned_by.get_full_name() or assigned_by.username,
            "message": (
                f"New task assigned to you: \"{task.title}\" "
                f"by {assigned_by.get_full_name() or assigned_by.username}"
            ),
        }
    )

def notify_task_status_updated(task, updated_by, old_status, new_status, notes):
    trigger_pusher(
        channel=f"private-user-{task.assigned_by.id}",
        event="task.status_updated",
        data={
            "task_id":         task.id,
            "title":           task.title,
            "old_status":      old_status,
            "new_status":      new_status,
            "updated_by_id":   updated_by.id,
            "updated_by_name": updated_by.get_full_name() or updated_by.username,
            "notes":           notes or "",
            "message": (
                f"\"{task.title}\" marked as {new_status} "
                f"by {updated_by.get_full_name() or updated_by.username}"
            ),
        }
    )


# ── Lead helpers ──────────────────────────────────────

def notify_lead_assigned(assignee, assigned_by, lead, assignment_type):
    trigger_pusher(
        channel=f"private-user-{assignee.id}",
        event="lead.assigned",
        data={
            "lead_id":          lead.id,
            "lead_name":        lead.name,
            "lead_phone":       lead.phone,
            "priority":         lead.priority,
            "status":           lead.status,
            "assignment_type":  assignment_type,
            "assigned_by_id":   assigned_by.id,
            "assigned_by_name": assigned_by.get_full_name() or assigned_by.username,
            "message": (
                f"{'Lead' if assignment_type == 'PRIMARY' else 'Sub-lead'} "
                f"assigned to you: {lead.name} "
                f"by {assigned_by.get_full_name() or assigned_by.username}"
            ),
        }
    )


# ── Chat helpers ──────────────────────────────────────

def notify_new_message(conversation_id, message_data):
    trigger_pusher(
        channel=f"private-chat-{conversation_id}",
        event="new-message",
        data=message_data
    )

def notify_new_conversation(user_id, conversation_id, conversation_type, name=None):
    data = {
        "conversation_id": conversation_id,
        "type":            conversation_type,
    }
    if name:
        data["name"] = name
    trigger_pusher(
        channel=f"private-user-{user_id}",
        event="new-conversation",
        data=data
    )