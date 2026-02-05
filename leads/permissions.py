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
    Admin can assign to managers
    Managers can sub-assign to their juniors
    OPS can also assign like admin
    """
    def has_permission(self, request, view):
        user = request.user
        if not user.is_authenticated:
            return False
        
        # Admins and OPS can assign
        if user.role in ADMIN_ROLES or user.role in OPERATIONS_ROLES:
            return True
        
        # Managers can sub-assign
        if user.role in MANAGER_ROLES:
            return True
        
        return False
