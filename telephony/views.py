import logging
import requests
from datetime import datetime

from django.db.models import Avg, Q
from django.http import HttpResponse

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

from .models import VoxbayCallLog
from .serializers import (
    VoxbayCallLogSerializer,
    CallStatsSerializer,
    ClickToCallSerializer,
)

logger = logging.getLogger(__name__)

VOXBAY_CLICK_TO_CALL_URL = "https://x.voxbay.com/api/click_to_call"
VOXBAY_RECORDING_BASE_URL = "https://x.voxbay.com:81/callcenter/"


# Helpers

def _parse_dt(date_str, time_str=None):
    if not date_str:
        return None
    combined = f"{date_str} {time_str}".strip() if time_str else date_str.strip()
    for fmt in (
        "%Y/%m/%d %H:%M:%S",
        "%Y-%m-%d %H:%M:%S",
        "%Y/%m/%d %H:%M",
        "%Y-%m-%d %H:%M",
        "%Y/%m/%d",
        "%Y-%m-%d",
    ):
        try:
            return datetime.strptime(combined, fmt)
        except ValueError:
            continue
    logger.warning(f"[Voxbay] Could not parse datetime: '{combined}'")
    return None


def _safe_int(val):
    try:
        return int(val) if val not in (None, "", "None") else None
    except (ValueError, TypeError):
        return None


def _resolve_recording_url(raw_url):
    """
    If the recording URL is a bare filename (no http), prepend the base URL.
    """
    if not raw_url:
        return None
    raw_url = raw_url.strip()
    if raw_url.startswith("http://") or raw_url.startswith("https://"):
        return raw_url
    return VOXBAY_RECORDING_BASE_URL + raw_url


def _date_filter(qs, request):
    """Apply from/to date range filters on call_start (falls back to created_at)."""
    from django.utils.dateparse import parse_datetime, parse_date
    from_str = request.query_params.get("from")
    to_str   = request.query_params.get("to")

    def _parse(s):
        return parse_datetime(s) or (
            datetime.combine(parse_date(s), datetime.min.time()) if parse_date(s) else None
        )

    if from_str:
        dt = _parse(from_str)
        if dt:
            qs = qs.filter(created_at__gte=dt)
    if to_str:
        dt = _parse(to_str)
        if dt:
            qs = qs.filter(created_at__lte=dt)
    return qs


# Webhook  (receives ALL Voxbay events for both Incoming and Outgoing calls)

class VoxbayWebhookView(APIView):
    permission_classes    = [AllowAny]
    authentication_classes = []

    def post(self, request):
        data = request.data 
        logger.info(f"[Voxbay Webhook] payload={dict(data)}")

        call_type = (
            "outgoing"
            if (data.get("extension") or data.get("destination"))
            else "incoming"
        )

        call_uuid = (
            data.get("CallUUID")
            or data.get("callUUID")
            or data.get("callUUlD")  
        )

        call_date  = data.get("callDate") or data.get("date")
        call_start = _parse_dt(call_date, data.get("callStartTime"))
        call_end   = _parse_dt(call_date, data.get("callEndTime"))

        defaults = {}

        def _set(key, val):
            if val not in (None, "", "None"):
                defaults[key] = val

        _set("call_type",             call_type)
        _set("call_status",           data.get("callStatus") or data.get("status"))
        _set("duration",              _safe_int(
                                          data.get("totalCallDuration") or data.get("duration")
                                      ))
        _set("conversation_duration", _safe_int(data.get("conversationDuration")))
        _set("recording_url",         _resolve_recording_url(
                                          data.get("recording_URL") or data.get("recording_url")
                                      ))
        if call_start:
            defaults["call_start"] = call_start
        if call_end:
            defaults["call_end"] = call_end

        if call_type == "incoming":
            # Fields present across one or more incoming events
            _set("called_number",      data.get("calledNumber"))
            _set("caller_number",      data.get("callerNumber"))
            _set("agent_number",       data.get("AgentNumber") or data.get("agentNumber"))
            _set("dtmf",               data.get("dtmf"))
            _set("transferred_number", data.get("transferredNumber"))
        else:
            # Outgoing – Event 1 & Event 2
            _set("extension",     data.get("extension"))
            _set("destination",   data.get("destination"))
            _set("caller_id",     data.get("callerid"))
            # Mirror callerid → caller_number so unified search works
            _set("caller_number", data.get("callerid"))


        if call_uuid:
            obj, created = VoxbayCallLog.objects.update_or_create(
                call_uuid=call_uuid,
                defaults=defaults,
            )
            logger.info(
                f"[Voxbay Webhook] {'created' if created else 'updated'} "
                f"CallLog id={obj.id} uuid={call_uuid}"
            )
        else:
            obj = VoxbayCallLog.objects.create(**defaults)
            logger.warning(
                f"[Voxbay Webhook] no UUID in payload – created new row id={obj.id}"
            )

        return HttpResponse("success", content_type="text/plain")



# Call Log List  (read-only, with filtering / search / ordering / pagination)


class CallLogListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        qs = VoxbayCallLog.objects.all()

        # Date range
        qs = _date_filter(qs, request)

        # Call type
        call_type = request.query_params.get("call_type")
        if call_type in ("incoming", "outgoing"):
            qs = qs.filter(call_type=call_type)

        # Call status
        call_status = request.query_params.get("call_status")
        if call_status:
            qs = qs.filter(call_status__iexact=call_status)

        # Full-text search across key number fields
        search = request.query_params.get("search", "").strip()
        if search:
            qs = qs.filter(
                Q(caller_number__icontains=search)  |
                Q(called_number__icontains=search)  |
                Q(agent_number__icontains=search)   |
                Q(destination__icontains=search)    |
                Q(extension__icontains=search)      |
                Q(call_uuid__icontains=search)
            )

        # Ordering
        ordering = request.query_params.get("ordering", "-created_at")
        allowed_orderings = {
            "created_at", "-created_at",
            "duration",   "-duration",
            "call_status",
        }
        if ordering in allowed_orderings:
            qs = qs.order_by(ordering)

        # Simple pagination
        try:
            page      = max(1, int(request.query_params.get("page", 1)))
            page_size = min(200, max(1, int(request.query_params.get("page_size", 20))))
        except (ValueError, TypeError):
            page, page_size = 1, 20

        total  = qs.count()
        offset = (page - 1) * page_size
        qs     = qs[offset: offset + page_size]

        serializer = VoxbayCallLogSerializer(qs, many=True)
        return Response({
            "count":     total,
            "page":      page,
            "page_size": page_size,
            "results":   serializer.data,
        })


# Call Log Detail  (fetch single record by DB id or call_uuid)


class CallLogDetailView(APIView):
    permission_classes = [AllowAny]

    def _get_object(self, lookup, by_uuid=False):
        try:
            if by_uuid:
                return VoxbayCallLog.objects.get(call_uuid=lookup)
            return VoxbayCallLog.objects.get(pk=lookup)
        except VoxbayCallLog.DoesNotExist:
            return None

    def get(self, request, pk=None, uuid=None):
        obj = self._get_object(uuid, by_uuid=True) if uuid else self._get_object(pk)
        if obj is None:
            return Response({"error": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        return Response(VoxbayCallLogSerializer(obj).data)


# Call Statistics


class CallStatsView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        qs = VoxbayCallLog.objects.all()
        qs = _date_filter(qs, request)

        # Optional direction filter
        call_type = request.query_params.get("call_type")
        if call_type in ("incoming", "outgoing"):
            qs = qs.filter(call_type=call_type)

        total       = qs.count()
        answered    = qs.filter(call_status="ANSWERED").count()
        # NOANSWER, CANCEL, MISSED all represent an unanswered call
        missed      = qs.filter(call_status__in=["NOANSWER", "CANCEL", "MISSED"]).count()
        busy        = qs.filter(call_status="BUSY").count()
        congestion  = qs.filter(call_status="CONGESTION").count()
        chanunavail = qs.filter(call_status="CHANUNAVAIL").count()
        incoming    = qs.filter(call_type="incoming").count()
        outgoing    = qs.filter(call_type="outgoing").count()

        avg_result = qs.filter(
            call_status="ANSWERED",
            duration__isnull=False,
        ).aggregate(avg=Avg("duration"))
        avg_duration = round(avg_result["avg"], 1) if avg_result["avg"] else 0.0

        data = {
            "total":        total,
            "answered":     answered,
            "missed":       missed,
            "busy":         busy,
            "congestion":   congestion,
            "chanunavail":  chanunavail,
            "incoming":     incoming,
            "outgoing":     outgoing,
            "avg_duration": avg_duration,
            "success_rate": round(answered / total * 100, 1) if total else 0.0,
        }

        serializer = CallStatsSerializer(data)
        return Response(serializer.data)



# Click-to-Call  (proxies the request to Voxbay)


class ClickToCallView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ClickToCallSerializer(data=request.data)
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
        # FORMAT 2: mobile-to-mobile requires source
        if validated.get("source"):
            params["source"] = validated["source"]

        logger.info(f"[Click-to-Call] params={params}")

        try:
            resp = requests.get(VOXBAY_CLICK_TO_CALL_URL, params=params, timeout=10)
            resp.raise_for_status()
            return Response({
                "success":         True,
                "voxbay_response": resp.text,
                "status_code":     resp.status_code,
            })
        except requests.Timeout:
            logger.error("[Click-to-Call] Voxbay API timed out")
            return Response(
                {"error": "Voxbay API timed out"},
                status=status.HTTP_504_GATEWAY_TIMEOUT,
            )
        except requests.HTTPError as e:
            logger.error(f"[Click-to-Call] HTTP error: {e}")
            return Response(
                {
                    "success":         False,
                    "voxbay_response": resp.text,
                    "status_code":     resp.status_code,
                },
                status=status.HTTP_502_BAD_GATEWAY,
            )
        except requests.RequestException as e:
            logger.error(f"[Click-to-Call] RequestException: {e}")
            return Response(
                {"error": str(e)},
                status=status.HTTP_502_BAD_GATEWAY,
            )