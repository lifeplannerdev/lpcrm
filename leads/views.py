from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
import json
from .models import Lead
from .models import RemarkHistory


@login_required
@require_POST
def update_priority(request, lead_id):
    try:
        data = json.loads(request.body)
        lead = Lead.objects.get(id=lead_id, assigned_to=request.user)
        new_priority = data.get('priority')
        
        if new_priority in dict(Lead.PRIORITY_CHOICES).keys():
            lead.priority = new_priority
            lead.save()
            return JsonResponse({'status': 'success'})
        return JsonResponse({'status': 'error', 'message': 'Invalid priority'}, status=400)
    except Lead.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Lead not found'}, status=404)
    except json.JSONDecodeError:
        return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)

@login_required
@require_POST
def update_status(request, lead_id):
    try:
        data = json.loads(request.body)
        lead = Lead.objects.get(id=lead_id, assigned_to=request.user)
        new_status = data.get('status')
        
        # Remove the choices validation since status is now free-form text
        # Only validate that it's not empty
        if new_status and new_status.strip():
            lead.status = new_status.strip()
            lead.save()
            return JsonResponse({'status': 'success'})
        return JsonResponse({'status': 'error', 'message': 'Status cannot be empty'}, status=400)
    except Lead.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Lead not found'}, status=404)
    except json.JSONDecodeError:
        return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)

@login_required
@require_POST
def update_program(request, lead_id):
    try:
        data = json.loads(request.body)
        lead = Lead.objects.get(id=lead_id, assigned_to=request.user)
        new_program = data.get('program')
        lead.program = new_program if new_program != '' else None
        lead.save()
        return JsonResponse({'status': 'success'})
    except Lead.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Lead not found'}, status=404)
    except json.JSONDecodeError:
        return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)


@login_required
@require_POST
def update_lead(request, lead_id):
    try:
        data = json.loads(request.body)
        lead = Lead.objects.get(id=lead_id)
        
        # Update lead fields
        lead.name = data.get('name')
        lead.phone = data.get('phone')
        lead.email = data.get('email')
        lead.location = data.get('location')
        lead.source = data.get('source')
        lead.program = data.get('program')
        lead.priority = data.get('priority')
        lead.status = data.get('status')  # Now accepts any text value

        # Record remark history if remarks changed
        previous_remarks = lead.remarks
        new_remarks = data.get('remarks')
        if previous_remarks != new_remarks:
            last = lead.remark_history.order_by('-changed_at').first()
            user_id = request.user.id if request.user.is_authenticated else None
            if not (last and last.previous_remarks == previous_remarks and last.new_remarks == new_remarks and (last.changed_by_id == user_id)):
                RemarkHistory.objects.create(
                    lead=lead,
                    previous_remarks=previous_remarks,
                    new_remarks=new_remarks,
                    changed_by=request.user if request.user.is_authenticated else None
                )
        lead.remarks = new_remarks
        
        lead.save()
        return JsonResponse({'status': 'success'})
    except Lead.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Lead not found'}, status=404)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)