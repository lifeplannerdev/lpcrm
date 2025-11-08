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

def is_hr(user):
    """Check if user has hr role"""
    return user.role == 'HR'


@login_required
@user_passes_test(lambda u: u.is_hr)
def hr_dashboard(request):
    """HR dashboard view"""
    staff_members = User.objects.filter(is_active=True).annotate(
        total_leads=Count('assigned_leads'),
        active_tasks=Count('tasks', filter=Q(tasks__status__in=['PENDING', 'IN_PROGRESS']))
    )
    tasks = Task.objects.filter(assigned_to=request.user).order_by('-priority', '-created_at')
    
    # Calculate totals
    total_leads = Lead.objects.count()
    total_active_tasks = sum(staff.active_tasks for staff in staff_members)
    
    return render(request, 'hr/hr_dashboard.html', {
        'staff_members': staff_members, 
        'tasks': tasks,
        'total_leads': total_leads,
        'total_active_tasks': total_active_tasks,
    })    
