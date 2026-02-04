from rest_framework.permissions import BasePermission


class IsTrainer(BasePermission):
    """
    Allows access only to trainers
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and hasattr(
            request.user, 'trainer_profile'
        )


class IsTrainerOwnStudent(BasePermission):
    """
    Object-level permission:
    Trainer can access only their own students
    Admin/staff can access all
    """
    def has_object_permission(self, request, view, obj):
        if hasattr(request.user, 'trainer_profile'):
            return obj.trainer == request.user.trainer_profile
        return True
