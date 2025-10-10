from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils import timezone
import json
from .models import Task, TaskUpdate
from .forms import TaskForm, TaskUpdateForm
from accounts.models import User





@login_required
def my_tasks(request):
    """View for users to see their assigned tasks"""
    tasks = Task.objects.filter(assigned_to=request.user).order_by('-priority', '-created_at')
    
    # Statistics for the user
    my_total_tasks = tasks.count()
    my_pending_tasks = tasks.filter(status='PENDING').count()
    my_in_progress_tasks = tasks.filter(status='IN_PROGRESS').count()
    my_completed_tasks = tasks.filter(status='COMPLETED').count()
    my_overdue_tasks = tasks.filter(status='OVERDUE').count()
    
    context = {
        'tasks': tasks,
        'my_total_tasks': my_total_tasks,
        'my_pending_tasks': my_pending_tasks,
        'my_in_progress_tasks': my_in_progress_tasks,
        'my_completed_tasks': my_completed_tasks,
        'my_overdue_tasks': my_overdue_tasks,
    }
    return render(request, 'tasks/my_tasks.html', context)

@login_required
def my_tasks_ajax(request):
    """AJAX endpoint for task sidebar to get user's tasks"""
    if request.headers.get('X-Requested-With') != 'XMLHttpRequest':
        return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)
    
    try:
        tasks = Task.objects.filter(assigned_to=request.user).order_by('-priority', '-created_at')
        
        # Convert tasks to JSON-serializable format
        tasks_data = []
        for task in tasks:
            tasks_data.append({
                'id': task.id,
                'title': task.title,
                'description': task.description,
                'status': task.status,
                'priority': task.priority,
                'deadline': task.deadline.strftime('%b %d, %Y %I:%M %p'),
                'overdue_days': task.overdue_days if task.status == 'OVERDUE' else 0,
                'assigned_by': task.assigned_by.get_full_name() or task.assigned_by.username,
                'created_at': task.created_at.strftime('%b %d, %Y'),
            })
        
        return JsonResponse({
            'status': 'success',
            'tasks': tasks_data,
            'total_tasks': len(tasks_data)
        })
        
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

@login_required
@require_POST
def update_task_status(request, task_id):
    """Update task status with notes"""
    try:
        task = get_object_or_404(Task, id=task_id, assigned_to=request.user)
        data = json.loads(request.body)
        new_status = data.get('status')
        notes = data.get('notes', '')
        
        if new_status not in dict(Task.STATUS_CHOICES).keys():
            return JsonResponse({'status': 'error', 'message': 'Invalid status'}, status=400)
        
        # Create task update record
        TaskUpdate.objects.create(
            task=task,
            updated_by=request.user,
            previous_status=task.status,
            new_status=new_status,
            notes=notes
        )
        
        # Update task status
        task.status = new_status
        if new_status == 'COMPLETED':
            task.completed_at = timezone.now()
        task.save()
        
        return JsonResponse({
            'status': 'success',
            'task_status': task.get_status_display(),
            'completed_at': task.completed_at.strftime('%b %d, %Y %I:%M %p') if task.completed_at else None
        })
        
    except Task.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Task not found'}, status=404)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

@login_required
def task_detail(request, task_id):
    """View task details and updates"""
    task = get_object_or_404(Task, id=task_id)
    
    # Check if user has permission to view this task
    if not (request.user == task.assigned_to or request.user == task.assigned_by or is_business_head(request.user)):
        messages.error(request, 'You do not have permission to view this task.')
        return redirect('tasks:my_tasks')
    
    updates = task.updates.all().order_by('-created_at')
    
    context = {
        'task': task,
        'updates': updates,
    }
    return render(request, 'tasks/task_detail.html', context)

