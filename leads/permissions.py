from rest_framework.permissions import BasePermission

# Role hierarchy for assignments
ADMIN_ROLES = ['ADMIN', 'CEO']
OPERATIONS_ROLES = ['OPS']

MANAGER_ROLES = [
    'ADM_MANAGER',
    'ADM_COUNSELLOR',
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
    'ACCOUNTS',
    'DOCUMENTATION'

]

LEAD_ACCESS_ROLES = ADMIN_ROLES + OPERATIONS_ROLES + MANAGER_ROLES + EXECUTIVE_ROLES

LEAD_VIEW_ALL_ROLES = ADMIN_ROLES


class CanAccessLeads(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and 
            request.user.role in LEAD_ACCESS_ROLES
        )


class CanAssignLeads(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if not user.is_authenticated:
            return False
        return user.role in LEAD_ACCESS_ROLES