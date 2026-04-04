from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.conf import settings

from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer

import pusher

User = get_user_model()


# ──────────────────────────────────────────────
#  Pusher Initialization
# ──────────────────────────────────────────────
def get_pusher_client():
    try:
        client = pusher.Pusher(
            app_id=settings.PUSHER_APP_ID,
            key=settings.PUSHER_KEY,
            secret=settings.PUSHER_SECRET,
            cluster=settings.PUSHER_CLUSTER,
            ssl=True
        )
        return client
    except AttributeError as e:
        print(f"[Pusher] Missing setting: {e}")
        return None
    except Exception as e:
        print(f"[Pusher] Initialization failed: {e}")
        return None

pusher_client = get_pusher_client()

if pusher_client:
    print("[Pusher] Client initialized successfully.")
else:
    print("[Pusher] Client is NOT initialized. Real-time events will be skipped.")


# ──────────────────────────────────────────────
#  Helper: Safe Pusher Trigger
# ──────────────────────────────────────────────
def trigger_pusher(channel: str, event: str, data: dict):
    """
    Safely triggers a Pusher event.
    Converts nested DRF ReturnDict to plain dict before sending.
    """
    if not pusher_client:
        print("[Pusher] Skipped trigger — client not initialized.")
        return

    try:
        # Deep-convert DRF ReturnDict → plain Python dict
        plain_data = convert_to_plain_dict(data)
        pusher_client.trigger(channel, event, plain_data)
        print(f"[Pusher] Triggered '{event}' on '{channel}'")
    except Exception as e:
        print(f"[Pusher] Trigger error on channel '{channel}': {e}")


def convert_to_plain_dict(data):
    """
    Recursively converts DRF ReturnDict / OrderedDict to plain dict.
    Ensures Pusher can JSON-serialize the payload without issues.
    """
    if isinstance(data, dict):
        return {key: convert_to_plain_dict(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [convert_to_plain_dict(item) for item in data]
    else:
        return data


# ──────────────────────────────────────────────
#  Conversation List
# ──────────────────────────────────────────────
class ConversationListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        qs = Conversation.objects.filter(
            participants=request.user
        ).order_by("-created_at")

        serializer = ConversationSerializer(qs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# ──────────────────────────────────────────────
#  Message List
# ──────────────────────────────────────────────
class MessageListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, conversation_id):
        if not str(conversation_id).isdigit():
            return Response(
                {"error": "Invalid conversation_id"},
                status=status.HTTP_400_BAD_REQUEST
            )

        conversation = get_object_or_404(
            Conversation,
            id=conversation_id,
            participants=request.user
        )

        messages = Message.objects.filter(
            conversation=conversation
        ).select_related("sender").order_by("created_at")

        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# ──────────────────────────────────────────────
#  Send Message  ← Main Pusher trigger point
# ──────────────────────────────────────────────
class SendMessageView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        conversation_id = request.data.get("conversation_id")
        text = request.data.get("text", "").strip()
        file = request.FILES.get("file")

        # ── Validate conversation_id
        if not conversation_id or not str(conversation_id).isdigit():
            return Response(
                {"error": "Valid conversation_id is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # ── Must have text or file
        if not text and not file:
            return Response(
                {"error": "Message must have text or a file"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # ── Verify user is a participant
        conversation = get_object_or_404(
            Conversation,
            id=conversation_id,
            participants=request.user
        )

        # ── Create message
        message = Message.objects.create(
            conversation=conversation,
            sender=request.user,
            text=text or None,
            file=file
        )

        # ── Re-fetch with sender loaded to avoid N+1 in serializer
        message = Message.objects.select_related("sender").get(id=message.id)

        # ── Serialize
        serialized_message = MessageSerializer(message).data

        # ── Trigger Pusher with safe plain-dict conversion
        trigger_pusher(
            channel=f"chat-{conversation.id}",
            event="new-message",
            data=serialized_message
        )

        return Response(serialized_message, status=status.HTTP_201_CREATED)


# ──────────────────────────────────────────────
#  Create Direct Conversation
# ──────────────────────────────────────────────
class CreateDirectConversationView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        other_user_id = request.data.get("user_id")

        if not other_user_id:
            return Response(
                {"error": "user_id is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        other_user = get_object_or_404(User, id=other_user_id)

        # Prevent self-chat
        if other_user == request.user:
            return Response(
                {"error": "Cannot create conversation with yourself"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Return existing direct conversation if already exists
        existing = Conversation.objects.filter(
            type="DIRECT",
            participants=request.user
        ).filter(participants=other_user).first()

        if existing:
            return Response(
                {"conversation_id": existing.id},
                status=status.HTTP_200_OK
            )

        conversation = Conversation.objects.create(
            type="DIRECT",
            created_by=request.user
        )
        conversation.participants.add(request.user, other_user)

        trigger_pusher(
            channel=f"user-{other_user.id}",
            event="new-conversation",
            data={"conversation_id": conversation.id, "type": "DIRECT"}
        )

        return Response(
            {"conversation_id": conversation.id},
            status=status.HTTP_201_CREATED
        )



class CreateGroupConversationView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        name = request.data.get("name")
        user_ids = request.data.get("user_ids", [])

        if not name:
            return Response(
                {"error": "Group name required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        conversation = Conversation.objects.create(
            type="GROUP",
            name=name,
            created_by=request.user
        )

        users = User.objects.filter(id__in=user_ids)

        conversation.participants.add(request.user, *users)

        for user in users:
            trigger_pusher(
                channel=f"user-{user.id}",
                event="new-conversation",
                data={
                    "conversation_id": conversation.id,
                    "type": "GROUP",
                    "name": name
                }
            )

        return Response(
            {"conversation_id": conversation.id},
            status=status.HTTP_201_CREATED
        )


class EmployeeListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        users = User.objects.all().values("id", "username", "role")
        return Response(list(users), status=status.HTTP_200_OK)