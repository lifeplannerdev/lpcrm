from rest_framework.permissions import BasePermission


class IsHR(BasePermission):
    """
    Permission class for HR-only access
    Allows only users with HR role
    """
    def has_permission(self, request, view):
        return (
            request.user and 
            request.user.is_authenticated and 
            request.user.role == 'HR'
        )


class IsHROrAccounts(BasePermission):
    """
    Permission class for HR and Accounts access
    Allows users with HR or ACCOUNTS role
    """
    def has_permission(self, request, view):
        return (
            request.user and 
            request.user.is_authenticated and 
            request.user.role in ['HR', 'ACCOUNTS']
        )


class IsHROrAccountsOrAdmin(BasePermission):
    """
    Permission class for HR, Accounts, and Admin access
    Allows users with HR, ACCOUNTS, or ADMIN role
    """
    def has_permission(self, request, view):
        return (
            request.user and 
            request.user.is_authenticated and 
            request.user.role in ['HR', 'ACCOUNTS', 'ADMIN']
        )


class IsAdminOnly(BasePermission):
    """
    Permission class for Admin-only access
    Allows only users with ADMIN role
    """
    def has_permission(self, request, view):
        return (
            request.user and 
            request.user.is_authenticated and 
            request.user.role == 'ADMIN'
        )
