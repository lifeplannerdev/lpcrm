from rest_framework import serializers
from .models import Penalty, AttendanceDocument
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "role", "salary", "join_date", "position"]

class PenaltySerializer(serializers.ModelSerializer):
    class Meta:
        model = Penalty
        fields = ['id', 'user', 'act', 'amount', 'month', 'date']

class AttendanceDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttendanceDocument
        fields = "__all__"


class StaffSerializer(serializers.ModelSerializer):
    role_display = serializers.CharField(source="get_role_display", read_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "phone",
            "role",
            "role_display",
            "team",
            "location",
            "salary",
            "join_date",
            "is_active",
        ]
