from django.shortcuts import render, redirect, get_object_or_404
import logging
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse
from django.db.models import Q, Count
from django.utils import timezone
from datetime import datetime, timedelta
import json

from accounts.models import User
from leads.models import Lead
from tasks.models import Task, TaskUpdate
from .models import DailyReport

logger = logging.getLogger(__name__)

def is_business_head(user):
    """Check if user is business head or higher"""
    return user.role in ['BUSINESS_HEAD', 'ADMIN', 'OPS']

@login_required
@user_passes_test(is_business_head)
def hob_dashboard(request):
    """Main HOB Dashboard"""
    context = get_dashboard_context(request)
    return render(request, 'hob/dashboard.html', context)

@login_required
@user_passes_test(is_business_head)
def overview_tab(request):
    """Overview tab data"""
    Task.update_overdue_tasks()
    context = get_dashboard_context(request)
    return render(request, 'hob/partials/overview.html', context)

@login_required
@user_passes_test(is_business_head)
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
    
    # Get staff members for assignment dropdown
    admission_managers = User.objects.filter(
        role='ADM_MANAGER', 
        is_active=True
    )
    admission_executives = User.objects.filter(
        role='ADM_EXEC', 
        is_active=True
    )
    
    context = {
        'leads': leads,
        'staff_members': User.objects.filter(
            role__in=['ADM_MANAGER', 'ADM_EXEC'],
            is_active=True
        ),
        'admission_managers': admission_managers,
        'admission_executives': admission_executives,
        'source_choices': Lead.SOURCE_CHOICES,
    }
    return render(request, 'hob/partials/leads.html', context)

@login_required
@user_passes_test(is_business_head)
def staff_tab(request):
    """Staff tab data"""
    staff_members = User.objects.filter(
        is_active=True
    ).annotate(
        total_leads=Count('assigned_leads'),
        active_tasks=Count('tasks', filter=Q(tasks__status__in=['PENDING', 'IN_PROGRESS']))
    )
    
    context = {
        'staff_members': staff_members,
    }
    return render(request, 'hob/partials/staff.html', context)


@login_required
@user_passes_test(is_business_head)
@require_POST
def hob_assign_lead(request):
    """HOB-specific lead assignment function"""
    try:
        data = json.loads(request.body)
        logger.info('[HOB] assign_lead payload: %s', data)
        lead_id = data.get('lead_id')
        field = data.get('field')
        value = data.get('value')
        
        if not lead_id or not field:
            return JsonResponse({'status': 'error', 'message': 'Missing required fields'}, status=400)
            
        lead = Lead.objects.get(id=lead_id)
        logger.info('[HOB] assign_lead resolved lead id=%s current assigned_to=%s', lead_id, getattr(lead.assigned_to, 'id', None))
        
        # Validate and update fields
        if field == 'priority':
            if value in dict(Lead.PRIORITY_CHOICES).keys():
                lead.priority = value
            else:
                return JsonResponse({'status': 'error', 'message': 'Invalid priority'}, status=400)
                
        elif field == 'status':
            # Status is free-text now; accept non-empty values only
            if not value or not str(value).strip():
                return JsonResponse({'status': 'error', 'message': 'Status cannot be empty'}, status=400)
            lead.status = str(value).strip()
            
            # Update registration date if status changed to REGISTERED
            if lead.status == 'REGISTERED' and not lead.registration_date:
                lead.registration_date = timezone.now()
            
        elif field == 'program':
            lead.program = value if value != '' else None
            
        elif field == 'assigned_to':
            # Handle assignment changes - HOB can assign to anyone
            if value == '' or value is None:
                # Unassign the lead
                lead.assigned_to = None
                lead.assigned_date = None
                logger.info('[HOB] Unassigned lead id=%s', lead_id)
            else:
                try:
                    assignee = User.objects.get(id=value, is_active=True)
                    logger.info('[HOB] Assigning lead id=%s to user id=%s role=%s', lead_id, assignee.id, assignee.role)
                    
                    # HOB can assign to both managers and executives
                    if assignee.role in ['ADM_MANAGER', 'ADM_EXEC']:
                        lead.assigned_to = assignee
                        # Set assignment date if not already set
                        if not lead.assigned_date:
                            lead.assigned_date = timezone.now()
                    else:
                        logger.warning('[HOB] Invalid assignee role for user id=%s role=%s', assignee.id, assignee.role)
                        return JsonResponse({
                            'status': 'error', 
                            'message': 'Can only assign to admission staff'
                        }, status=400)
                        
                except User.DoesNotExist:
                    logger.exception('[HOB] Assignee does not exist id=%s', value)
                    return JsonResponse({'status': 'error', 'message': 'Invalid user assignment'}, status=400)
            
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid field'}, status=400)
            
        lead.save()
        logger.info('[HOB] Saved assignment for lead id=%s assigned_to=%s', lead_id, getattr(lead.assigned_to, 'id', None))
        
        # Return additional data if needed
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
        logger.exception('[HOB] Lead not found id=%s', data.get('lead_id') if 'data' in locals() else None)
        return JsonResponse({'status': 'error', 'message': 'Lead not found'}, status=404)
    except Exception as e:
        logger.exception('[HOB] Unexpected error during assign')
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)    

@login_required
@user_passes_test(is_business_head)
def tasks_tab(request):
    """Tasks tab data"""
    # ← ADD THIS LINE - Check and update overdue tasks
    Task.update_overdue_tasks()
    
    tasks = Task.objects.all().order_by('-created_at')
    
    # Count overdue tasks
    overdue_count = Task.objects.filter(status='OVERDUE').count()
    
    # Get all active users for task assignment
    staff_members = User.objects.filter(is_active=True)
    
    context = {
        'tasks': tasks,
        'staff_members': staff_members,
        'overdue_count': overdue_count,
    }
    return render(request, 'hob/partials/tasks.html', context)

@login_required
@user_passes_test(is_business_head)
def reports_tab(request):
    """Reports tab data"""
    today = timezone.now().date()
    daily_reports = DailyReport.objects.filter(date=today)
    
    context = {
        'daily_reports': daily_reports,
        'today': today,
    }
    return render(request, 'hob/partials/reports.html', context)

@login_required
@user_passes_test(is_business_head)
def search_data(request):
    """Search functionality for HOB dashboard"""
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
            'url': '#staff'  # You can create detail URLs later
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
@user_passes_test(is_business_head)
@require_POST
def create_task(request):
    """Create a new task from HOB dashboard"""
    try:
        data = json.loads(request.body)
        
        # Get the assigned user
        assigned_to_user = User.objects.get(id=data.get('assigned_to'))
        
        task = Task.objects.create(
            title=data.get('title'),
            description=data.get('description', ''),
            assigned_by=request.user,
            assigned_to=assigned_to_user,
            priority=data.get('priority', 'MEDIUM'),
            deadline=data.get('deadline')
        )
        
        # Create initial task update
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
@user_passes_test(is_business_head)
@require_POST
def delete_task(request, task_id):
    """Delete a task from HOB dashboard"""
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
    
    # Staff statistics
    total_staff = User.objects.filter(
        role__in=['ADM_MANAGER', 'ADM_EXEC', 'MEDIA'],
        is_active=True
    ).count()
    
    # Task statistics
    tasks_today = Task.objects.filter(created_at__date=today)
    total_tasks_assigned = tasks_today.count()
    pending_tasks = Task.objects.filter(status='PENDING').count()
    completed_tasks = Task.objects.filter(status='COMPLETED', completed_at__date=today).count()
    overdue_tasks = Task.objects.filter(
        deadline__lt=timezone.now(),
        status__in=['PENDING', 'IN_PROGRESS']
    ).count()
    
    # Lead statistics
    total_leads = Lead.objects.count()
    today_leads = Lead.objects.filter(created_at__date=today).count()
    
    # Recent leads for overview
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
    }
    
    return context

# Create your views here.
