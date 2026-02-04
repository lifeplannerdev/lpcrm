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

        if user.role == "ADMIN" or user.role in TASK_ASSIGNERS:
            qs = Task.objects.all()
        elif user.role in TASK_ASSIGNEES:
            qs = Task.objects.filter(assigned_to=user)
        else:
            qs = Task.objects.none()

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

        if user.role == "ADMIN" or user.role in TASK_ASSIGNERS:
            return qs.order_by("-created_at")

        if user.role in TASK_ASSIGNEES:
            return qs.filter(assigned_to=user).order_by("-created_at")

        return Task.objects.none()

    def perform_create(self, serializer):
        serializer.save(assigned_by=self.request.user)


# Task Detail / Update / Delete
class TaskDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TaskSerializer

    def get_permissions(self):
        if self.request.method in ["PUT", "PATCH", "DELETE"]:
            return [IsTaskAssigner()]
        return [IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user
        qs = Task.objects.select_related("assigned_to", "assigned_by")

        if user.role == "ADMIN" or user.role in TASK_ASSIGNERS:
            return qs

        if user.role in TASK_ASSIGNEES:
            return qs.filter(assigned_to=user)

        return Task.objects.none()
    
    def perform_update(self, serializer):
        """Create TaskUpdate record when status changes"""
        task = self.get_object()
        old_status = task.status
        new_status = serializer.validated_data.get('status', old_status)
        
        logger.info(f"Task {task.id} being updated from {old_status} to {new_status}")
        
        # Save the task
        instance = serializer.save()
        
        # If status changed, create a TaskUpdate record
        if old_status != new_status:
            update = TaskUpdate.objects.create(
                task=instance,
                updated_by=self.request.user,
                previous_status=old_status,
                new_status=new_status,
                notes=f"Status changed by {self.request.user.username}"
            )
            logger.info(f"Created TaskUpdate {update.id} for task {task.id}")


# Task Updates - ENHANCED WITH LOGGING
class TaskUpdateListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TaskUpdateSerializer

    def get_queryset(self):
        task_id = self.kwargs["task_id"]
        logger.info(f"=== Fetching updates for task {task_id} ===")
        
        task = get_object_or_404(Task, pk=task_id)
        user = self.request.user

        if (
            task.assigned_to != user
            and user.role not in TASK_ASSIGNERS
            and user.role != "ADMIN"
        ):
            logger.warning(f"User {user.id} denied access to task {task_id} updates")
            raise PermissionDenied("You do not have access to this task.")

        updates = TaskUpdate.objects.filter(task=task).order_by("-created_at")
        
        logger.info(f"Found {updates.count()} updates for task {task_id}")
        
        # Log each update's notes
        for update in updates:
            logger.info(f"Update {update.id}: notes='{update.notes}' (type: {type(update.notes)}, length: {len(update.notes) if update.notes else 0})")
        
        return updates

    def get_serializer_context(self):
        """Add task to serializer context for validation"""
        context = super().get_serializer_context()
        task = get_object_or_404(Task, pk=self.kwargs["task_id"])
        context['task'] = task
        logger.info(f"Added task {task.id} to serializer context")
        return context

    def perform_create(self, serializer):
        task_id = self.kwargs["task_id"]
        logger.info(f"=== Creating new task update for task {task_id} ===")
        
        task = get_object_or_404(Task, pk=task_id)

        if task.assigned_to != self.request.user:
            logger.warning(f"User {self.request.user.id} not authorized to update task {task_id}")
            raise PermissionDenied("Only the assigned employee can update this task.")

        new_status = serializer.validated_data.get("new_status", task.status)
        notes = serializer.validated_data.get("notes", "")
        
        logger.info(f"New status: {new_status}, Previous status: {task.status}")
        logger.info(f"Notes received: '{notes}' (type: {type(notes)}, length: {len(notes) if notes else 0})")

        # Save the update with all data including notes
        update = serializer.save(
            task=task,
            updated_by=self.request.user,
            previous_status=task.status
        )
        
        logger.info(f"Created TaskUpdate {update.id}")
        logger.info(f"Saved notes: '{update.notes}' (type: {type(update.notes)}, length: {len(update.notes) if update.notes else 0})")

        # Update task status if it changed
        if new_status != task.status:
            task.status = new_status
            task.save(update_fields=["status", "updated_at"])
            logger.info(f"Updated task {task_id} status to {new_status}")


# Tasks Assigned By Me
class TasksAssignedByMeAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TaskSerializer

    def get_queryset(self):
        user = self.request.user
        if user.role not in TASK_ASSIGNERS and user.role != "ADMIN":
            return Task.objects.none()

        return Task.objects.filter(
            assigned_by=user
        ).select_related(
            'assigned_to', 'assigned_by'
        ).order_by('-created_at')


# Task Status Update (Assignee only) - ENHANCED WITH LOGGING
class TaskStatusUpdateAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TaskUpdateSerializer

    def post(self, request, pk):
        logger.info(f"=== Task Status Update Request for task {pk} ===")
        logger.info(f"Request user: {request.user.id} ({request.user.username})")
        logger.info(f"Request data: {request.data}")
        
        task = get_object_or_404(Task, pk=pk)
        logger.info(f"Task found: {task.id} - '{task.title}'")
        logger.info(f"Current status: {task.status}")
        logger.info(f"Assigned to: {task.assigned_to.id} ({task.assigned_to.username})")

        if request.user != task.assigned_to:
            logger.warning(f"Permission denied: User {request.user.id} is not assigned to task {pk}")
            return Response(
                {"detail": "Only assigned user can change status."},
                status=status.HTTP_403_FORBIDDEN
            )

        new_status = request.data.get("status")
        notes = request.data.get("notes", "")
        
        logger.info(f"New status from request: {new_status}")
        logger.info(f"Notes from request: '{notes}' (type: {type(notes)}, length: {len(notes) if notes else 0})")

        if new_status not in dict(Task.STATUS_CHOICES):
            logger.error(f"Invalid status: {new_status}")
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
                notes=notes  # This is the critical part - notes should be saved here
            )
            
            logger.info(f"✅ Created TaskUpdate {update.id}")
            logger.info(f"TaskUpdate details:")
            logger.info(f"  - ID: {update.id}")
            logger.info(f"  - Task: {update.task.id}")
            logger.info(f"  - Previous Status: {update.previous_status}")
            logger.info(f"  - New Status: {update.new_status}")
            logger.info(f"  - Notes: '{update.notes}' (type: {type(update.notes)})")
            logger.info(f"  - Notes length: {len(update.notes) if update.notes else 0}")
            logger.info(f"  - Updated by: {update.updated_by.username}")
            logger.info(f"  - Created at: {update.created_at}")
            
            # Verify by re-fetching from database
            saved_update = TaskUpdate.objects.get(pk=update.id)
            logger.info(f"Verification - Re-fetched update notes: '{saved_update.notes}'")
            
        except Exception as e:
            logger.error(f"❌ Error creating TaskUpdate: {str(e)}", exc_info=True)
            return Response(
                {"detail": f"Failed to create update: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        # Update the task status
        try:
            task.status = new_status
            task.save(update_fields=['status', 'updated_at'])
            logger.info(f"✅ Updated task {pk} status to {new_status}")
        except Exception as e:
            logger.error(f"❌ Error updating task status: {str(e)}", exc_info=True)
            return Response(
                {"detail": f"Failed to update task: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        logger.info(f"=== Task Status Update Complete ===")
        return Response({"detail": "Status updated successfully", "update_id": update.id})


# Upcoming Tasks
class UpcomingTasksAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        qs = Task.objects.filter(deadline__gte=now())

        if request.user.role not in TASK_ASSIGNERS and request.user.role != "ADMIN":
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
