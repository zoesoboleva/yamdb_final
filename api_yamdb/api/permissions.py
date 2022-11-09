from rest_framework import permissions
from users.models import MODERATOR


class IsAdminModeratorOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or request.method == 'POST'
            and request.user.is_authenticated
            or obj.author == request.user
            or request.user.is_admin
            or request.user.role == MODERATOR
        )

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )


class IsAdmin(permissions.BasePermission):
    """полные права на управление всем контентом проекта.
    Может создавать и удалять произведения,
    категории и жанры. Может назначать роли пользователям."""

    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.is_staff or request.user.is_admin
        )


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS or (
            request.user.is_authenticated
            and (request.user.is_staff or request.user.is_admin)
        )
