from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from django.contrib.auth import get_user_model

User = get_user_model()


class ConversationListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        qs = Conversation.objects.filter(
            participants=request.user
        ).order_by("-created_at")

        return Response(ConversationSerializer(qs, many=True).data)


class MessageListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, conversation_id):
        messages = Message.objects.filter(
            conversation_id=conversation_id
        ).order_by("created_at")

        return Response(MessageSerializer(messages, many=True).data)


class SendMessageView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        conversation_id = request.data.get("conversation_id")
        text = request.data.get("text")

        if not conversation_id or not text:
            return Response({"error": "Missing fields"}, status=400)

        message = Message.objects.create(
            conversation_id=conversation_id,
            sender=request.user,
            text=text
        )

        return Response({"status": "sent", "message_id": message.id})


class CreateDirectConversationView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        other_user_id = request.data.get("user_id")

        other_user = User.objects.get(id=other_user_id)

        # check existing direct chat
        existing = Conversation.objects.filter(
            type="DIRECT",
            participants=request.user
        ).filter(participants=other_user).first()

        if existing:
            return Response({"conversation_id": existing.id})

        conversation = Conversation.objects.create(
            type="DIRECT",
            created_by=request.user
        )
        conversation.participants.add(request.user, other_user)

        return Response({"conversation_id": conversation.id})


class CreateGroupConversationView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        name = request.data.get("name")
        user_ids = request.data.get("user_ids", [])

        if not name:
            return Response({"error": "Group name required"}, status=400)

        conversation = Conversation.objects.create(
            type="GROUP",
            name=name,
            created_by=request.user
        )

        users = User.objects.filter(id__in=user_ids)
        conversation.participants.add(request.user, *users)

        return Response({"conversation_id": conversation.id})


class EmployeeListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        users = User.objects.exclude(id=request.user.id)
        return Response(UserSerializer(users, many=True).data)
