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
    Permission for lead assignment - more permissive than you might think.
    Anyone who can create leads can also see the available users list.
    
    Admin & OPS: assign to managers and executives
    Admission Manager: assign to FOE and Admission Executives
    FOE: assign to self only
    Admission Executive: assign to self only
    """
    def has_permission(self, request, view):
        user = request.user
        if not user.is_authenticated:
            return False
        
        # All roles that can access leads can also view available users
        # The actual assignment restrictions are handled in the serializer
        return user.role in LEAD_ACCESS_ROLES
