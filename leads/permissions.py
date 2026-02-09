from rest_framework.permissions import BasePermission

# Role hierarchy for assignments
ADMIN_ROLES = ['ADMIN', 'BUSINESS_HEAD']
OPERATIONS_ROLES = ['OPS']

MANAGER_ROLES = [
    'ADM_MANAGER',
    'CM',  # Center Manager
    'BDM',  # Business Development Manager
]

EXECUTIVE_ROLES = [
    'ADM_EXEC',
    'FOE',  # Front Office Executive - CAN handle leads and assign to self
]

# Roles that should NOT handle leads (but may have system access for other purposes)
NON_LEAD_ROLES = [
    'PROCESSING',
    'MEDIA',
    'TRAINER',
    'HR',
    'ACCOUNTS'
]

# Roles allowed to access leads API
LEAD_ACCESS_ROLES = ADMIN_ROLES + OPERATIONS_ROLES + MANAGER_ROLES + EXECUTIVE_ROLES

# Roles who can view ALL leads - ONLY ADMIN and BUSINESS_HEAD
LEAD_VIEW_ALL_ROLES = ADMIN_ROLES


class CanAccessLeads(BasePermission):
    """Checks if user role is allowed to access leads"""
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and 
            request.user.role in LEAD_ACCESS_ROLES
        )


class CanAssignLeads(BasePermission):
    """
    Admin & OPS: assign to managers and executives
    Admission Manager: assign to FOE and Admission Executives
    FOE: assign to self only
    Admission Executive: assign to self only
    """
    def has_permission(self, request, view):
        user = request.user
        if not user.is_authenticated:
            return False
        
        # Admin and OPS can assign
        if user.role in ADMIN_ROLES or user.role in OPERATIONS_ROLES:
            return True
        
        # Managers can sub-assign to executives
        if user.role in MANAGER_ROLES:
            return True
        
        # Executives (including FOE) can assign to themselves
        if user.role in EXECUTIVE_ROLES:
            return True
        
        return False
