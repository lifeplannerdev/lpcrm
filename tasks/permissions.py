from rest_framework.permissions import BasePermission

TOP_MANAGEMENT = [
    "ADMIN",
    "CEO",
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
    "ADM_COUNSELLOR",
    "PROCESSING",
    "FOE",
    "TRAINER",
    "ACCOUNTS",
    'DOCUMENTATION',
]



TASK_ASSIGNERS = TOP_MANAGEMENT + OPERATIONS + HR_ROLES
TASK_ASSIGNEES = EXECUTION_ROLES




class IsTaskAssigner(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role in TASK_ASSIGNERS
        )


class IsTaskAssignee(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role in TASK_ASSIGNEES
        )



class IsAssigneeOrTaskAssigner(BasePermission):
    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False

        if obj.assigned_to == request.user:
            return True

        if request.user.role == "ADMIN" or request.user.role in TASK_ASSIGNERS:
            return True

        return False
