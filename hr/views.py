from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import Penalty, AttendanceDocument
from .serializers import (
    PenaltySerializer, 
    AttendanceDocumentSerializer, 
    StaffSerializer
)
from .permissions import IsHR, IsHROrAccountsOrAdmin

User = get_user_model()


# ===== PENALTY APIs =====

class PenaltyListCreateAPI(APIView):
    """
    List all penalties or create a new penalty
    Accessible by: HR, Accounts, Admin
    """
    permission_classes = [IsHROrAccountsOrAdmin]
    
    def get(self, request):
        """
        GET /api/penalties/
        Query params:
        - month: Filter by month (e.g., "2025-01")
        - user: Filter by user ID
        """
        penalties = Penalty.objects.all()
        
        # Filter by month
        month = request.GET.get("month")
        if month:
            penalties = penalties.filter(month=month)
        
        # Filter by user
        user_id = request.GET.get("user")
        if user_id:
            penalties = penalties.filter(user_id=user_id)
        
        # Serialize with user details
        serializer = PenaltySerializer(
            penalties.order_by("-date"), 
            many=True
        )
        
        return Response({
            "count": penalties.count(),
            "results": serializer.data
        })
    
    def post(self, request):
        """
        POST /api/penalties/
        Body: {
            "user": <user_id>,
            "act": "Reason for penalty",
            "amount": 100,
            "month": "2025-01",
            "date": "2025-01-15"
        }
        """
        serializer = PenaltySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PenaltyDetailAPI(APIView):
    """
    Update or delete a specific penalty
    Accessible by: HR, Accounts, Admin
    """
    permission_classes = [IsHROrAccountsOrAdmin]
    
    def get(self, request, pk):
        """
        GET /api/penalties/<id>/
        Get details of a specific penalty
        """
        try:
            penalty = Penalty.objects.get(pk=pk)
        except Penalty.DoesNotExist:
            return Response(
                {"error": "Penalty not found"}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = PenaltySerializer(penalty)
        return Response(serializer.data)
    
    def put(self, request, pk):
        """
        PUT /api/penalties/<id>/
        Update a penalty
        """
        try:
            penalty = Penalty.objects.get(pk=pk)
        except Penalty.DoesNotExist:
            return Response(
                {"error": "Penalty not found"}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = PenaltySerializer(penalty, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        """
        DELETE /api/penalties/<id>/
        Delete a penalty
        """
        try:
            penalty = Penalty.objects.get(pk=pk)
        except Penalty.DoesNotExist:
            return Response(
                {"error": "Penalty not found"}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        penalty.delete()
        return Response(
            {"message": "Penalty deleted successfully"}, 
            status=status.HTTP_204_NO_CONTENT
        )


# ===== ATTENDANCE APIs =====

class AttendanceDocumentAPI(APIView):
    """
    List all attendance documents or upload a new one
    Accessible by: HR only
    """
    permission_classes = [IsHR]
    
    def get(self, request):
        """
        GET /api/attendance/
        Query params:
        - month: Filter by month
        """
        docs = AttendanceDocument.objects.all()
        
        month = request.GET.get("month")
        if month:
            docs = docs.filter(month=month)
        
        serializer = AttendanceDocumentSerializer(docs.order_by("-date"), many=True)
        return Response({
            "count": docs.count(),
            "results": serializer.data
        })
    
    def post(self, request):
        """
        POST /api/attendance/
        Body: {
            "name": "January 2025 Attendance",
            "date": "2025-01-31",
            "month": "2025-01",
            "document": <file>
        }
        """
        serializer = AttendanceDocumentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AttendanceDocumentDeleteAPI(APIView):
    """
    Delete an attendance document
    Accessible by: HR only
    """
    permission_classes = [IsHR]
    
    def get(self, request, pk):
        """Get specific attendance document"""
        try:
            doc = AttendanceDocument.objects.get(pk=pk)
        except AttendanceDocument.DoesNotExist:
            return Response(
                {"error": "Document not found"}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = AttendanceDocumentSerializer(doc)
        return Response(serializer.data)
    
    def delete(self, request, pk):
        """
        DELETE /api/attendance/<id>/
        """
        try:
            doc = AttendanceDocument.objects.get(pk=pk)
        except AttendanceDocument.DoesNotExist:
            return Response(
                {"error": "Document not found"}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        doc.delete()
        return Response(
            {"message": "Document deleted successfully"}, 
            status=status.HTTP_204_NO_CONTENT
        )


# ===== STAFF/EMPLOYEE APIs =====

class StaffListAPI(APIView):
    """
    List all staff/employees
    Accessible by: HR, Accounts, Admin
    """
    permission_classes = [IsHROrAccountsOrAdmin]
    
    def get(self, request):
        """
        GET /api/employees/
        Query params:
        - role: Filter by role
        - is_active: Filter by active status (true/false)
        - search: Search by name, username, or email
        """
        users = User.objects.all()
        
        # Filter by role
        role = request.GET.get("role")
        if role:
            users = users.filter(role=role)
        
        # Filter by active status
        is_active = request.GET.get("is_active")
        if is_active is not None:
            users = users.filter(is_active=is_active.lower() == "true")
        
        # Search
        search = request.GET.get("search")
        if search:
            users = users.filter(
                first_name__icontains=search
            ) | users.filter(
                last_name__icontains=search
            ) | users.filter(
                username__icontains=search
            ) | users.filter(
                email__icontains=search
            )
        
        serializer = StaffSerializer(users.order_by("first_name"), many=True)
        return Response({
            "count": users.count(),
            "results": serializer.data
        })


class StaffDetailAPI(APIView):
    """
    Get details of a specific staff member
    Accessible by: HR, Accounts, Admin
    """
    permission_classes = [IsHROrAccountsOrAdmin]
    
    def get(self, request, pk):
        """
        GET /api/employees/<id>/
        """
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response(
                {"error": "Employee not found"}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = StaffSerializer(user)
        return Response(serializer.data)
