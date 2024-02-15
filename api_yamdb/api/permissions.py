from rest_framework import permissions

from users.models import ROLE_CHOICES


class IsAdminUser(permissions.BasePermission):

    message = 'Данный запрос недоступен для вас.'

    def has_permission(self, request, view):
        return request.user.is_admin


class IsAdminOrReadOnly(permissions.BasePermission):

    message = 'Данный запрос недоступен для вас.'

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_admin)


class IsAuthorModeratorOrAdmin(permissions.BasePermission):

    message = 'Данный запрос недоступен для вас.'

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or (
                obj.author == request.user
                or request.user.is_moderator
                or request.user.is_admin
                or request.user.is_superuser
            )
            
        )
