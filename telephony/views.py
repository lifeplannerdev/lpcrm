import json
import logging
import requests
from datetime import datetime

from django.db.models import Avg, Q
from django.http import HttpResponse

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import VoxbayCallLog
from .serializers import (
    VoxbayCallLogSerializer,
    CallStatsSerializer,
    ClickToCallSerializer,
)

logger = logging.getLogger(__name__)

VOXBAY_CLICK_TO_CALL_URL = "https://x.voxbay.com/api/click_to_call"



def _parse_dt(date_str, time_str=None):
    if not date_str:
        return None
    combined = f"{date_str} {time_str}".strip() if time_str else date_str.strip()
    for fmt in (
        "%Y/%m/%d %H:%M:%S",
        "%Y-%m-%d %H:%M:%S",
        "%Y/%m/%d",
        "%Y-%m-%d",
    ):
        try:
            return datetime.strptime(combined, fmt)
        except ValueError:
            continue
    return None


def _safe_int(val):
    try:
        return int(val) if val not in (None, "", "None") else None
    except (ValueError, TypeError):
        return None


def _date_filter(qs, request):
    """Apply from/to date filters on created_at from query params."""
    from django.utils.dateparse import parse_datetime
    from_str = request.query_params.get("from")
    to_str   = request.query_params.get("to")
    if from_str:
        dt = parse_datetime(from_str)
        if dt:
            qs = qs.filter(created_at__gte=dt)
    if to_str:
        dt = parse_datetime(to_str)
        if dt:
            qs = qs.filter(created_at__lte=dt)
    return qs



class VoxbayWebhookView(APIView):
    permission_classes = [AllowAny]  
    authentication_classes = []      

    def post(self, request):
        if request.content_type and "application/json" in request.content_type:
            data = request.data  
        else:
            data = request.data   

        logger.info(f"[Voxbay Webhook] {dict(data)}")

        call_type = "outgoing" if (data.get("extension") or data.get("destination")) else "incoming"

        call_uuid  = data.get("CallUUID") or data.get("callUUID") or data.get("callUUlD")
        call_date  = data.get("callDate") or data.get("date")
        call_start = _parse_dt(call_date, data.get("callStartTime"))
        call_end   = _parse_dt(call_date, data.get("callEndTime"))

    
        defaults = {}

        def _set(key, val):
            if val not in (None, "", "None"):
                defaults[key] = val

        _set("call_type",             call_type)
        _set("call_status",           data.get("callStatus") or data.get("status"))
        _set("duration",              _safe_int(data.get("totalCallDuration") or data.get("duration")))
        _set("conversation_duration", _safe_int(data.get("conversationDuration")))
        _set("recording_url",         data.get("recording_URL") or data.get("recording_url"))
        if call_start: defaults["call_start"] = call_start
        if call_end:   defaults["call_end"]   = call_end

        if call_type == "incoming":
            _set("called_number",       data.get("calledNumber"))
            _set("caller_number",       data.get("callerNumber"))
            _set("agent_number",        data.get("AgentNumber") or data.get("agentNumber"))
            _set("dtmf",                data.get("dtmf"))
            _set("transferred_number",  data.get("transferredNumber"))
        else:
            _set("extension",     data.get("extension"))
            _set("destination",   data.get("destination"))
            _set("caller_id",     data.get("callerid"))
            _set("caller_number", data.get("callerid"))  # mirror for unified search

        if call_uuid:
            VoxbayCallLog.objects.update_or_create(
                call_uuid=call_uuid,
                defaults=defaults,
            )
        else:
            VoxbayCallLog.objects.create(call_uuid=call_uuid, **defaults)

        return HttpResponse("success", content_type="text/plain")



class CallLogListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        qs = VoxbayCallLog.objects.all()

        # Date range
        qs = _date_filter(qs, request)

        # Type filter
        call_type = request.query_params.get("call_type")
        if call_type in ("incoming", "outgoing"):
            qs = qs.filter(call_type=call_type)

        # Status filter
        call_status = request.query_params.get("call_status")
        if call_status:
            qs = qs.filter(call_status__iexact=call_status)

        # Search
        search = request.query_params.get("search", "").strip()
        if search:
            qs = qs.filter(
                Q(caller_number__icontains=search)  |
                Q(called_number__icontains=search)  |
                Q(agent_number__icontains=search)   |
                Q(destination__icontains=search)    |
                Q(call_uuid__icontains=search)
            )

        # Ordering
        ordering = request.query_params.get("ordering", "-created_at")
        allowed_orderings = {"created_at", "-created_at", "duration", "-duration", "call_status"}
        if ordering in allowed_orderings:
            qs = qs.order_by(ordering)

        serializer = VoxbayCallLogSerializer(qs, many=True)
        return Response(serializer.data)



class CallStatsView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        qs = VoxbayCallLog.objects.all()
        qs = _date_filter(qs, request)

        total      = qs.count()
        answered   = qs.filter(call_status="ANSWERED").count()
        missed     = qs.filter(call_status__in=["NOANSWER", "CANCEL", "MISSED"]).count()
        busy       = qs.filter(call_status="BUSY").count()
        congestion = qs.filter(call_status="CONGESTION").count()
        incoming   = qs.filter(call_type="incoming").count()
        outgoing   = qs.filter(call_type="outgoing").count()

        avg_result = qs.filter(
            call_status="ANSWERED",
            duration__isnull=False
        ).aggregate(avg=Avg("duration"))
        avg_duration = round(avg_result["avg"], 1) if avg_result["avg"] else 0.0

        data = {
            "total":        total,
            "answered":     answered,
            "missed":       missed,
            "busy":         busy,
            "congestion":   congestion,
            "incoming":     incoming,
            "outgoing":     outgoing,
            "avg_duration": avg_duration,
            "success_rate": round((answered / total * 100), 1) if total else 0.0,
        }

        serializer = CallStatsSerializer(data)
        return Response(serializer.data)



class ClickToCallView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ClickToCallSerializer(data=request.data)

        # Serializer validates required fields and types automatically
        if not serializer.is_valid():
            return Response(
                {"error": "Validation failed", "details": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

        validated = serializer.validated_data

        params = {
            "id_dept":     0,
            "uid":         validated["uid"],
            "upin":        validated["upin"],
            "user_no":     validated["user_no"],
            "destination": validated["destination"],
            "callerid":    validated["callerid"],
        }
        if validated.get("source"):
            params["source"] = validated["source"]

        try:
            resp = requests.get(VOXBAY_CLICK_TO_CALL_URL, params=params, timeout=10)
            return Response({
                "success":          resp.status_code == 200,
                "voxbay_response":  resp.text,
                "status_code":      resp.status_code,
            })
        except requests.Timeout:
            return Response({"error": "Voxbay API timed out"}, status=status.HTTP_504_GATEWAY_TIMEOUT)
        except requests.RequestException as e:
            logger.error(f"[Click-to-Call] {e}")
            return Response({"error": str(e)}, status=status.HTTP_502_BAD_GATEWAY)