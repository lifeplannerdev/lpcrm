from tasks.models import Task
import logging

logger = logging.getLogger(__name__)

def update_overdue_tasks():
    """Cron job to update overdue tasks"""
    try:
        updated_count = Task.update_overdue_tasks()
        logger.info(f'Updated {updated_count} overdue tasks')
        return f'Successfully updated {updated_count} tasks'
    except Exception as e:
        logger.error(f'Error updating overdue tasks: {str(e)}')
        return f'Error: {str(e)}'