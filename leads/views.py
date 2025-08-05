from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
import json
from .models import Lead


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
        
        if new_status in dict(Lead.STATUS_CHOICES).keys():
            lead.status = new_status
            lead.save()
            return JsonResponse({'status': 'success'})
        return JsonResponse({'status': 'error', 'message': 'Invalid status'}, status=400)
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
        
        if new_program in dict(Lead.PROGRAM_CHOICES).keys() or new_program == '':
            lead.program = new_program if new_program != '' else None
            lead.save()
            return JsonResponse({'status': 'success'})
        return JsonResponse({'status': 'error', 'message': 'Invalid program'}, status=400)
    except Lead.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Lead not found'}, status=404)
    except json.JSONDecodeError:
        return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
    

 