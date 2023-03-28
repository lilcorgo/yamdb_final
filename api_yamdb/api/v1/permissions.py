from rest_framework.permissions import (
    BasePermission,
    SAFE_METHODS,
    IsAuthenticatedOrReadOnly
)


class IsAdminOrReadOnly(BasePermission):
    """
    Доступ к редактированию объекта только админу.
    Остальным только чтение.
    """
    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or request.user.is_authenticated and request.user.is_admin
        )


class IsAdmin(BasePermission):
    """Доступ только админу."""
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and request.user.is_admin
        )


class IsAdminOrAuthorOrModeratorOrReadOnly(IsAuthenticatedOrReadOnly):
    """
    Доступ к редактированию объекта админу, автору или модератору.
    Остальным только чтение.
    """
    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS
            or request.user.is_admin
            or request.user.is_moderator
            or obj.author == request.user
        )
