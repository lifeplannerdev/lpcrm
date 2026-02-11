from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from .models import CallLog


class VoxbayWebhookAPIView(APIView):

    authentication_classes = []  # disable DRF auth (Voxbay won't send JWT)
    permission_classes = []      # allow public access (we’ll secure manually)

    def post(self, request, *args, **kwargs):

        # OPTIONAL: Verify secret token (if Voxbay provides one)
        token = request.headers.get("X-VOXBAY-TOKEN")
        if settings.VOXBAY_WEBHOOK_SECRET and token != settings.VOXBAY_WEBHOOK_SECRET:
            return Response({"error": "Unauthorized"}, status=status.HTTP_403_FORBIDDEN)

        data = request.data

        try:
            CallLog.objects.update_or_create(
                call_id=data.get("call_id"),
                defaults={
                    "caller_number": data.get("caller"),
                    "agent_number": data.get("agent"),
                    "status": data.get("status"),
                    "duration": data.get("duration"),
                    "recording_url": data.get("recording_url"),
                    "raw_data": data
                }
            )

            return Response({"message": "Webhook received successfully"}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
