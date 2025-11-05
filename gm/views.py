from django.shortcuts import render, redirect, get_object_or_404
import logging
from accounts.models import DailyReport, User
from django.views.decorators.http import require_POST, require_http_methods
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse
from django.db.models import Q, Count
from django.utils import timezone
from datetime import datetime, timedelta
import json

from accounts.models import User
from leads.models import Lead
from tasks.models import Task, TaskUpdate

logger = logging.getLogger(__name__)

def is_gm(user):
    """Check if user is GM or higher - using ADMIN role as GM"""
    return user.role in ['ADMIN', 'BUSINESS_HEAD', 'OPS', 'CM']

@login_required
@user_passes_test(is_gm)
def gm_dashboard(request):
    """Main GM Dashboard"""
    context = get_dashboard_context(request)
    return render(request, 'gm/dashboard.html', context)

@login_required
@user_passes_test(is_gm)
def overview_tab(request):
    """Overview tab data"""
    Task.update_overdue_tasks()
    context = get_dashboard_context(request)
    return render(request, 'gm/partials/overview.html', context)

@login_required
@user_passes_test(is_gm)
def leads_tab(request):
    """Leads tab data"""
    leads = Lead.objects.all().order_by('-created_at')
    
    # Filters
    source_filter = request.GET.get('source', '')
    status_filter = request.GET.get('status', '')
    staff_filter = request.GET.get('staff', '')
    
    if source_filter:
        leads = leads.filter(source=source_filter)
    if status_filter:
        leads = leads.filter(status__icontains=status_filter)
    if staff_filter:
        leads = leads.filter(assigned_to_id=staff_filter)
    
    # Get staff members for assignment dropdown - include all admission roles
    admission_staff = User.objects.filter(
        role__in=['ADM_MANAGER', 'ADM_EXEC', 'PROCESSING'],
        is_active=True
    )
    
    context = {
        'leads': leads,
        'staff_members': admission_staff,
        'admission_managers': admission_staff.filter(role='ADM_MANAGER'),
        'admission_executives': admission_staff.filter(role__in=['ADM_EXEC', 'PROCESSING']),
        'source_choices': Lead.SOURCE_CHOICES,
    }
    return render(request, 'gm/partials/leads.html', context)

@login_required
@user_passes_test(is_gm)
def staff_tab(request):
    """Staff tab data"""
    staff_members = User.objects.filter(
        is_active=True
    ).annotate(
        total_leads=Count('assigned_leads', distinct=True),
        active_tasks=Count('tasks', filter=Q(tasks__status__in=['PENDING', 'IN_PROGRESS']), distinct=True)
    )
    
    context = {
        'staff_members': staff_members,
    }
    return render(request, 'gm/partials/staff.html', context)

@login_required
@user_passes_test(is_gm)
@require_POST
def gm_assign_lead(request):
    """GM-specific lead assignment function"""
    try:
        data = json.loads(request.body)
        logger.info('[GM] assign_lead payload: %s', data)
        lead_id = data.get('lead_id')
        field = data.get('field')
        value = data.get('value')
        
        if not lead_id or not field:
            return JsonResponse({'status': 'error', 'message': 'Missing required fields'}, status=400)
            
        lead = Lead.objects.get(id=lead_id)
        logger.info('[GM] assign_lead resolved lead id=%s current assigned_to=%s', lead_id, getattr(lead.assigned_to, 'id', None))
        
        # Validate and update fields
        if field == 'priority':
            if value in dict(Lead.PRIORITY_CHOICES).keys():
                lead.priority = value
            else:
                return JsonResponse({'status': 'error', 'message': 'Invalid priority'}, status=400)
                
        elif field == 'status':
            if not value or not str(value).strip():
                return JsonResponse({'status': 'error', 'message': 'Status cannot be empty'}, status=400)
            lead.status = str(value).strip()
            
            if lead.status == 'REGISTERED' and not lead.registration_date:
                lead.registration_date = timezone.now()
            
        elif field == 'program':
            lead.program = value if value != '' else None
            
        elif field == 'assigned_to':
            if value == '' or value is None:
                lead.assigned_to = None
                lead.assigned_date = None
                logger.info('[GM] Unassigned lead id=%s', lead_id)
            else:
                try:
                    assignee = User.objects.get(id=value, is_active=True)
                    logger.info('[GM] Assigning lead id=%s to user id=%s role=%s', lead_id, assignee.id, assignee.role)
                    
                    # GM can assign to admission staff and processing
                    if assignee.role in ['ADM_MANAGER', 'ADM_EXEC', 'PROCESSING']:
                        lead.assigned_to = assignee
                        if not lead.assigned_date:
                            lead.assigned_date = timezone.now()
                    else:
                        logger.warning('[GM] Invalid assignee role for user id=%s role=%s', assignee.id, assignee.role)
                        return JsonResponse({
                            'status': 'error', 
                            'message': 'Can only assign to admission staff'
                        }, status=400)
                        
                except User.DoesNotExist:
                    logger.exception('[GM] Assignee does not exist id=%s', value)
                    return JsonResponse({'status': 'error', 'message': 'Invalid user assignment'}, status=400)
            
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid field'}, status=400)
            
        lead.save()
        logger.info('[GM] Saved assignment for lead id=%s assigned_to=%s', lead_id, getattr(lead.assigned_to, 'id', None))
        
        response_data = {
            'status': 'success',
            'assigned_to': {
                'id': lead.assigned_to.id if lead.assigned_to else None,
                'name': lead.assigned_to.get_full_name() if lead.assigned_to else 'Unassigned',
                'role': lead.assigned_to.role if lead.assigned_to else None
            } if field == 'assigned_to' else None
        }
        
        return JsonResponse(response_data)
        
    except Lead.DoesNotExist:
        logger.exception('[GM] Lead not found id=%s', data.get('lead_id') if 'data' in locals() else None)
        return JsonResponse({'status': 'error', 'message': 'Lead not found'}, status=404)
    except Exception as e:
        logger.exception('[GM] Unexpected error during assign')
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

@login_required
@user_passes_test(is_gm)
def tasks_tab(request):
    """Tasks tab data"""
    Task.update_overdue_tasks()
    
    tasks = Task.objects.all().order_by('-created_at')
    
    overdue_count = Task.objects.filter(status='OVERDUE').count()
    
    # Get all active users for task assignment
    staff_members = User.objects.filter(is_active=True)
    
    context = {
        'tasks': tasks,
        'staff_members': staff_members,
        'overdue_count': overdue_count,
    }
    return render(request, 'gm/partials/tasks.html', context)

@login_required
@user_passes_test(is_gm)
def reports_tab(request):
    """Reports tab data"""
    today = timezone.now().date()
    
    recent_reports = DailyReport.objects.filter(
        report_date__gte=today - timezone.timedelta(days=30)
    ).select_related('user').order_by('-report_date', '-created_at')
    
    context = {
        'recent_reports': recent_reports,
        'today': today,
    }
    return render(request, 'gm/partials/reports.html', context)

@login_required
@user_passes_test(is_gm)
def search_data(request):
    """Search functionality for GM dashboard"""
    query = request.GET.get('q', '').strip()
    
    if not query:
        return JsonResponse({'results': []})
    
    results = []
    
    # Search staff
    staff_results = User.objects.filter(
        Q(first_name__icontains=query) | 
        Q(last_name__icontains=query) |
        Q(role__icontains=query) |
        Q(team__icontains=query),
        is_active=True
    )[:5]
    
    for staff in staff_results:
        results.append({
            'type': 'Staff',
            'title': staff.get_full_name(),
            'subtitle': f"{staff.get_role_display()} - {staff.team}",
            'url': '#staff'
        })
    
    # Search leads
    lead_results = Lead.objects.filter(
        Q(name__icontains=query) |
        Q(phone__icontains=query) |
        Q(email__icontains=query) |
        Q(program__icontains=query)
    )[:5]
    
    for lead in lead_results:
        results.append({
            'type': 'Lead',
            'title': lead.name,
            'subtitle': f"{lead.phone} - {lead.program}",
            'url': f"#lead-{lead.id}"
        })
    
    # Search tasks
    task_results = Task.objects.filter(
        Q(title__icontains=query) |
        Q(description__icontains=query)
    )[:5]
    
    for task in task_results:
        results.append({
            'type': 'Task',
            'title': task.title,
            'subtitle': f"Assigned to: {task.assigned_to.get_full_name()}",
            'url': f"#task-{task.id}"
        })
    
    return JsonResponse({'results': results})

@login_required
@user_passes_test(is_gm)
@require_POST
def create_task(request):
    """Create a new task from GM dashboard"""
    try:
        data = json.loads(request.body)
        
        assigned_to_user = User.objects.get(id=data.get('assigned_to'))
        
        task = Task.objects.create(
            title=data.get('title'),
            description=data.get('description', ''),
            assigned_by=request.user,
            assigned_to=assigned_to_user,
            priority=data.get('priority', 'MEDIUM'),
            deadline=data.get('deadline')
        )
        
        TaskUpdate.objects.create(
            task=task,
            updated_by=request.user,
            previous_status='PENDING',
            new_status='PENDING',
            notes=f'Task created by {request.user.get_full_name()}'
        )
        
        return JsonResponse({
            'status': 'success',
            'message': 'Task created successfully!',
            'task_id': task.id
        })
        
    except Exception as e:
        return JsonResponse({
            'status': 'error', 
            'message': f'Error creating task: {str(e)}'
        }, status=400)

@login_required
@user_passes_test(is_gm)
@require_http_methods(["POST", "PUT"])
def update_task(request, task_id):
    """Update a task from GM dashboard"""
    try:
        data = json.loads(request.body or '{}')
        
        task = get_object_or_404(Task, id=task_id)
        if not (task.assigned_by == request.user or is_gm(request.user)):
            return JsonResponse({'status': 'error', 'message': 'Permission denied'}, status=403)
        
        if 'assigned_to' in data and data['assigned_to']:
            assignee = User.objects.get(id=data.get('assigned_to'))
            task.assigned_to = assignee
        if 'title' in data:
            task.title = data['title']
        if 'description' in data:
            task.description = data['description']
        if 'priority' in data:
            task.priority = data['priority']
        if 'deadline' in data:
            task.deadline = data['deadline']
        
        task.save()
        
        TaskUpdate.objects.create(
            task=task,
            updated_by=request.user,
            previous_status=task.status,
            new_status=task.status,
            notes=f'Task updated by {request.user.get_full_name() or request.user.username}'
        )
        
        return JsonResponse({'status': 'success', 'message': 'Task updated successfully!', 'task_id': task.id})
    except User.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Assigned user not found'}, status=404)
    except Task.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Task not found'}, status=404)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

@login_required
@user_passes_test(is_gm)
@require_POST
def delete_task(request, task_id):
    """Delete a task from GM dashboard"""
    try:
        task = get_object_or_404(Task, id=task_id, assigned_by=request.user)
        task.delete()
        
        return JsonResponse({
            'status': 'success',
            'message': 'Task deleted successfully!'
        })
        
    except Task.DoesNotExist:
        return JsonResponse({
            'status': 'error',
            'message': 'Task not found'
        }, status=404)

def get_dashboard_context(request):
    """Get common dashboard context data"""
    Task.update_overdue_tasks()
    
    today = timezone.now().date()
    
    total_staff = User.objects.filter(is_active=True).count()
    
    tasks_today = Task.objects.filter(created_at__date=today)
    total_tasks_assigned = tasks_today.count()
    pending_tasks = Task.objects.filter(status='PENDING').count()
    completed_tasks = Task.objects.filter(status='COMPLETED', completed_at__date=today).count()
    overdue_tasks = Task.objects.filter(
        deadline__lt=timezone.now(),
        status__in=['PENDING', 'IN_PROGRESS']
    ).count()
    
    total_leads = Lead.objects.count()
    today_leads = Lead.objects.filter(created_at__date=today).count()
    
    total_reports = DailyReport.objects.filter(report_date__gte=today - timezone.timedelta(days=30)).count()
    
    recent_leads = Lead.objects.all().order_by('-created_at')[:10]
    
    context = {
        'total_staff': total_staff,
        'total_tasks_assigned': total_tasks_assigned,
        'pending_tasks': pending_tasks,
        'completed_tasks': completed_tasks,
        'overdue_tasks': overdue_tasks,
        'total_leads': total_leads,
        'today_leads': today_leads,
        'recent_leads': recent_leads,
        'total_reports': total_reports,
    }
    
    return context