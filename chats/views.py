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


#  Safe Pusher Initialization
try:
    pusher_client = pusher.Pusher(
        app_id=settings.PUSHER_APP_ID,
        key=settings.PUSHER_KEY,
        secret=settings.PUSHER_SECRET,
        cluster=settings.PUSHER_CLUSTER,
        ssl=True
    )
except Exception as e:
    print("Pusher init error:", e)
    pusher_client = None


#  Conversation List
class ConversationListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        qs = Conversation.objects.filter(
            participants=request.user
        ).order_by("-created_at")

        serializer = ConversationSerializer(qs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


#  Message List 
class MessageListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, conversation_id):
        if not str(conversation_id).isdigit():
            return Response(
                {"error": "Invalid conversation_id"},
                status=status.HTTP_400_BAD_REQUEST
            )

        #  Ensure user belongs to conversation
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


#  Send Message
class SendMessageView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        conversation_id = request.data.get("conversation_id")
        text = request.data.get("text", "").strip()
        file = request.FILES.get("file")

        if not conversation_id or not str(conversation_id).isdigit():
            return Response(
                {"error": "Valid conversation_id is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not text and not file:
            return Response(
                {"error": "Message must have text or a file"},
                status=status.HTTP_400_BAD_REQUEST
            )

        conversation = get_object_or_404(
            Conversation,
            id=conversation_id,
            participants=request.user
        )

        message = Message.objects.create(
            conversation=conversation,
            sender=request.user,
            text=text or None,
            file=file
        )

        serialized_message = MessageSerializer(message).data

        #  Safe Pusher trigger
        try:
            if pusher_client:
                pusher_client.trigger(
                    f"chat-{conversation.id}",
                    "new-message",
                    serialized_message
                )
        except Exception as e:
            print("Pusher trigger error:", e)

        return Response(serialized_message, status=status.HTTP_201_CREATED)


#  Create Direct Conversation
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

        return Response(
            {"conversation_id": conversation.id},
            status=status.HTTP_201_CREATED
        )


#  Create Group Conversation
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

        # Always include creator
        conversation.participants.add(request.user, *users)

        return Response(
            {"conversation_id": conversation.id},
            status=status.HTTP_201_CREATED
        )


#  Employee List 
class EmployeeListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        users = User.objects.all().values("id", "username", "role")

        return Response(list(users), status=status.HTTP_200_OK)