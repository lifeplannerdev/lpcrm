from rest_framework import status, generics, filters
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
    UpcomingTaskSerializer,
)
from django.contrib.auth import get_user_model
from .permissions import (
    IsTaskAssigner,
    TASK_ASSIGNERS,
    TASK_ASSIGNEES,
    TOP_MANAGEMENT,
    OPERATIONS,
)
from django.utils.timezone import now

User = get_user_model()

logger = logging.getLogger(__name__)


# ─── Helpers ──────────────────────────────────────────────────────────────────

def _task_queryset_for_user(user, base_qs=None):
    if base_qs is None:
        base_qs = Task.objects.select_related("assigned_to", "assigned_by")

    # ADMIN / CEO → see everything
    if user.role in TOP_MANAGEMENT:
        return base_qs

    # OPS / CM → tasks assigned TO them  +  tasks they created
    if user.role in OPERATIONS:
        return base_qs.filter(
            Q(assigned_to=user) | Q(assigned_by=user)
        ).distinct()

    # All other roles → only tasks assigned to them
    return base_qs.filter(assigned_to=user)


def _apply_status_ordering(qs):
    """Order tasks: OVERDUE → PENDING → IN_PROGRESS → COMPLETED → CANCELLED."""
    return qs.annotate(
        status_priority=Case(
            When(status='OVERDUE',      then=1),
            When(status='PENDING',      then=2),
            When(status='IN_PROGRESS',  then=3),
            When(status='COMPLETED',    then=4),
            When(status='CANCELLED',    then=5),
            default=6,
            output_field=IntegerField(),
        )
    ).order_by('status_priority', '-created_at')


def _apply_priority_ordering(qs):
    """Order tasks: URGENT → HIGH → MEDIUM → LOW."""
    return qs.annotate(
        priority_order=Case(
            When(priority='URGENT', then=1),
            When(priority='HIGH',   then=2),
            When(priority='MEDIUM', then=3),
            When(priority='LOW',    then=4),
            default=5,
            output_field=IntegerField(),
        )
    )


# ─── Pagination ───────────────────────────────────────────────────────────────

class TaskPagination(PageNumberPagination):
    page_size = 50
    page_size_query_param = 'page_size'
    max_page_size = 50


class TaskUpdatePagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


# ─── Task Stats ───────────────────────────────────────────────────────────────

class TaskStatsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        qs = _task_queryset_for_user(user)

        now_dt = timezone.now()
        overdue_count = qs.filter(
            Q(deadline__lt=now_dt) &
            ~Q(status='COMPLETED') &
            ~Q(status='CANCELLED')
        ).count()

        stats = qs.aggregate(
            total=Count('id'),
            pending=Count('id',     filter=Q(status='PENDING')),
            in_progress=Count('id', filter=Q(status='IN_PROGRESS')),
            completed=Count('id',   filter=Q(status='COMPLETED')),
        )
        stats['overdue'] = overdue_count

        return Response(stats)


# ─── Employee List ────────────────────────────────────────────────────────────

class EmployeeListAPIView(generics.ListAPIView):
    """
    Returns users the requesting user is allowed to assign tasks to.
    - ADMIN / CEO  → all active users
    - OPS / CM     → only EXECUTION_ROLES
    """
    permission_classes = [IsTaskAssigner]
    serializer_class = EmployeeSerializer

    def get_queryset(self):
        user = self.request.user

        if user.role in TOP_MANAGEMENT:
            return User.objects.filter(is_active=True).exclude(id=user.id)

        # OPS / CM can only assign to execution-level employees
        return User.objects.filter(
            is_active=True,
            role__in=TASK_ASSIGNEES
        ).exclude(id=user.id)


# ─── Task List / Create ───────────────────────────────────────────────────────

class TaskListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = TaskSerializer
    pagination_class = TaskPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'description']

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsTaskAssigner()]
        return [IsAuthenticated()]

    def get_queryset(self):
        qs = _apply_status_ordering(
            _task_queryset_for_user(self.request.user)
        )

        # Filter by status if provided
        status_filter = self.request.query_params.get('status')
        if status_filter and status_filter != 'all':
            qs = qs.filter(status=status_filter)

        # Filter by priority if provided
        priority_filter = self.request.query_params.get('priority')
        if priority_filter and priority_filter != 'all':
            qs = qs.filter(priority=priority_filter)

        return qs

    def perform_create(self, serializer):
        user = self.request.user
        assigned_to = serializer.validated_data.get('assigned_to')

        # OPS / CM cannot assign tasks to ADMIN or CEO
        if user.role in OPERATIONS and assigned_to:
            if assigned_to.role in TOP_MANAGEMENT:
                from rest_framework.exceptions import ValidationError
                raise ValidationError(
                    "OPS and CM can only assign tasks to execution-level employees."
                )

        serializer.save(assigned_by=user)


# ─── Task Detail / Update / Delete ───────────────────────────────────────────

class TaskDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return _task_queryset_for_user(self.request.user)

    def _check_edit_permission(self, task):
        user = self.request.user

        if user.role in TOP_MANAGEMENT:
            return

        if user.role in OPERATIONS and task.assigned_by == user:
            return

        raise PermissionDenied(
            "Only the creator of this task can edit or delete it."
        )

    def update(self, request, *args, **kwargs):
        self._check_edit_permission(self.get_object())
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        self._check_edit_permission(self.get_object())
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        self._check_edit_permission(self.get_object())
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


# ─── Task Updates (timeline) ─────────────────────────────────────────────────

class TaskUpdateListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TaskUpdateSerializer
    pagination_class = TaskUpdatePagination   # FIX: was unpaginated → frontend expected .results

    def _get_task(self):
        return get_object_or_404(Task, pk=self.kwargs["task_id"])

    def get_queryset(self):
        task = self._get_task()
        user = self.request.user

        # ADMIN / CEO → can view any task's update history
        if user.role in TOP_MANAGEMENT:
            return TaskUpdate.objects.filter(task=task).order_by("-created_at")

        # OPS / CM → can view updates for tasks they assigned
        if user.role in OPERATIONS and task.assigned_by == user:
            return TaskUpdate.objects.filter(task=task).order_by("-created_at")

        # Assigned employee → can view their own task's updates
        if task.assigned_to == user:
            return TaskUpdate.objects.filter(task=task).order_by("-created_at")

        raise PermissionDenied("You do not have access to this task.")

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['task'] = self._get_task()
        return context

    def perform_create(self, serializer):
        task = self._get_task()

        # Only the assigned employee can post progress updates / notes
        if task.assigned_to != self.request.user:
            raise PermissionDenied("Only the assigned employee can post updates on this task.")

        new_status = serializer.validated_data.get("new_status")

        serializer.save(
            task=task,
            updated_by=self.request.user,
            previous_status=task.status,
            new_status=new_status if new_status is not None else task.status,
        )

        # Only mutate the task's status when explicitly changed
        if new_status is not None and new_status != task.status:
            task.status = new_status
            task.save(update_fields=["status", "updated_at"])


# ─── Tasks Assigned By Me ─────────────────────────────────────────────────────

class TasksAssignedByMeAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TaskSerializer
    pagination_class = TaskPagination

    def get_queryset(self):
        user = self.request.user

        if user.role not in TASK_ASSIGNERS:
            return Task.objects.none()

        return _apply_status_ordering(
            Task.objects.filter(assigned_by=user)
            .select_related('assigned_to', 'assigned_by')
        )


# ─── Task Status Update (Assignee only) ──────────────────────────────────────

class TaskStatusUpdateAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TaskUpdateSerializer

    def post(self, request, pk):
        task = get_object_or_404(Task, pk=pk)

        # Only the assigned employee can change status
        if request.user != task.assigned_to:
            return Response(
                {"detail": "Only the assigned employee can change the task status."},
                status=status.HTTP_403_FORBIDDEN
            )

        new_status = request.data.get("status")
        notes = request.data.get("notes", "").strip()

        if not new_status or new_status not in dict(Task.STATUS_CHOICES):
            return Response(
                {"detail": "Invalid or missing status."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if new_status == task.status:
            return Response(
                {"detail": "New status must differ from the current status."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Notes are required when completing or cancelling
        if new_status in ['COMPLETED', 'CANCELLED'] and not notes:
            return Response(
                {"detail": "Notes are required when completing or cancelling a task."},
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

        return Response({
            "detail": "Status updated successfully",
            "update_id": update.id
        })


# ─── Pending Tasks ────────────────────────────────────────────────────────────

class PendingTasksAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        qs = _task_queryset_for_user(
            user,
            base_qs=Task.objects.filter(
                status__in=['PENDING', 'IN_PROGRESS']
            ).select_related('assigned_to', 'assigned_by')
        )

        qs = _apply_priority_ordering(qs).order_by('priority_order', 'deadline')

        return Response(TaskSerializer(qs, many=True).data)


# ─── Upcoming Tasks ───────────────────────────────────────────────────────────

class UpcomingTasksAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        qs = _task_queryset_for_user(
            user,
            base_qs=Task.objects.filter(deadline__gte=now())
                                .exclude(status__in=['COMPLETED', 'CANCELLED'])
                                .select_related('assigned_to', 'assigned_by')
        )

        qs = qs.order_by("deadline")[:5]

        return Response(UpcomingTaskSerializer(qs, many=True).data)