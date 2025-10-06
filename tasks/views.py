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

def is_business_head(user):
    """Check if user is business head or higher"""
    return user.role in ['BUSINESS_HEAD', 'ADMIN', 'OPS']

@login_required
@user_passes_test(is_business_head)
def business_head_dashboard(request):
    """Business Head Dashboard for task management"""
    # Tasks assigned by this user
    assigned_tasks = Task.objects.filter(assigned_by=request.user).order_by('-created_at')
    
    # All active tasks for overview
    all_tasks = Task.objects.all().order_by('-created_at')[:50]
    
    # Statistics
    total_tasks = Task.objects.count()
    pending_tasks = Task.objects.filter(status='PENDING').count()
    completed_tasks = Task.objects.filter(status='COMPLETED').count()
    overdue_tasks = Task.objects.filter(
        deadline__lt=timezone.now(),
        status__in=['PENDING', 'IN_PROGRESS']
    ).count()
    
    context = {
        'assigned_tasks': assigned_tasks,
        'all_tasks': all_tasks,
        'total_tasks': total_tasks,
        'pending_tasks': pending_tasks,
        'completed_tasks': completed_tasks,
        'overdue_tasks': overdue_tasks,
        'team_members': User.objects.filter(
            role__in=['MEDIA', 'ADM_MANAGER', 'ADM_EXEC'],
            is_active=True
        ),
    }
    return render(request, 'tasks/business_head_dashboard.html', context)

@login_required
@user_passes_test(is_business_head)
def create_task(request):
    """Create a new task"""
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.assigned_by = request.user
            task.save()
            
            # Create initial task update
            TaskUpdate.objects.create(
                task=task,
                updated_by=request.user,
                previous_status='PENDING',
                new_status='PENDING',
                notes=f'Task created by {request.user.get_full_name()}'
            )
            
            messages.success(request, 'Task created successfully!')
            return redirect('tasks:business_head_dashboard')
    else:
        form = TaskForm()
    
    return render(request, 'tasks/create_task.html', {'form': form})

@login_required
def my_tasks(request):
    """View for users to see their assigned tasks"""
    tasks = Task.objects.filter(assigned_to=request.user).order_by('-priority', '-created_at')
    
    # Statistics for the user
    my_total_tasks = tasks.count()
    my_pending_tasks = tasks.filter(status='PENDING').count()
    my_in_progress_tasks = tasks.filter(status='IN_PROGRESS').count()
    my_completed_tasks = tasks.filter(status='COMPLETED').count()
    my_overdue_tasks = tasks.filter(
        deadline__lt=timezone.now(),
        status__in=['PENDING', 'IN_PROGRESS']
    ).count()
    
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

@login_required
@user_passes_test(is_business_head)
@require_POST
def delete_task(request, task_id):
    """Delete a task (Business Head only)"""
    try:
        task = get_object_or_404(Task, id=task_id, assigned_by=request.user)
        task.delete()
        messages.success(request, 'Task deleted successfully!')
        return JsonResponse({'status': 'success'})
    except Task.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Task not found'}, status=404)