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
from .models import Employee, Penalty, AttendanceDocument
from django.core.paginator import Paginator

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



@login_required
@user_passes_test(lambda u: u.is_hr)
def documents_partial(request):
    """Documents partial view"""
    documents = AttendanceDocument.objects.all().order_by('-date')
    
    # Add search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        documents = documents.filter(
            Q(name__icontains=search_query) |
            Q(month__icontains=search_query)
        )
    
    # Add pagination
    paginator = Paginator(documents, 10)  # 10 documents per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'documents': page_obj,
        'search_query': search_query,
    }
    
    return render(request, 'hr/partials/documents.html', context)

@require_POST
@login_required
@user_passes_test(lambda u: u.is_hr)
def add_document(request):
    """Add new attendance document"""
    try:
        # Get form data
        name = request.POST.get('name')
        date = request.POST.get('date')
        month = request.POST.get('month')
        document_file = request.FILES.get('document')
        
        # Create new document
        document = AttendanceDocument.objects.create(
            name=name,
            date=date,
            month=month,
        )
        
        # Upload document to Cloudinary if provided
        if document_file:
            document.document = document_file
            document.save()
        
        return JsonResponse({
            'status': 'success',
            'message': 'Document uploaded successfully',
            'document_id': document.id
        })
    except Exception as e:
        logger.error(f"Error adding document: {str(e)}")
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        })

@require_http_methods(["DELETE"])
@login_required
@user_passes_test(lambda u: u.is_hr)
def delete_document(request, document_id):
    """Delete a document"""
    try:
        document = get_object_or_404(AttendanceDocument, id=document_id)
        document.delete()
        return JsonResponse({
            'status': 'success',
            'message': 'Document deleted successfully'
        })
    except Exception as e:
        logger.error(f"Error deleting document: {str(e)}")
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        })

@login_required
@user_passes_test(lambda u: u.is_hr)
def document_details(request, document_id):
    """Get document details for modal view"""
    try:
        document = get_object_or_404(AttendanceDocument, id=document_id)
        
        # Determine file type and icon
        file_type = "Unknown"
        file_type_class = "neutral"
        icon_class = "file"
        
        if document.document:
            doc_url = document.document.url.lower()
            if '.pdf' in doc_url:
                file_type = "PDF"
                file_type_class = "error"
                icon_class = "file-pdf"
            elif '.xlsx' in doc_url or '.xls' in doc_url:
                file_type = "Excel"
                file_type_class = "success"
                icon_class = "file-excel"
            elif '.doc' in doc_url or '.docx' in doc_url:
                file_type = "Word"
                file_type_class = "info"
                icon_class = "file-word"
            elif '.jpg' in doc_url or '.png' in doc_url or '.jpeg' in doc_url:
                file_type = "Image"
                file_type_class = "warning"
                icon_class = "file-image"
            else:
                file_type = "File"
                file_type_class = "neutral"
                icon_class = "file"
        
        document_data = {
            'id': document.id,
            'name': document.name,
            'date': document.date.strftime("%Y-%m-%d") if document.date else "",
            'month': document.month,
            'file_type': file_type,
            'file_type_class': file_type_class,
            'icon_class': icon_class,
            'uploaded_at': document.uploaded_at.strftime("%B %d, %Y at %I:%M %p") if document.uploaded_at else "",
            'document_url': document.document.url if document.document else None
        }
        
        return JsonResponse({
            'status': 'success',
            'document': document_data
        })
    except Exception as e:
        logger.error(f"Error fetching document details: {str(e)}")
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        })
