from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from django.db.models import Count, Q, Case, When, IntegerField
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
from .permissions import IsTaskAssigner, TASK_ASSIGNERS, TASK_ASSIGNEES, TOP_MANAGEMENT
from django.utils.timezone import now

User = get_user_model()

# Setup logger
logger = logging.getLogger(__name__)

# Roles that can see ALL tasks (not just their own)
FULL_TASK_VIEW_ROLES = TOP_MANAGEMENT  # ADMIN, CEO


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

        # TOP_MANAGEMENT sees stats across all tasks
        if user.role in FULL_TASK_VIEW_ROLES:
            qs = Task.objects.all()
        else:
            qs = Task.objects.filter(assigned_to=user)

        now_dt = timezone.now()

        overdue_count = qs.filter(
            Q(deadline__lt=now_dt) &
            ~Q(status='COMPLETED') &
            ~Q(status='CANCELLED')
        ).count()

        stats = qs.aggregate(
            total=Count('id'),
            pending=Count('id', filter=Q(status='PENDING')),
            in_progress=Count('id', filter=Q(status='IN_PROGRESS')),
            completed=Count('id', filter=Q(status='COMPLETED')),
        )

        stats['overdue'] = overdue_count

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
            # TASK_ASSIGNERS (TOP_MANAGEMENT + OPERATIONS + HR) can create tasks
            return [IsTaskAssigner()]
        return [IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user
        qs = Task.objects.select_related("assigned_to", "assigned_by")

        # TOP_MANAGEMENT (ADMIN, CEO) can see all tasks
        if user.role in FULL_TASK_VIEW_ROLES:
            base_qs = qs
        # TASK_ASSIGNERS (OPS, CM, BDM, GM, HR, etc.) see tasks they assigned
        elif user.role in TASK_ASSIGNERS:
            base_qs = qs.filter(assigned_by=user)
        # Everyone else (TASK_ASSIGNEES) sees only tasks assigned to them
        else:
            base_qs = qs.filter(assigned_to=user)

        return base_qs.annotate(
            status_priority=Case(
                When(status='OVERDUE', then=1),
                When(status='PENDING', then=2),
                When(status='IN_PROGRESS', then=3),
                When(status='COMPLETED', then=4),
                default=5,
                output_field=IntegerField(),
            )
        ).order_by('status_priority', '-created_at')

    def perform_create(self, serializer):
        serializer.save(assigned_by=self.request.user)


# Task Detail / Update / Delete
class TaskDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TaskSerializer

    def get_permissions(self):
        return [IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user
        qs = Task.objects.select_related("assigned_to", "assigned_by")

        # TOP_MANAGEMENT can access all tasks
        if user.role in FULL_TASK_VIEW_ROLES:
            return qs

        # TASK_ASSIGNERS (OPS, CM, BDM, GM, HR) can access tasks they assigned
        if user.role in TASK_ASSIGNERS:
            return qs.filter(assigned_by=user)

        # Everyone else can only access tasks assigned to them
        return qs.filter(assigned_to=user)

    def check_edit_permission(self, task):
        """
        Only the user who created the task (assigned_by) can edit/delete it.
        TOP_MANAGEMENT can also edit/delete any task.
        """
        user = self.request.user

        if user.role in FULL_TASK_VIEW_ROLES:
            return

        if task.assigned_by != user:
            raise PermissionDenied(
                "Only the user who created this task can edit or delete it."
            )

    def update(self, request, *args, **kwargs):
        task = self.get_object()
        self.check_edit_permission(task)
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        task = self.get_object()
        self.check_edit_permission(task)
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        task = self.get_object()
        self.check_edit_permission(task)
        return super().destroy(request, *args, **kwargs)

    def perform_update(self, serializer):
        task = self.get_object()
        old_status = task.status
        new_status = serializer.validated_data.get('status', old_status)

        instance = serializer.save()

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

        # TOP_MANAGEMENT can view any task's updates
        if user.role in FULL_TASK_VIEW_ROLES:
            return TaskUpdate.objects.filter(task=task).order_by("-created_at")

        # TASK_ASSIGNERS can view updates for tasks they assigned
        if user.role in TASK_ASSIGNERS and task.assigned_by == user:
            return TaskUpdate.objects.filter(task=task).order_by("-created_at")

        # Assigned employee can view their own task updates
        if task.assigned_to == user:
            return TaskUpdate.objects.filter(task=task).order_by("-created_at")

        raise PermissionDenied("You do not have access to this task.")

    def get_serializer_context(self):
        context = super().get_serializer_context()
        task = get_object_or_404(Task, pk=self.kwargs["task_id"])
        context['task'] = task
        return context

    def perform_create(self, serializer):
        task_id = self.kwargs["task_id"]
        task = get_object_or_404(Task, pk=task_id)

        # Only the assigned employee can post updates
        if task.assigned_to != self.request.user:
            raise PermissionDenied("Only the assigned employee can update this task.")

        new_status = serializer.validated_data.get("new_status", task.status)

        serializer.save(
            task=task,
            updated_by=self.request.user,
            previous_status=task.status
        )

        if new_status != task.status:
            task.status = new_status
            task.save(update_fields=["status", "updated_at"])


# Tasks Assigned By Me
class TasksAssignedByMeAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TaskSerializer

    def get_queryset(self):
        user = self.request.user

        if user.role not in TASK_ASSIGNERS:
            return Task.objects.none()

        return Task.objects.filter(
            assigned_by=user
        ).select_related(
            'assigned_to', 'assigned_by'
        ).annotate(
            status_priority=Case(
                When(status='OVERDUE', then=1),
                When(status='PENDING', then=2),
                When(status='IN_PROGRESS', then=3),
                When(status='COMPLETED', then=4),
                default=5,
                output_field=IntegerField(),
            )
        ).order_by('status_priority', '-created_at')


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


# Pending Tasks
class PendingTasksAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        qs = Task.objects.filter(
            status__in=['PENDING', 'IN_PROGRESS']
        ).select_related('assigned_to', 'assigned_by')

        # TOP_MANAGEMENT sees all pending tasks
        if user.role in FULL_TASK_VIEW_ROLES:
            pass
        # TASK_ASSIGNERS see pending tasks they assigned
        elif user.role in TASK_ASSIGNERS:
            qs = qs.filter(assigned_by=user)
        # Everyone else sees only their own
        else:
            qs = qs.filter(assigned_to=user)

        qs = qs.annotate(
            priority_order=Case(
                When(priority='HIGH', then=1),
                When(priority='MEDIUM', then=2),
                When(priority='LOW', then=3),
                default=4,
                output_field=IntegerField(),
            )
        ).order_by('priority_order', 'deadline')

        serializer = TaskSerializer(qs, many=True)
        return Response(serializer.data)


# Upcoming Tasks
class UpcomingTasksAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        qs = Task.objects.filter(deadline__gte=now())

        # TOP_MANAGEMENT sees all upcoming tasks
        if user.role in FULL_TASK_VIEW_ROLES:
            pass
        # TASK_ASSIGNERS see upcoming tasks they assigned
        elif user.role in TASK_ASSIGNERS:
            qs = qs.filter(assigned_by=user)
        # Everyone else sees only their own
        else:
            qs = qs.filter(assigned_to=user)

        qs = qs.order_by("deadline")[:5]

        return Response([
            {
                "title": t.title,
                "status": t.status,
                "deadline": t.deadline.strftime("%d %b %Y"),
            }
            for t in qs
        ])