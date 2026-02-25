from rest_framework.permissions import BasePermission


class IsHR(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user and 
            request.user.is_authenticated and 
            request.user.role == 'HR'
        )


class IsHROrAccounts(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user and 
            request.user.is_authenticated and 
            request.user.role in ['HR', 'ACCOUNTS']
        )


class IsHROrAccountsOrAdmin(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user and 
            request.user.is_authenticated and 
            request.user.role in ['HR', 'ACCOUNTS', 'ADMIN']
        )


class IsAdminOnly(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user and 
            request.user.is_authenticated and 
            request.user.role == 'ADMIN'
        )

