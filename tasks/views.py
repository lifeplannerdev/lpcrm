from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from django.utils import timezone
from rest_framework.exceptions import PermissionDenied
import logging

from .models import Task, TaskUpdate
from .serializers import (
    TaskSerializer,
    TaskUpdateSerializer,
    EmployeeSerializer,
)
from django.contrib.auth import get_user_model
from .permissions import IsTaskAssigner, TASK_ASSIGNERS, TASK_ASSIGNEES
from django.utils.timezone import now

User = get_user_model()

# Setup logger
logger = logging.getLogger(__name__)


# Pagination
class TaskPagination(PageNumberPagination):
    page_size = 50
    page_size_query_param = 'page_size'
    max_page_size = 50


# Task Stats
class TaskStatsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        # ONLY ADMIN can see all tasks stats
        if user.role == "ADMIN":
            qs = Task.objects.all()
        else:
            # All other roles see only tasks assigned to them
            qs = Task.objects.filter(assigned_to=user)

        stats = qs.aggregate(
            total=Count('id'),
            pending=Count('id', filter=Q(status='PENDING')),
            in_progress=Count('id', filter=Q(status='IN_PROGRESS')),
            completed=Count('id', filter=Q(status='COMPLETED')),
            overdue=Count('id', filter=Q(status='OVERDUE')),
        )

        return Response(stats)


# Employee List
class EmployeeListAPIView(generics.ListAPIView):
    permission_classes = [IsTaskAssigner]
    queryset = User.objects.filter(is_active=True)
    serializer_class = EmployeeSerializer


# Task List / Create
class TaskListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = TaskSerializer
    pagination_class = TaskPagination

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsTaskAssigner()]
        return [IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user
        qs = Task.objects.select_related("assigned_to", "assigned_by")

        # ONLY ADMIN can see all tasks
        if user.role == "ADMIN":
            return qs.order_by("-created_at")

        # All other roles (including TASK_ASSIGNERS) see only tasks assigned to them
        return qs.filter(assigned_to=user).order_by("-created_at")

    def perform_create(self, serializer):
        serializer.save(assigned_by=self.request.user)


# Task Detail / Update / Delete
class TaskDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TaskSerializer

    def get_permissions(self):
        # Anyone authenticated can view (subject to queryset filtering)
        # Update/Delete require custom permission check
        return [IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user
        qs = Task.objects.select_related("assigned_to", "assigned_by")

        # ONLY ADMIN can access all tasks
        if user.role == "ADMIN":
            return qs

        # All other roles can only access tasks assigned to them
        return qs.filter(assigned_to=user)
    
    def check_edit_permission(self, task):
        """
        Check if user can edit/delete the task.
        Only the user who created the task (assigned_by) can edit/delete it.
        """
        user = self.request.user
        
        if task.assigned_by != user:
            raise PermissionDenied(
                "Only the user who created this task can edit or delete it."
            )
    
    def update(self, request, *args, **kwargs):
        """Override update to check edit permission"""
        task = self.get_object()
        self.check_edit_permission(task)
        return super().update(request, *args, **kwargs)
    
    def partial_update(self, request, *args, **kwargs):
        """Override partial_update to check edit permission"""
        task = self.get_object()
        self.check_edit_permission(task)
        return super().partial_update(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        """Override destroy to check edit permission"""
        task = self.get_object()
        self.check_edit_permission(task)
        return super().destroy(request, *args, **kwargs)
    
    def perform_update(self, serializer):
        """Create TaskUpdate record when status changes"""
        task = self.get_object()
        old_status = task.status
        new_status = serializer.validated_data.get('status', old_status)
        
        # Save the task
        instance = serializer.save()
        
        # If status changed, create a TaskUpdate record
        if old_status != new_status:
            TaskUpdate.objects.create(
                task=instance,
                updated_by=self.request.user,
                previous_status=old_status,
                new_status=new_status,
                notes=f"Status changed by {self.request.user.username}"
            )


# Task Updates
class TaskUpdateListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TaskUpdateSerializer

    def get_queryset(self):
        task_id = self.kwargs["task_id"]
        task = get_object_or_404(Task, pk=task_id)
        user = self.request.user

        # ONLY ADMIN or assigned user can view task updates
        if task.assigned_to != user and user.role != "ADMIN":
            raise PermissionDenied("You do not have access to this task.")

        return TaskUpdate.objects.filter(task=task).order_by("-created_at")

    def get_serializer_context(self):
        """Add task to serializer context for validation"""
        context = super().get_serializer_context()
        task = get_object_or_404(Task, pk=self.kwargs["task_id"])
        context['task'] = task
        return context

    def perform_create(self, serializer):
        task_id = self.kwargs["task_id"]
        task = get_object_or_404(Task, pk=task_id)

        # Only the assigned employee can create updates
        if task.assigned_to != self.request.user:
            raise PermissionDenied("Only the assigned employee can update this task.")

        new_status = serializer.validated_data.get("new_status", task.status)
        notes = serializer.validated_data.get("notes", "")

        # Save the update with all data including notes
        update = serializer.save(
            task=task,
            updated_by=self.request.user,
            previous_status=task.status
        )

        # Update task status if it changed
        if new_status != task.status:
            task.status = new_status
            task.save(update_fields=["status", "updated_at"])


# Tasks Assigned By Me
class TasksAssignedByMeAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TaskSerializer

    def get_queryset(self):
        user = self.request.user
        
        # ONLY ADMIN and TASK_ASSIGNERS can use this endpoint
        if user.role not in TASK_ASSIGNERS and user.role != "ADMIN":
            return Task.objects.none()

        return Task.objects.filter(
            assigned_by=user
        ).select_related(
            'assigned_to', 'assigned_by'
        ).order_by('-created_at')


# Task Status Update (Assignee only)
class TaskStatusUpdateAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TaskUpdateSerializer

    def post(self, request, pk):
        task = get_object_or_404(Task, pk=pk)

        # Only assigned user can change status
        if request.user != task.assigned_to:
            return Response(
                {"detail": "Only assigned user can change status."},
                status=status.HTTP_403_FORBIDDEN
            )

        new_status = request.data.get("status")
        notes = request.data.get("notes", "")

        if new_status not in dict(Task.STATUS_CHOICES):
            return Response(
                {"detail": "Invalid status."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Create the TaskUpdate record with notes
        try:
            update = TaskUpdate.objects.create(
                task=task,
                updated_by=request.user,
                previous_status=task.status,
                new_status=new_status,
                notes=notes
            )
        except Exception as e:
            logger.error(f"Error creating TaskUpdate: {str(e)}", exc_info=True)
            return Response(
                {"detail": f"Failed to create update: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        # Update the task status
        try:
            task.status = new_status
            task.save(update_fields=['status', 'updated_at'])
        except Exception as e:
            logger.error(f"Error updating task status: {str(e)}", exc_info=True)
            return Response(
                {"detail": f"Failed to update task: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return Response({"detail": "Status updated successfully", "update_id": update.id})


# Pending Tasks (NEW)

class PendingTasksAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user = request.user
        qs = Task.objects.filter(
            status__in=['PENDING', 'IN_PROGRESS']
        ).select_related('assigned_to', 'assigned_by')

        if user.role != "ADMIN":
            qs = qs.filter(assigned_to=user)
        qs = qs.order_by('-priority', 'deadline')
        serializer = TaskSerializer(qs, many=True)
        return Response(serializer.data)

# Upcoming Tasks
class UpcomingTasksAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        qs = Task.objects.filter(deadline__gte=now())

        # ONLY ADMIN can see all upcoming tasks
        if request.user.role != "ADMIN":
            qs = qs.filter(assigned_to=request.user)

        qs = qs.order_by("deadline")[:5]

        return Response([
            {
                "title": t.title,
                "status": t.status,
                "deadline": t.deadline.strftime("%d %b %Y"),
            }
            for t in qs
        ])
