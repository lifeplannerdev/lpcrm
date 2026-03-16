from rest_framework.permissions import BasePermission

# Role hierarchy for assignments
ADMIN_ROLES = ['ADMIN', 'CEO']
OPERATIONS_ROLES = ['OPS']

MANAGER_ROLES = [
    'ADM_MANAGER',
    'CM',  
    'BDM',  
]

EXECUTIVE_ROLES = [
    'ADM_EXEC',
    'FOE',  
]

NON_LEAD_ROLES = [
    'PROCESSING',
    'MEDIA',
    'TRAINER',
    'HR',
    'ACCOUNTS'
]

LEAD_ACCESS_ROLES = ADMIN_ROLES + OPERATIONS_ROLES + MANAGER_ROLES + EXECUTIVE_ROLES


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
        return user.role in LEAD_ACCESS_ROLES