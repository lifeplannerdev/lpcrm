from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import User
from django.contrib import messages
from leads.models import Lead
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



def landing_page(request):
    """Render the role selection landing page"""
    return render(request, 'accounts/landing.html')


@require_POST
def quick_login(request):
    """Handle role-based quick login authentication"""
    request.session.cookie_name = settings.SESSION_COOKIE_NAME
    request.session.cookie_path = settings.SESSION_COOKIE_PATH
    
    role = request.POST.get('role')
    password = request.POST.get('password')
    
    # Validate required fields
    if not role or not password:
        messages.error(request, "Role and password are required")
        return redirect('accounts:landing')

    try:
        users = User.objects.filter(role=role, is_active=True)
        
        if not users.exists():
            messages.error(request, "No active users found with this role")
            return redirect('accounts:landing')
        
        # Try authenticating each user with the provided password
        authenticated_user = None
        for user in users:
            auth_user = authenticate(
                request,
                username=user.username,
                password=password
            )
            if auth_user is not None:
                authenticated_user = auth_user
                break
        
        if authenticated_user:
            login(request, authenticated_user)
            
            # Role-based redirection - UPDATED THIS SECTION
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
            # Changed to use namespace
            # Add other role redirects as needed
            
            # Default redirect if role not specifically handled
            return redirect('accounts:landing')
            
        messages.error(request, "Invalid password for this role")
        
    except Exception as e:
        messages.error(request, f"An error occurred during login: {str(e)}")  # More detailed error
        # Consider logging the actual error for admin review
    
    return redirect('accounts:landing')






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
        if not (user.role in ['ADM_MANAGER', 'OPS', 'ADMIN'] or 
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
        'status_choices': Lead.STATUS_CHOICES,
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
            if value in dict(Lead.STATUS_CHOICES).keys():
                lead.status = value
            else:
                return JsonResponse({'status': 'error', 'message': 'Invalid status'}, status=400)
                
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
def delete_lead(request, lead_id):
    lead = get_object_or_404(Lead, id=lead_id)
    lead.delete()
    return redirect('accounts:all_leads') 
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
            if value not in dict(Lead.STATUS_CHOICES).keys():
                return JsonResponse({'status': 'error', 'message': 'Invalid status value'}, status=400)
            lead.status = value
            
            # Update registration date if status changed to REGISTERED
            if value == 'REGISTERED' and not lead.registration_date:
                from django.utils import timezone
                lead.registration_date = timezone.now()
            
        elif field == 'program':
            lead.program = value if value != '' else None
            
        elif field == 'source':
            if value not in dict(Lead.SOURCE_CHOICES).keys():
                return JsonResponse({'status': 'error', 'message': 'Invalid source value'}, status=400)
            lead.source = value
            
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
                        # Only operations or admins can assign to managers
                        if user.role not in ['OPS', 'ADMIN']:
                            return JsonResponse(
                                {'status': 'error', 'message': 'Only operations can assign to managers'}, 
                                status=403
                            )
                    elif assignee.role == 'ADM_EXEC':
                        # Only managers or operations can assign to executives
                        if user.role not in ['ADM_MANAGER', 'OPS', 'ADMIN']:
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