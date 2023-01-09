import sys

from django.urls import resolve
from rest_framework.permissions import BasePermission


class IsViewPermitted(BasePermission):
    """
    Permission check if the user is allowed to access the view
    """

    def has_permission(self, request, view):
        user = request.user
        app_label = sys.modules[resolve(request.path_info).func.__module__].__package__
        url_name = resolve(request.path_info).url_name
        view_name = f'{app_label}:{url_name}'
        permissions = []
        for permission in user.get_group_permissions():
            try:
                index = permission.index('.')
                permissions.append(permission[index + 1:])
            except ValueError:
                permissions.append(permission)
        return view_name in permissions
