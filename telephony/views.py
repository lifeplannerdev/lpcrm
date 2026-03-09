import json
import logging
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.dateparse import parse_datetime
from .models import VoxbayCallLog
from datetime import datetime

logger = logging.getLogger(__name__)


@csrf_exempt
def voxbay_webhook(request):
    """Receives call events from Voxbay and saves them to DB."""
    if request.method != "POST":
        return HttpResponse("Invalid request", status=405)

    content_type = request.content_type or ""
    if "application/json" in content_type:
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return HttpResponse("Invalid JSON", status=400)
    else:
        data = request.POST

    logger.info(f"Voxbay webhook: {dict(data)}")

    call_uuid = data.get("CallUUID") or data.get("callUUID")

    call_start = call_end = None
    call_date       = data.get("callDate") or data.get("date")
    call_start_time = data.get("callStartTime")
    call_end_time   = data.get("callEndTime")

    for fmt in ("%Y/%m/%d %H:%M:%S", "%Y-%m-%d %H:%M:%S"):
        try:
            if call_date and call_start_time:
                call_start = datetime.strptime(f"{call_date} {call_start_time}", fmt); break
            elif call_date:
                call_start = datetime.strptime(call_date, fmt); break
        except ValueError:
            continue

    for fmt in ("%Y/%m/%d %H:%M:%S", "%Y-%m-%d %H:%M:%S"):
        try:
            if call_date and call_end_time:
                call_end = datetime.strptime(f"{call_date} {call_end_time}", fmt); break
        except ValueError:
            continue

    duration = data.get("totalCallDuration") or data.get("duration") or data.get("conversationDuration")
    try:
        duration = int(duration) if duration else None
    except (ValueError, TypeError):
        duration = None

    defaults = {
        "caller_number": data.get("callerNumber"),
        "agent_number":  data.get("AgentNumber") or data.get("agentNumber") or data.get("extension"),
        "call_status":   data.get("callStatus") or data.get("status"),
        "duration":      duration,
        "recording_url": data.get("recording_URL") or data.get("recording_url"),
        "call_start":    call_start,
        "call_end":      call_end,
    }

    if call_uuid:
        VoxbayCallLog.objects.update_or_create(call_uuid=call_uuid, defaults=defaults)
    else:
        VoxbayCallLog.objects.create(**defaults)

    return HttpResponse("success")


def call_logs_list(request):
    """Returns call logs as JSON for the frontend analytics page."""
    if request.method != "GET":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    qs = VoxbayCallLog.objects.all().order_by("-created_at")

    from_str = request.GET.get("from")
    to_str   = request.GET.get("to")
    if from_str:
        try:
            qs = qs.filter(created_at__gte=parse_datetime(from_str))
        except Exception:
            pass
    if to_str:
        try:
            qs = qs.filter(created_at__lte=parse_datetime(to_str))
        except Exception:
            pass

    data = list(qs.values(
        "call_uuid", "caller_number", "agent_number",
        "call_status", "duration", "recording_url",
        "call_start", "call_end", "created_at",
    ))

    for row in data:
        for key in ("call_start", "call_end", "created_at"):
            if row[key]:
                row[key] = row[key].isoformat()

    return JsonResponse(data, safe=False)