from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import VoxbayCallLog
from datetime import datetime

@csrf_exempt
def voxbay_webhook(request):
    if request.method == "POST":
        data = request.POST

        VoxbayCallLog.objects.create(
            call_uuid=data.get("CallUUID"),
            caller_number=data.get("callerNumber"),
            agent_number=data.get("AgentNumber"),
            call_status=data.get("callStatus"),
            duration=data.get("totalCallDuration") or data.get("duration"),
            recording_url=data.get("recording_URL"),
        )

        return HttpResponse("success")

    return HttpResponse("Invalid request")