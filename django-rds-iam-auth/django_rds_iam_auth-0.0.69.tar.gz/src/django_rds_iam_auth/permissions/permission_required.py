from functools import wraps
from typing import Tuple

from rest_framework.response import Response


def permission_required(permission_names: Tuple):
    """
    Decorator for views that checks whether a user has a particular permission
    in format app_label.permission_code
    """

    def _method_wrapper(view_method):

        @wraps(view_method)
        def _arguments_wrapper(request, *args, **kwargs):
            """
            Wrapper with arguments to invoke the method
            """

            if not request.request.user.role.permissions.filter(codename__in=permission_names).exists():
                return Response('You have not permissions to this view', status=403)

            return view_method(request, *args, **kwargs)

        return _arguments_wrapper

    return _method_wrapper
