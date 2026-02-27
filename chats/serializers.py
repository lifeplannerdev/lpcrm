from rest_framework import serializers
from .models import Conversation, Message
from django.contrib.auth import get_user_model

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "role"]


class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer()
    file = serializers.SerializerMethodField()  

    class Meta:
        model = Message
        fields = ["id", "sender", "text", "file", "created_at"]

    def get_file(self, obj):
        if obj.file:
            return obj.file.url
        return None


class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True)
    last_message = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = ["id", "type", "name", "participants", "last_message", "created_by"]

    def get_last_message(self, obj):
        last = obj.messages.order_by("-created_at").first()
        return MessageSerializer(last).data if last else None