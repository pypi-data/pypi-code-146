from rest_framework import permissions


class IsCreator(permissions.BasePermission):
    """Allow access only for the creator of the object."""

    def has_object_permission(self, request, view, obj):
        return obj.creator == request.user
