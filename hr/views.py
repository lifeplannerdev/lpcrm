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
from .models import Employee
from leads.models import Lead
from .models import Penalty
from tasks.models import Task

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

@login_required
@user_passes_test(lambda u: u.is_hr)
def employees(request):
    """Employees management view"""
    employees = Employee.objects.all()
    tasks = Task.objects.filter(assigned_to=request.user).order_by('-priority', '-created_at')
    
    return render(request, 'hr/employees.html', {
        'employees': employees, 
        'tasks': tasks,
    })

@login_required
@user_passes_test(lambda u: u.is_hr)
def employees_list_partial(request):
    """Employees list partial view"""
    employees = Employee.objects.all().order_by('name')
    return render(request, 'hr/partials/employees_list.html', {
        'employees': employees,
    })

@require_POST
@login_required
@user_passes_test(lambda u: u.is_hr)
def add_employee(request):
    """Add new employee"""
    print("Add employee view called")
    try:
        # Get form data
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address', '')
        join_date = request.POST.get('join_date', '')
        position = request.POST.get('position')
        salary = request.POST.get('salary')
        
        print(f"Form data: name={name}, email={email}, phone={phone}, position={position}, salary={salary}")
        
        # Create new employee
        employee = Employee.objects.create(
            name=name,
            email=email,
            phone=phone,
            address=address,
            join_date=join_date,
            position=position,
            salary=salary
        )
        
        print(f"Employee created with ID: {employee.id}")
        
        return JsonResponse({
            'status': 'success',
            'message': 'Employee added successfully',
            'employee_id': employee.id
        })
    except Exception as e:
        print(f"Error adding employee: {str(e)}")
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        })

@require_http_methods(["DELETE"])
@login_required
@user_passes_test(lambda u: u.is_hr)
def delete_employee(request, employee_id):
    """Delete an employee"""
    try:
        employee = get_object_or_404(Employee, id=employee_id)
        employee.delete()
        return JsonResponse({
            'status': 'success',
            'message': 'Employee deleted successfully'
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        })        

@login_required
@user_passes_test(lambda u: u.is_hr)
def attendance_partial(request):
    """Attendance partial view"""
    # For now, we'll return the partial without specific data
    # You can add specific attendance data logic here
    return render(request, 'hr/partials/attendance.html')

@login_required
@user_passes_test(lambda u: u.is_hr)
def penalties_partial(request):
    """Penalties partial view"""
    penalties = Penalty.objects.all().order_by('-id')
    employees = Employee.objects.all()
    total_amount = sum(penalty.amount for penalty in penalties)
    avg_amount = total_amount / len(penalties) if penalties else 0
    
    # Check if this is an AJAX request
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'hr/partials/penalties.html', {
            'penalties': penalties,
            'employees': employees,
            'total_amount': total_amount,
            'avg_amount': avg_amount,
        })
    
    return render(request, 'hr/partials/penalties.html', {
        'penalties': penalties,
        'employees': employees,
        'total_amount': total_amount,
        'avg_amount': avg_amount,
    })


@require_POST
@login_required
@user_passes_test(lambda u: u.is_hr)
def add_penalty(request):
    """Add new penalty"""
    try:
        # Get form data
        employee_id = request.POST.get('employee')
        act = request.POST.get('act')
        amount = request.POST.get('amount')
        month = request.POST.get('month')
        date = request.POST.get('date')
        
        # Get employee instance
        employee = Employee.objects.get(id=employee_id)
        
        # Create new penalty
        penalty = Penalty.objects.create(
            employee=employee,
            act=act,
            amount=amount,
            month=month,
            date=date
        )
        
        return JsonResponse({
            'status': 'success',
            'message': 'Penalty added successfully',
            'penalty_id': penalty.id
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        })


@require_http_methods(["DELETE"])
@login_required
@user_passes_test(lambda u: u.is_hr)
def delete_penalty(request, penalty_id):
    """Delete a penalty"""
    try:
        penalty = get_object_or_404(Penalty, id=penalty_id)
        penalty.delete()
        return JsonResponse({
            'status': 'success',
            'message': 'Penalty deleted successfully'
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        })


