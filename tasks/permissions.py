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
    "ACCOUNTS",
]


# =====================
# Derived Permissions
# =====================

TASK_ASSIGNERS = TOP_MANAGEMENT + OPERATIONS + HR_ROLES
TASK_ASSIGNEES = EXECUTION_ROLES


# =====================
# View-Level Permissions
# =====================

class IsTaskAssigner(BasePermission):
    """
    ADMIN / OPS / HR
    Can create, update, delete tasks
    Can assign tasks to ALL employees
    """

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role in TASK_ASSIGNERS
        )


class IsTaskAssignee(BasePermission):
    """
    Employees who receive tasks
    Can update their own task status
    """

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role in TASK_ASSIGNEES
        )


# =====================
# Object-Level Permission
# =====================

class IsAssigneeOrTaskAssigner(BasePermission):
    """
    - Assigned employee → access own task
    - ADMIN / Assigners → access ALL tasks
    """

    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False

        if obj.assigned_to == request.user:
            return True

        if request.user.role == "ADMIN" or request.user.role in TASK_ASSIGNERS:
            return True

        return False
