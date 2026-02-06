from rest_framework.permissions import BasePermission

# Role hierarchy for assignments
ADMIN_ROLES = ['ADMIN', 'BUSINESS_HEAD']  # Removed 'OPS' from here
OPERATIONS_ROLES = ['OPS']  # OPS separated into its own category
MANAGER_ROLES = [
    'ADM_MANAGER',
    'CM',  # Center Manager
    'BDM',  # Business Development Manager
]
EXECUTIVE_ROLES = [
    'ADM_EXEC',
    'FOE',
    'PROCESSING',
    'MEDIA',
    'TRAINER',
]

# Roles allowed to access leads
LEAD_ACCESS_ROLES = ADMIN_ROLES + OPERATIONS_ROLES + MANAGER_ROLES + EXECUTIVE_ROLES + ['HR', 'ACCOUNTS']

# Roles who can view ALL leads - ONLY ADMIN and BUSINESS_HEAD
LEAD_VIEW_ALL_ROLES = ADMIN_ROLES  # This now excludes OPS


class CanAccessLeads(BasePermission):
    """Checks if user role is allowed to access leads"""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in LEAD_ACCESS_ROLES


class CanAssignLeads(BasePermission):
    """
    Admin & OPS: assign to anyone
    Admission Manager: assign to self + Admission Executives
    Admission Executive: assign to self only
    """
    def has_permission(self, request, view):
        user = request.user

        if not user.is_authenticated:
            return False

        if user.role in ADMIN_ROLES or user.role in OPERATIONS_ROLES:
            return True

        if user.role == 'ADM_MANAGER':
            return True

        if user.role == 'ADM_EXEC':
            return True

        return False
