from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Доступ к редактированию объекта только админу.
    Остальным только чтение.
    """
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated and request.user.is_admin
        )


class IsAdmin(permissions.BasePermission):
    """Доступ только админу."""
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and request.user.is_admin
        )


class IsAdminOrAuthorOrModeratorOrReadOnly(
    permissions.IsAuthenticatedOrReadOnly
):
    """
    Доступ к редактированию объекта админу, автору или модератору.
    Остальным только чтение.
    """
    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_admin
            or request.user.is_moderator
            or obj.author == request.user
        )
