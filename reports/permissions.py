from rest_framework.permissions import BasePermission

REPORT_REVIEWERS = [
    "ADMIN",
    "BUSINESS_HEAD",
    "OPS",
    "GENERAL_MANAGER",
    "HR",
    "CM"
]

class IsReportReviewer(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            request.user.role in REPORT_REVIEWERS
        )


class IsReportOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
