from asyncio import tasks
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import User
import pytz
from tasks.models import Task
from django.db.models import Q, Count, Sum
from django.contrib import messages
from leads.models import Lead
from leads.models import RemarkHistory
from .models import MicroWork
from leads.forms import LeadForm
from django.conf import settings
import json
from django.http import JsonResponse
from django.db import models
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from django.utils import timezone
from leads.models import ProcessingUpdate
from django.db.models import Q
import pandas as pd
from django.http import JsonResponse, HttpResponse
import tempfile
import os
from django.views.decorators.csrf import csrf_exempt
import io
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django.utils import timezone
from .models import DailyReport
import traceback
from .forms import DailyReportForm



def landing_page(request):
    """Render the role selection landing page"""
    return render(request, 'accounts/landing.html')


@require_POST
def quick_login(request):
    """Authenticate with username/password and redirect by role"""
    request.session.cookie_name = settings.SESSION_COOKIE_NAME
    request.session.cookie_path = settings.SESSION_COOKIE_PATH

    username = request.POST.get('username')
    password = request.POST.get('password')

    if not username or not password:
        messages.error(request, "Username and password are required")
        return redirect('accounts:landing')

    try:
        user = authenticate(request, username=username, password=password)
        if user is None:
            messages.error(request, "Invalid username or password")
            return redirect('accounts:landing')

        if not user.is_active:
            messages.error(request, "Your account is inactive")
            return redirect('accounts:landing')

        login(request, user)

        # Redirect based on the authenticated user's role
        role = getattr(user, 'role', None)
        if role == 'ADM_MANAGER':
            return redirect('accounts:admission_dashboard')
        elif role == 'ADM_EXEC':
            return redirect('accounts:admission_executive_dashboard')
        elif role == 'MEDIA':
            return redirect('accounts:media_dashboard')
        elif role == 'OPS':
            return redirect('accounts:operations_dashboard')
        elif role == 'PROCESSING':
            return redirect('accounts:processing_dashboard')
        elif role == 'TRAINER':
            return redirect('trainers:dashboard')
        elif role == 'BUSINESS_HEAD':
            return redirect('hob:dashboard')
        elif role == 'CM':
            return redirect('accounts:cm_dashboard')  
        elif role == 'ADMIN':
            return redirect('gm:dashboard')      

        # Fallback
        return redirect('accounts:landing')

    except Exception as e:
        messages.error(request, f"An error occurred during login: {str(e)}")
        return redirect('accounts:landing')


def is_cm(user):
    """Check if user has cm role"""
    return user.role == 'CM'

@login_required
@user_passes_test(lambda u: u.is_cm)
def cm_dashboard(request):
    """CM dashboard view"""
    staff_members = User.objects.filter(is_active=True).annotate(
        total_leads=Count('assigned_leads'),
        active_tasks=Count('tasks', filter=Q(tasks__status__in=['PENDING', 'IN_PROGRESS']))
    )
    tasks = Task.objects.filter(assigned_to=request.user).order_by('-priority', '-created_at')
    
    # Calculate totals
    total_leads = Lead.objects.count()
    total_active_tasks = sum(staff.active_tasks for staff in staff_members)
    
    return render(request, 'accounts/cm_dashboard.html', {
        'staff_members': staff_members, 
        'tasks': tasks,
        'total_leads': total_leads,
        'total_active_tasks': total_active_tasks,
    })
   


def is_admission_manager(user):
    """Check if user has admission manager role"""
    return user.role == 'ADM_MANAGER'

@login_required
@user_passes_test(is_admission_manager)
def admission_dashboard(request):
    """Admission manager dashboard view"""
    leads = Lead.objects.filter(assigned_to=request.user).order_by('-priority', '-created_at')
    admission_executives = User.objects.filter(role='ADM_EXEC', is_active=True)
    
    context = {
        'high_priority_leads': leads.filter(priority='HIGH'),
        'medium_priority_leads': leads.filter(priority='MEDIUM'),
        'low_priority_leads': leads.filter(priority='LOW'),
        'admission_executives':admission_executives,
    }
    return render(request, 'accounts/admissionmanager.html', context)


def is_admission_executive(user):
    """Check if user has admission executive role"""
    return user.role == 'ADM_EXEC'

@login_required
@user_passes_test(is_admission_executive)
def admission_executive_dashboard(request):
    """Admission executive dashboard view"""
    # Get leads assigned to this executive
    leads = Lead.objects.filter(assigned_to=request.user).order_by('-priority', '-created_at')
    
    # Split by priority
    high_priority_leads = leads.filter(priority='HIGH')
    medium_priority_leads = leads.filter(priority='MEDIUM')
    low_priority_leads = leads.filter(priority='LOW')
    
    context = {
        'high_priority_leads': high_priority_leads,
        'medium_priority_leads': medium_priority_leads,
        'low_priority_leads': low_priority_leads,
    }
    return render(request, 'accounts/admissionexecutive.html', context) 


@login_required
@require_POST
def assign_lead_to_executive(request):
    """Assign lead to admission executive"""
    try:
        data = json.loads(request.body)
        lead_id = data.get('lead_id')
        executive_id = data.get('executive_id')
        
        if not lead_id:
            return JsonResponse({'status': 'error', 'message': 'Lead ID is required'}, status=400)
            
        lead = Lead.objects.get(id=lead_id)
        user = request.user
        
        # Verify permissions
        if not (user.role in ['ADM_MANAGER', 'OPS', 'ADMIN','BUSINESS_HEAD'] or 
                lead.assigned_to == user):
            return JsonResponse(
                {'status': 'error', 'message': 'Permission denied'}, 
                status=403
            )
        
        if executive_id:
            try:
                executive = User.objects.get(
                    id=executive_id, 
                    role='ADM_EXEC', 
                    is_active=True
                )
                lead.assigned_to = executive
                lead.assigned_date = timezone.now()
            except User.DoesNotExist:
                return JsonResponse(
                    {'status': 'error', 'message': 'Invalid executive'}, 
                    status=400
                )
        else:
            # Unassign the lead
            lead.assigned_to = None
            lead.assigned_date = None
            
        lead.save()
        
        return JsonResponse({
            'status': 'success',
            'assigned_to': {
                'id': lead.assigned_to.id if lead.assigned_to else None,
                'name': lead.assigned_to.get_full_name() if lead.assigned_to else 'Unassigned'
            }
        })
        
    except json.JSONDecodeError:
        return JsonResponse(
            {'status': 'error', 'message': 'Invalid JSON data'}, 
            status=400
        )
    except Lead.DoesNotExist:
        return JsonResponse(
            {'status': 'error', 'message': 'Lead not found'}, 
            status=404
        )
    except Exception as e:
        return JsonResponse(
            {'status': 'error', 'message': str(e)}, 
            status=500
        )


def is_media_member(user):
    """Check if user is in media team"""
    return user.role == 'MEDIA'

@login_required
@user_passes_test(is_media_member)
def media_dashboard(request):
    """Media team dashboard view"""
    if request.method == 'POST':
        form = LeadForm(request.POST)
        if form.is_valid():
            lead = form.save(commit=False)
            lead.source = form.cleaned_data.get('source')
            lead.custom_source = form.cleaned_data.get('custom_source', '')
            lead.save()
            messages.success(request, 'Lead added successfully!')
            return redirect('accounts:media_dashboard')
    else:
        form = LeadForm()
    
    # Show leads created recently (you can filter by media team if needed)
    leads = Lead.objects.all().order_by('-created_at')[:10]
    
    context = {
        'form': form,
        'leads': leads,
    }
    return render(request, 'accounts/media.html', context)


def is_operations(user):
    """Check if user is operations manager"""
    return user.role == 'OPS'

def operations_dashboard(request):
    """Operations manager dashboard view"""
    # Get all unassigned leads, leads assigned to admission managers/executives, and rejected leads
    leads = Lead.objects.filter(
        models.Q(assigned_to__isnull=True) | 
        models.Q(assigned_to__role__in=['ADM_MANAGER', 'ADM_EXEC']) |
        models.Q(processing_status='REJECTED')
    ).order_by('-created_at')
    
    # Get all admission managers and executives for the assignment dropdown
    admission_managers = User.objects.filter(role='ADM_MANAGER', is_active=True)
    admission_executives = User.objects.filter(role='ADM_EXEC', is_active=True)
    
    context = {
        'leads': leads,
        'admission_managers': admission_managers,
        'admission_executives': admission_executives,
        'priority_choices': Lead.PRIORITY_CHOICES,
        # Status is now free-text; keep template happy with empty list
        'status_choices': [],
    }
    return render(request, 'accounts/operations.html', context)


@login_required
@require_POST
def assign_lead(request):
    """Assign lead to admission manager"""
    try:
        data = json.loads(request.body)
        lead_id = data.get('lead_id')
        manager_id = data.get('manager_id')
        
        lead = Lead.objects.get(id=lead_id)
        manager = User.objects.get(id=manager_id, role='ADM_MANAGER')
        
        lead.assigned_to = manager
        lead.save()
        
        return JsonResponse({'status': 'success'})
    except (Lead.DoesNotExist, User.DoesNotExist):
        return JsonResponse({'status': 'error', 'message': 'Invalid lead or manager'}, status=400)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

@login_required
@require_POST
def forward_to_processing(request):
    """Forward registered leads to processing"""
    try:
        data = json.loads(request.body)
        lead_id = data.get('lead_id')
        
        lead = Lead.objects.get(id=lead_id)
        if lead.status != 'REGISTERED':
            return JsonResponse({
                'status': 'error', 
                'message': 'Only registered leads can be forwarded'
            }, status=400)
            
        lead.processing_status = 'FORWARDED'
        lead.processing_status_date = timezone.now()
        lead.save()
        
        return JsonResponse({'status': 'success'})
    except Lead.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Invalid lead'}, status=400)
    

@login_required
@require_POST
def update_lead_field(request):
    """Update any lead field for operations"""
    try:
        data = json.loads(request.body)
        lead_id = data.get('lead_id')
        field = data.get('field')
        value = data.get('value')
        
        lead = Lead.objects.get(id=lead_id)
        
        # Validate field updates
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
                
        elif field == 'program':
            lead.program = value if value != '' else None
        elif field == 'assigned_to':
            if value == '':
                # Unassign the lead
                lead.assigned_to = None
            else:
                try:
                    manager = User.objects.get(id=value, role='ADM_MANAGER')
                    lead.assigned_to = manager
                except User.DoesNotExist:
                    return JsonResponse({'status': 'error', 'message': 'Invalid manager'}, status=400)
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid field'}, status=400)
            
        lead.save()
        return JsonResponse({'status': 'success'})
        
    except Lead.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Lead not found'}, status=404)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    

def is_processing_executive(user):
    return user.role == 'PROCESSING'

@method_decorator([login_required, user_passes_test(is_processing_executive)], name='dispatch')
class ProcessingDashboard(TemplateView):
    template_name = 'accounts/processing_dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        # Forwarded leads (registrations tab)
        context['forwarded_leads'] = Lead.objects.filter(
            processing_status='FORWARDED'
        ).order_by('-processing_status_date')
        
        # Processing leads (in-progress tab)
        context['processing_leads'] = Lead.objects.filter(
            processing_status='PROCESSING',
            processing_executive=user
        ).order_by('-processing_status_date')
        
        return context

@login_required
@user_passes_test(is_processing_executive)
@require_POST
def accept_lead(request):
    try:
        data = json.loads(request.body)
        lead_id = data.get('lead_id')
        
        lead = Lead.objects.get(id=lead_id, processing_status='FORWARDED')
        lead.update_processing_status('PROCESSING', request.user)
        
        return JsonResponse({'status': 'success'})
    except Lead.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Invalid lead'}, status=400)


@login_required
@user_passes_test(is_processing_executive)
@require_POST
def complete_processing(request):
    try:
        data = json.loads(request.body)
        lead_id = data.get('lead_id')
        notes = data.get('notes', '')
        
        lead = Lead.objects.get(
            id=lead_id, 
            processing_status='PROCESSING',
            processing_executive=request.user
        )
        lead.processing_notes = notes
        lead.update_processing_status('COMPLETED')
        
        return JsonResponse({'status': 'success'})
    except Lead.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Invalid lead'}, status=400)    
    

# Processing Executive Views
def is_processing_executive(user):
    """Check if user is a processing executive"""
    return user.role == 'PROCESSING'

@method_decorator([login_required, user_passes_test(is_processing_executive)], name='dispatch')
class ProcessingDashboard(TemplateView):
    template_name = 'accounts/processing.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        # Forwarded leads (registrations tab)
        context['forwarded_leads'] = Lead.objects.filter(
            processing_status='FORWARDED'
        ).order_by('-processing_status_date')
        
        # Processing leads (in-progress tab)
        context['processing_leads'] = Lead.objects.filter(
            processing_status='PROCESSING',
            processing_executive=user
        ).order_by('-processing_status_date')
        
        # Completed leads
        context['completed_leads'] = Lead.objects.filter(
            processing_status='COMPLETED',
            processing_executive=user
        ).order_by('-processing_status_date')[:50]  # Limit to 50 most recent
        
        # Document status choices for the template
        context['document_status_choices'] = Lead.DOCUMENT_STATUS_CHOICES
        
        return context

@login_required
@user_passes_test(is_processing_executive)
@require_POST
def accept_lead(request):
    """Accept a forwarded lead for processing"""
    try:
        data = json.loads(request.body)
        lead_id = data.get('lead_id')
        
        lead = Lead.objects.get(id=lead_id, processing_status='FORWARDED')
        lead.processing_status = 'PROCESSING'
        lead.processing_executive = request.user
        lead.processing_status_date = timezone.now()
        lead.save()
        
        # Create processing update record
        ProcessingUpdate.objects.create(
            lead=lead,
            status='PROCESSING',
            changed_by=request.user,
            notes='Lead accepted for processing'
        )
        
        return JsonResponse({'status': 'success'})
    except Lead.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Invalid lead'}, status=400)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

@login_required
@user_passes_test(is_processing_executive)
@require_POST
def reject_lead(request):
    """Reject a forwarded lead"""
    try:
        data = json.loads(request.body)
        lead_id = data.get('lead_id')
        notes = data.get('notes', '')
        
        lead = Lead.objects.get(id=lead_id, processing_status='FORWARDED')
        lead.processing_status = 'REJECTED'
        lead.processing_status_date = timezone.now()
        lead.processing_notes = notes
        lead.save()
        
        # Create processing update record
        ProcessingUpdate.objects.create(
            lead=lead,
            status='REJECTED',
            changed_by=request.user,
            notes=notes or 'Lead rejected'
        )
        
        return JsonResponse({'status': 'success'})
    except Lead.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Invalid lead'}, status=400)

@login_required
@user_passes_test(is_processing_executive)
@require_POST
def complete_processing(request):
    """Mark processing as complete"""
    try:
        data = json.loads(request.body)
        lead_id = data.get('lead_id')
        notes = data.get('notes', '')
        
        lead = Lead.objects.get(
            id=lead_id, 
            processing_status='PROCESSING',
            processing_executive=request.user
        )
        lead.processing_status = 'COMPLETED'
        lead.processing_status_date = timezone.now()
        lead.processing_notes = notes
        lead.save()
        
        # Create processing update record
        ProcessingUpdate.objects.create(
            lead=lead,
            status='COMPLETED',
            changed_by=request.user,
            notes=notes or 'Processing completed'
        )
        
        return JsonResponse({'status': 'success'})
    except Lead.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Invalid lead'}, status=400)

@login_required
@user_passes_test(is_processing_executive)
@require_POST
def hold_processing(request):
    """Put processing on hold"""
    try:
        data = json.loads(request.body)
        lead_id = data.get('lead_id')
        notes = data.get('notes', '')
        
        lead = Lead.objects.get(
            id=lead_id, 
            processing_status='PROCESSING',
            processing_executive=request.user
        )
        lead.processing_status = 'ON_HOLD'
        lead.processing_status_date = timezone.now()
        lead.processing_notes = notes
        lead.save()
        
        # Create processing update record
        ProcessingUpdate.objects.create(
            lead=lead,
            status='ON_HOLD',
            changed_by=request.user,
            notes=notes or 'Processing put on hold'
        )
        
        return JsonResponse({'status': 'success'})
    except Lead.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Invalid lead'}, status=400)

@login_required
@user_passes_test(is_processing_executive)
@require_POST
def update_document_status(request):
    """Update document collection status"""
    try:
        data = json.loads(request.body)
        lead_id = data.get('lead_id')
        status = data.get('status')
        
        if status not in dict(Lead.DOCUMENT_STATUS_CHOICES).keys():
            return JsonResponse({'status': 'error', 'message': 'Invalid status'}, status=400)
        
        lead = Lead.objects.get(
            id=lead_id,
            processing_executive=request.user
        )
        lead.document_status = status
        lead.save()
        
        return JsonResponse({'status': 'success'})
    except Lead.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Invalid lead'}, status=400)

@login_required
@user_passes_test(is_processing_executive)
@require_POST
def update_processing_notes(request):
    """Update processing notes"""
    try:
        data = json.loads(request.body)
        lead_id = data.get('lead_id')
        notes = data.get('notes', '')
        
        lead = Lead.objects.get(id=lead_id)
        lead.processing_notes = notes
        lead.save()
        
        return JsonResponse({'status': 'success'})
    except Lead.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Lead not found'}, status=404)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

@login_required
@user_passes_test(is_processing_executive)
@require_POST
def reopen_lead(request):
    try:
        data = json.loads(request.body)
        lead_id = data.get('lead_id')
        
        lead = Lead.objects.get(id=lead_id)
        
        # Change status back to processing
        lead.processing_status = 'PROCESSING'
        lead.processing_status_date = timezone.now()
        lead.save()
        
        # Create processing update record
        ProcessingUpdate.objects.create(
            lead=lead,
            status='PROCESSING',
            changed_by=request.user,
            notes='Lead reopened for further processing'
        )
        
        return JsonResponse({'status': 'success'})
    except Lead.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Lead not found'}, status=404)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)    

@login_required
@require_POST
def add_lead(request):
    """Add a new lead and automatically assign it to the current user"""
    try:
        data = json.loads(request.body)
        
        # Validate required fields
        name = data.get('name', '').strip()
        phone = data.get('phone', '').strip()
        
        if not name or len(name) < 3:
            return JsonResponse({'status': 'error', 'message': 'Name must be at least 3 characters'}, status=400)
            
        if not phone or len(phone) < 10:
            return JsonResponse({'status': 'error', 'message': 'Phone must be at least 10 digits'}, status=400)
        
        # Create the lead
        lead = Lead.objects.create(
            name=name,
            phone=phone,
            email=data.get('email', '').strip() or None,
            priority=data.get('priority', 'MEDIUM'),
            status=data.get('status', 'ENQUIRY'),
            program=data.get('program', '').strip() or None,
            source=data.get('source', 'WHATSAPP'),
            location=data.get('location', '').strip() or None,
            remarks=data.get('remarks', '').strip() or None,
            assigned_to=request.user,  # Automatically assign to current user
            assigned_date=timezone.now()
        )
        
        return JsonResponse({
            'status': 'success',
            'message': 'Lead added successfully',
            'lead_id': lead.id
        })
        
    except json.JSONDecodeError:
        return JsonResponse({'status': 'error', 'message': 'Invalid JSON data'}, status=400)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

@login_required
def all_leads(request):
    query = request.GET.get('q', '')
    if query:
        leads = Lead.objects.filter(
            Q(name__icontains=query) |
            Q(phone__icontains=query) |
            Q(email__icontains=query) |
            Q(program__icontains=query) |
            Q(status__icontains=query) |
            Q(priority__icontains=query) |
            Q(source__icontains=query)    
        ).order_by('-created_at')
    else:
        leads = Lead.objects.all().order_by('-created_at')

    if request.method == 'POST':
        form = LeadForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('accounts:all_leads')
    else:
        form = LeadForm()

    return render(request, 'accounts/all_leads.html', {
        'leads': leads,
        'form': form,
        'query': query,
    }) 
@login_required
@require_http_methods(["POST"])
def import_leads_excel(request):
    try:
        # Determine data source: uploaded Excel or pasted CSV/TSV
        df = None
        pasted_text = request.POST.get('pasted_data', '').strip()

        if pasted_text:
            try:
                # Clean and normalize the pasted text
                pasted_text = pasted_text.strip()
                lines = pasted_text.split('\n')
                
                # Try different parsing strategies
                df = None
                
                # Strategy 1: Try to parse as CSV with headers
                try:
                    df = pd.read_csv(io.StringIO(pasted_text), sep=None, engine='python', header=0)
                    # Check if first row looks like data (not headers)
                    first_row_values = df.iloc[0].astype(str).tolist()
                    first_row_text = ' '.join(first_row_values).lower()
                    
                    # If first row contains common field names, it's likely headers
                    has_field_names = any(field in first_row_text for field in ['name', 'phone', 'mobile', 'contact', 'email', 'location', 'program', 'priority', 'status', 'source', 'remarks', 'notes'])
                    
                    # If first row looks like data (no field names), re-parse without headers so we don't lose the first line
                    if not has_field_names:
                        df = pd.read_csv(io.StringIO(pasted_text), sep=None, engine='python', header=None)
                        default_columns = ['name', 'phone', 'email', 'location', 'program', 'priority', 'status', 'source', 'remarks']
                        df.columns = default_columns[:len(df.columns)]
                except:
                    pass
                
                # Strategy 2: If Strategy 1 failed, try parsing as data without headers
                if df is None or len(df) == 0:
                    try:
                        df = pd.read_csv(io.StringIO(pasted_text), sep=None, engine='python', header=None)
                        # Assign default column names
                        default_columns = ['name', 'phone', 'email', 'location', 'program', 'priority', 'status', 'source', 'remarks']
                        df.columns = default_columns[:len(df.columns)]
                    except:
                        pass
                
                # Strategy 3: Manual parsing for single row
                if df is None or len(df) == 0:
                    if len(lines) == 1:
                        # Single row, try to split by comma or tab
                        line = lines[0].strip()
                        if '\t' in line:
                            values = line.split('\t')
                        else:
                            values = line.split(',')
                        
                        # Clean up values
                        values = [str(v).strip().strip('"\'') for v in values]
                        
                        # Create DataFrame with default column names
                        default_columns = ['name', 'phone', 'email', 'location', 'program', 'priority', 'status', 'source', 'remarks']
                        while len(values) < len(default_columns):
                            values.append('')
                        values = values[:len(default_columns)]
                        
                        df = pd.DataFrame([values], columns=default_columns)
                
                if df is None or len(df) == 0:
                    return JsonResponse({'status': 'error', 'message': 'Could not parse the pasted data. Please ensure it contains at least name and phone columns.'})
                    
            except Exception as e:
                return JsonResponse({'status': 'error', 'message': f'Error reading pasted data: {str(e)}'})
        elif 'excel_file' in request.FILES:
            excel_file = request.FILES['excel_file']
            # Validate file type
            if not excel_file.name.endswith(('.xlsx', '.xls')):
                return JsonResponse({'status': 'error', 'message': 'Please upload a valid Excel file (.xlsx or .xls)'})
            # Read Excel file
            try:
                df = pd.read_excel(excel_file)
            except Exception as e:
                return JsonResponse({'status': 'error', 'message': f'Error reading Excel file: {str(e)}'})
        else:
            return JsonResponse({'status': 'error', 'message': 'No data provided. Upload a file or paste rows.'})

        # Check if this is just a preview request
        preview_only = request.POST.get('preview_only') == 'true'

        if preview_only:
            # Create case-insensitive column mapping for preview
            column_mapping = {}
            for col in df.columns:
                col_lower = col.lower().strip()
                if 'name' in col_lower:
                    column_mapping['name'] = col
                elif 'phone' in col_lower or 'mobile' in col_lower or 'contact' in col_lower:
                    column_mapping['phone'] = col
                elif 'email' in col_lower:
                    column_mapping['email'] = col
                elif 'location' in col_lower or 'address' in col_lower:
                    column_mapping['location'] = col
                elif 'program' in col_lower or 'course' in col_lower:
                    column_mapping['program'] = col
                elif 'priority' in col_lower:
                    column_mapping['priority'] = col
                elif 'status' in col_lower:
                    column_mapping['status'] = col
                elif 'source' in col_lower:
                    column_mapping['source'] = col
                elif 'remarks' in col_lower or 'notes' in col_lower or 'comment' in col_lower:
                    column_mapping['remarks'] = col

            # Return preview data
            preview_data = {
                'headers': df.columns.tolist(),
                'rows': df.head(5).fillna('').values.tolist()
            }

            # Count valid rows for preview (rows with name and phone)
            valid_rows = 0
            for index, row in df.iterrows():
                name = str(row.get(column_mapping.get('name', 'name'), '')).strip()
                phone = str(row.get(column_mapping.get('phone', 'phone'), '')).strip()
                if name and phone and len(phone) >= 10:
                    valid_rows += 1

            stats = {
                'total_rows': len(df),
                'valid_rows': valid_rows,
                'invalid_rows': len(df) - valid_rows
            }

            return JsonResponse({
                'status': 'success',
                'preview_data': preview_data,
                'stats': stats
            })

        # Process and import data
        imported_count = 0
        errors = []

        # Create case-insensitive column mapping
        column_mapping = {}
        for col in df.columns:
            col_lower = col.lower().strip()
            if 'name' in col_lower:
                column_mapping['name'] = col
            elif 'phone' in col_lower or 'mobile' in col_lower or 'contact' in col_lower:
                column_mapping['phone'] = col
            elif 'email' in col_lower:
                column_mapping['email'] = col
            elif 'location' in col_lower or 'address' in col_lower:
                column_mapping['location'] = col
            elif 'program' in col_lower or 'course' in col_lower:
                column_mapping['program'] = col
            elif 'priority' in col_lower:
                column_mapping['priority'] = col
            elif 'status' in col_lower:
                column_mapping['status'] = col
            elif 'source' in col_lower:
                column_mapping['source'] = col
            elif 'remarks' in col_lower or 'notes' in col_lower or 'comment' in col_lower:
                column_mapping['remarks'] = col

        for index, row in df.iterrows():
            try:
                # Map Excel columns to Lead model fields using case-insensitive mapping
                lead_data = {
                    'name': str(row.get(column_mapping.get('name', 'name'), '')).strip(),
                    'phone': str(row.get(column_mapping.get('phone', 'phone'), '')).strip(),
                    'email': str(row.get(column_mapping.get('email', 'email'), '')).strip() or None,
                    'location': str(row.get(column_mapping.get('location', 'location'), '')).strip() or '',
                    'program': str(row.get(column_mapping.get('program', 'program'), '')).strip() or '',
                    'priority': str(row.get(column_mapping.get('priority', 'priority'), 'MEDIUM')).strip().upper(),
                    'status': str(row.get(column_mapping.get('status', 'status'), 'ENQUIRY')).strip(),
                    'source': str(row.get(column_mapping.get('source', 'source'), 'OTHER')).strip().upper(),
                    'remarks': str(row.get(column_mapping.get('remarks', 'remarks'), '')).strip() or '',
                    # Automatically assign to logged-in user
                    'assigned_to': request.user,
                    'assigned_date': timezone.now()
                }
                
                # Validate required fields
                if not lead_data['name'] or not lead_data['phone']:
                    errors.append(f"Row {index + 2}: Missing required fields (name or phone)")
                    continue
                
                # Validate phone length
                if len(lead_data['phone']) < 10:
                    errors.append(f"Row {index + 2}: Phone number too short")
                    continue
                
                # Validate priority and source choices (status is now free-text)
                valid_priorities = ['HIGH', 'MEDIUM', 'LOW']
                valid_sources = ['WHATSAPP', 'INSTAGRAM', 'WEBSITE', 'WALK_IN', 'AUTOMATION', 'OTHER']
                
                if lead_data['priority'] not in valid_priorities:
                    lead_data['priority'] = 'MEDIUM'
                
                # Status is now free-text, just ensure it's not empty
                if not lead_data['status']:
                    lead_data['status'] = 'ENQUIRY'
                
                if lead_data['source'] not in valid_sources:
                    lead_data['source'] = 'OTHER'
                
                # Create or update lead
                lead, created = Lead.objects.get_or_create(
                    phone=lead_data['phone'],
                    defaults=lead_data
                )
                
                if not created:
                    # Update existing lead - but preserve assignment unless it's the same user
                    for key, value in lead_data.items():
                        if key not in ['assigned_to', 'assigned_date']:  # Don't override assignment on updates
                            setattr(lead, key, value)
                    lead.save()
                
                imported_count += 1
                
            except Exception as e:
                errors.append(f"Row {index + 2}: {str(e)}")
                continue
        
        if errors and imported_count == 0:
            return JsonResponse({
                'status': 'error', 
                'message': 'No leads imported. Errors: ' + '; '.join(errors[:5])
            })
        
        message = f'Successfully imported {imported_count} leads'
        if errors:
            message += f' ({len(errors)} errors)'
        
        return JsonResponse({
            'status': 'success',
            'imported_count': imported_count,
            'error_count': len(errors),
            'message': message
        })
        
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': f'Unexpected error: {str(e)}'})
@login_required
def download_excel_template(request):
    """Download an Excel template for lead imports"""
    try:
        # Create a sample DataFrame with the expected columns
        sample_data = {
            'name': ['John Doe', 'Risheb.s'],
            'phone': ['1234567890', '7994631745'],
            'email': ['john@example.com', 'rishebs@example.com'],
            'location': ['New York', 'Kerala'],
            'program': ['MBA', 'BBA'],
            'priority': ['HIGH', 'MEDIUM'],
            'status': ['ENQUIRY', 'INTERESTED'],
            'source': ['WEBSITE', 'WHATSAPP'],
            'remarks': ['Interested in evening classes', 'Requested callback']
        }
        
        df = pd.DataFrame(sample_data)
        
        # Create response
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="leads_import_template.xlsx"'
        
        # Write DataFrame to Excel
        with pd.ExcelWriter(response, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Leads Template', index=False)
            
            # Get the worksheet and auto-adjust column widths
            worksheet = writer.sheets['Leads Template']
            for column in worksheet.columns:
                max_length = 0
                column_letter = column[0].column_letter
                for cell in column:
                    try:
                        if len(str(cell.value)) > max_length:
                            max_length = len(str(cell.value))
                    except:
                        pass
                adjusted_width = min(max_length + 2, 50)
                worksheet.column_dimensions[column_letter].width = adjusted_width
        
        return response
        
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': f'Error creating template: {str(e)}'})
        
@login_required
def delete_lead(request, lead_id):
    lead = get_object_or_404(Lead, id=lead_id)
    lead.delete()
    
    # Check if user is a Business Head (HOB) and redirect accordingly
    if request.user.role == 'BUSINESS_HEAD':
        return redirect('hob:dashboard')
    elif request.user.role == 'ADM_MANAGER':
        return redirect('/dashboard')
    elif request.user.role == 'OPS':
        return redirect('/operations')  
    elif request.user.role == 'ADM_EXEC':
        return redirect('/executive-dashboard')      
    else:
        return redirect('/all-leads')    
@login_required
@require_POST
def update_lead_field(request):
    """Update any lead field with enhanced assignment handling"""
    try:
        data = json.loads(request.body)
        lead_id = data.get('lead_id')
        field = data.get('field')
        value = data.get('value')
        
        if not lead_id or not field:
            return JsonResponse({'status': 'error', 'message': 'Missing required fields'}, status=400)
            
        lead = Lead.objects.get(id=lead_id)
        user = request.user
        
        # Validate and update fields
        if field == 'name':
            if len(value) < 3:
                return JsonResponse({'status': 'error', 'message': 'Name must be at least 3 characters'}, status=400)
            lead.name = value
            
        elif field == 'phone':
            if len(value) < 10:
                return JsonResponse({'status': 'error', 'message': 'Phone must be at least 10 digits'}, status=400)
            lead.phone = value
            
        elif field == 'priority':
            if value not in dict(Lead.PRIORITY_CHOICES).keys():
                return JsonResponse({'status': 'error', 'message': 'Invalid priority value'}, status=400)
            lead.priority = value
            
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
            
        elif field == 'source':
            if value not in dict(Lead.SOURCE_CHOICES).keys():
                return JsonResponse({'status': 'error', 'message': 'Invalid source value'}, status=400)
            lead.source = value

        elif field == 'remarks':
            previous = lead.remarks
            new_value = value if value != '' else None
            # Only record history if there is a change
            if previous != new_value:
                # Prevent duplicate logs when multiple rapid requests occur
                last = lead.remark_history.order_by('-changed_at').first()
                if not (last and last.previous_remarks == previous and last.new_remarks == new_value and last.changed_by_id == (user.id if user.is_authenticated else None)):
                    RemarkHistory.objects.create(
                        lead=lead,
                        previous_remarks=previous,
                        new_remarks=new_value,
                        changed_by=user if user.is_authenticated else None
                    )
            lead.remarks = new_value    
            
        elif field == 'assigned_to':
            # Handle assignment changes
            if value == '' or value is None:
                # Unassign the lead
                lead.assigned_to = None
                lead.assigned_date = None
            else:
                try:
                    # Check if assigning to manager or executive
                    assignee = User.objects.get(id=value, is_active=True)
                    
                    # Validate assignment based on user role
                    if assignee.role == 'ADM_MANAGER':
                        # Allow OPS, ADMIN, and BUSINESS_HEAD to assign to managers
                        if user.role not in ['OPS', 'ADMIN', 'BUSINESS_HEAD']:
                            return JsonResponse(
                                {'status': 'error', 'message': 'Only operations can assign to managers'}, 
                                status=403
                            )
                    elif assignee.role == 'ADM_EXEC':
                        # Allow ADM_MANAGER, OPS, ADMIN, and BUSINESS_HEAD to assign to executives
                        if user.role not in ['ADM_MANAGER', 'OPS', 'ADMIN', 'BUSINESS_HEAD']:
                            return JsonResponse(
                                {'status': 'error', 'message': 'Only managers can assign to executives'}, 
                                status=403
                            )
                    else:
                        return JsonResponse(
                            {'status': 'error', 'message': 'Can only assign to admission staff'}, 
                            status=400
                        )
                    
                    lead.assigned_to = assignee
                    # Set assignment date if not already set
                    if not lead.assigned_date:
                        from django.utils import timezone
                        lead.assigned_date = timezone.now()
                        
                except User.DoesNotExist:
                    return JsonResponse({'status': 'error', 'message': 'Invalid user assignment'}, status=400)
            
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid field'}, status=400)
            
        lead.save()
        
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
        return JsonResponse({'status': 'error', 'message': 'Lead not found'}, status=404)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

@login_required
def lead_details(request, lead_id):
    """View for displaying individual lead details"""
    try:
        lead = Lead.objects.get(id=lead_id)
    except Lead.DoesNotExist:
        messages.error(request, 'Lead not found.')
        return redirect('accounts:all_leads')
    
    context = {
        'lead': lead,
        'remarks_history': lead.remark_history.all(),
    }
    return render(request, 'accounts/leaddetails.html', context)




@login_required
def staff_reports_page(request):
    """Main staff reports page view - handles both display and report creation"""
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        # Handle AJAX report creation
        try:
            name = request.POST.get('name')
            heading = request.POST.get('heading')
            report_text = request.POST.get('report_text')
            report_date = request.POST.get('report_date')
            attached_file = request.FILES.get('attached_file')
            
            # Validate required fields
            if not all([name, heading, report_text, report_date]):
                return JsonResponse({
                    'status': 'error', 
                    'message': 'All fields are required'
                }, status=400)
            
            # Validate file size if provided (10MB limit)
            if attached_file:
                if attached_file.size > 10 * 1024 * 1024:  # 10MB
                    return JsonResponse({
                        'status': 'error', 
                        'message': 'File size too large. Maximum 10MB allowed.'
                    }, status=400)
                
                # Validate file types
                allowed_types = [
                    'application/pdf',
                    'application/msword',
                    'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                    'application/vnd.ms-excel',
                    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                    'image/jpeg',
                    'image/jpg',
                    'image/png',
                    'text/plain'
                ]
                
                if attached_file.content_type not in allowed_types:
                    return JsonResponse({
                        'status': 'error', 
                        'message': 'File type not allowed. Please upload PDF, Word, Excel, Image, or Text files.'
                    }, status=400)
            
            # Create the report
            report = DailyReport(
                user=request.user,
                name=name,
                heading=heading,
                report_text=report_text,
                report_date=report_date
            )
            
            # Handle file upload - Cloudinary will process this automatically
            if attached_file:
                report.attached_file = attached_file
            
            report.save()
            
            return JsonResponse({
                'status': 'success', 
                'message': 'Report created successfully',
                'report_id': report.id,
                'has_file': bool(attached_file)
            })
            
        except Exception as e:
            import traceback
            error_details = traceback.format_exc()
            print("Error creating report:", error_details)
            return JsonResponse({
                'status': 'error', 
                'message': f'Failed to create report: {str(e)}'
            }, status=500)
    
    # GET request - show the reports page
    reports = DailyReport.objects.filter(user=request.user).order_by('-report_date')
    
    context = {
        'reports': reports,
    }
    return render(request, 'accounts/staffreports.html', context)

@login_required
@require_http_methods(["GET"])
def get_report_details(request, report_id):
    """Get detailed information for a specific report"""
    try:
        report = get_object_or_404(DailyReport, id=report_id, user=request.user)
        
        report_data = {
            'id': report.id,
            'name': report.name,
            'heading': report.heading,
            'report_text': report.report_text,
            'report_date': report.report_date.isoformat(),
            'created_at': report.created_at.isoformat(),
            'updated_at': report.updated_at.isoformat(),
            'attached_file': bool(report.attached_file),  # Add file info
            'file_url': report.attached_file.url if report.attached_file else None,
            'file_name': report.get_file_name() if report.attached_file else None,
        }
        
        return JsonResponse(report_data)
        
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

@login_required
@require_http_methods(["PUT"])
def update_report(request, report_id):
    """Update an existing report"""
    try:
        report = get_object_or_404(DailyReport, id=report_id, user=request.user)
        
        # For PUT requests with form data
        name = request.POST.get('name')
        heading = request.POST.get('heading')
        report_text = request.POST.get('report_text')
        report_date = request.POST.get('report_date')
        attached_file = request.FILES.get('attached_file')
        remove_existing_file = request.POST.get('remove_existing_file') == 'true'
        
        # Update report fields
        if name:
            report.name = name
        if heading:
            report.heading = heading
        if report_text:
            report.report_text = report_text
        if report_date:
            report.report_date = report_date
        
        # Handle file operations
        if remove_existing_file:
            report.attached_file.delete(save=False)  # Remove current file
            report.attached_file = None
        
        if attached_file:
            # Remove old file if exists
            if report.attached_file:
                report.attached_file.delete(save=False)
            report.attached_file = attached_file
        
        report.save()
        
        return JsonResponse({
            'status': 'success', 
            'message': 'Report updated successfully',
            'report_id': report.id
        })
        
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

@login_required
@require_http_methods(["DELETE"])
def delete_report(request, report_id):
    """Delete a report"""
    try:
        report = get_object_or_404(DailyReport, id=report_id, user=request.user)
        report.delete()
        
        return JsonResponse({
            'status': 'success', 
            'message': 'Report deleted successfully'
        })
        
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500) 





@login_required
@require_http_methods(["POST"])
def create_micro_work(request):
    """Create a new micro work"""
    try:
        job_title = request.POST.get('job_title')
        description = request.POST.get('description')
        time_required = request.POST.get('time_required')
        
        # Validate required fields
        if not all([job_title, description, time_required]):
            return JsonResponse({
                'status': 'error', 
                'message': 'All fields are required'
            }, status=400)
        
        # Create the micro work
        micro_work = MicroWork(
            user=request.user,
            job_title=job_title,
            description=description,
            time_required=time_required
        )
        micro_work.save()
        
        return JsonResponse({
            'status': 'success', 
            'message': 'Micro work added successfully',
            'work_id': micro_work.id
        })
        
    except Exception as e:
        return JsonResponse({
            'status': 'error', 
            'message': f'Failed to add micro work: {str(e)}'
        }, status=500)

@login_required
@require_http_methods(["POST"])
def mark_micro_work_completed(request, work_id):
    """Mark a micro work as completed"""
    try:
        micro_work = get_object_or_404(MicroWork, id=work_id, user=request.user)
        micro_work.mark_completed()
        
        return JsonResponse({
            'status': 'success', 
            'message': 'Micro work marked as completed',
            'work_id': micro_work.id
        })
        
    except Exception as e:
        return JsonResponse({
            'status': 'error', 
            'message': str(e)
        }, status=500)

@login_required
@require_http_methods(["GET"])
def get_micro_works(request):
    """Get all micro works for the current user"""
    try:
        micro_works = MicroWork.objects.filter(user=request.user).order_by('-created_at')
        
        # India timezone
        ist = pytz.timezone('Asia/Kolkata')
        
        works_data = []
        for work in micro_works:
            # Convert UTC times to IST
            created_at_ist = work.created_at.astimezone(ist) if work.created_at else None
            completed_at_ist = work.completed_at.astimezone(ist) if work.completed_at else None
            
            works_data.append({
                'id': work.id,
                'job_title': work.job_title,
                'description': work.description,
                'time_required': work.time_required,
                'status': work.status,
                'created_at': work.created_at.isoformat(),
                'created_date_display': created_at_ist.strftime('%b %d, %Y') if created_at_ist else '',
                'created_time_display': created_at_ist.strftime('%I:%M %p') if created_at_ist else '',
                'completed_at': work.completed_at.isoformat() if work.completed_at else None,
                'completed_date_display': completed_at_ist.strftime('%b %d, %Y') if completed_at_ist else None,
                'completed_time_display': completed_at_ist.strftime('%I:%M %p') if completed_at_ist else None,
                'is_completed': work.is_completed
            })
        
        return JsonResponse({
            'status': 'success',
            'micro_works': works_data
        })
        
    except Exception as e:
        return JsonResponse({
            'status': 'error', 
            'message': str(e)
        }, status=500)

@login_required
@require_http_methods(["DELETE"])
def delete_micro_work(request, work_id):
    """Delete a micro work"""
    try:
        micro_work = get_object_or_404(MicroWork, id=work_id, user=request.user)
        micro_work.delete()
        
        return JsonResponse({
            'status': 'success', 
            'message': 'Micro work deleted successfully'
        })
        
    except Exception as e:
        return JsonResponse({
            'status': 'error', 
            'message': str(e)
        }, status=500)