from rest_framework.permissions import BasePermission


# =====================
# Role Groups
# =====================

TOP_MANAGEMENT = [
    "ADMIN",
    "BUSINESS_HEAD",
]

OPERATIONS = [
    "OPS",
    "GENERAL_MANAGER",
    "CM",
    "BDM",
]

HR_ROLES = [
    "HR",
]

EXECUTION_ROLES = [
    "MEDIA",
    "ADM_EXEC",
    "ADM_MANAGER",
    "PROCESSING",
    "FOE",
    "TRAINER",
]


# =====================
# Derived Permissions
# =====================

TASK_ASSIGNERS = TOP_MANAGEMENT + OPERATIONS + HR_ROLES
TASK_ASSIGNEES = EXECUTION_ROLES


# =====================
# Base Permissions
# =====================

class IsTaskAssigner(BasePermission):
    """
    Can create, update, delete tasks
    Can view all tasks
    """

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role in TASK_ASSIGNERS
        )


class IsTaskAssignee(BasePermission):
    """
    Can receive tasks and update status
    """

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role in TASK_ASSIGNEES
        )


# =====================
# Object-Level Permissions
# =====================

class IsAssigneeOrTaskAssigner(BasePermission):
    """
    Object-level:
    - Assigned employee can access their task
    - Task assigners (OPS / CM / ADMIN) can access all tasks
    """

    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False

        # Assigned employee
        if obj.assigned_to == request.user:
            return True

        # Admin or task assigners
        if request.user.role == "ADMIN" or request.user.role in TASK_ASSIGNERS:
            return True

        return False
