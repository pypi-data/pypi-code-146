from rest_framework import exceptions, permissions

__all__ = [
    "IsSafeMethods",
    "IsAnonymous",
    "IsValidVersion",
    "CanCreate",
    "CanUpdate",
    "IsUserActive",
]


class IsSafeMethods(permissions.BasePermission):
    """Allows access only if method is in permissions.SAFE_METHODS."""

    def has_permission(self, request, _):
        return request.method in permissions.SAFE_METHODS


class IsAnonymous(permissions.BasePermission):
    """Allows access only if request user is Annonymous."""

    def has_permission(self, request, _):
        return request.user.is_anonymous


class IsValidVersion(permissions.BasePermission):
    """Allows access only if version is in request."""

    def has_permission(self, request, _):
        if not request.version:
            raise exceptions.NotAcceptable()

        return True


class CanCreate(permissions.BasePermission):
    """Allows access only if method is POST."""

    def has_permission(self, request, view):
        return request.method == "POST"


class CanUpdate(permissions.BasePermission):
    """Allows access only if method is either PATCH or PUT."""

    def has_permission(self, request, view):
        return request.method in ["PATCH", "PUT"]


class IsUserActive(permissions.BasePermission):
    """Allows access only if request user is active."""

    def has_permission(self, request, view):
        return request.user.is_active
