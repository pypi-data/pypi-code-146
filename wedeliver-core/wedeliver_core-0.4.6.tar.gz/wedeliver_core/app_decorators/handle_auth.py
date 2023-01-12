from functools import wraps

from flask import request

from wedeliver_core.helpers.auth import verify_user_token
from wedeliver_core.helpers.exceptions import (
    AppValidationError,
    AppMissingAuthError,
)


def handle_auth(require_auth, append_auth_args=None, allowed_roles=None):
    def factory(func):
        @wraps(func)
        def inner_function(*args, **kws):
            if not require_auth:
                return func(*args, **kws)

            if "Authorization" not in request.headers:
                raise AppMissingAuthError("Missing authentication")

            token = request.headers["Authorization"]
            if "country_code" not in request.headers and request.endpoint != "health_check":
                raise AppValidationError("Country Code is Required (c)")

            user = verify_user_token(token=token)

            has_valid_role = True
            if allowed_roles and len(allowed_roles):
                user_role = user.get('role')
                if user_role not in allowed_roles:
                    has_valid_role = False

            if not has_valid_role:
                raise AppMissingAuthError("You have not enough permission")

            if append_auth_args and isinstance(append_auth_args, list):
                for arg in append_auth_args:
                    if not kws.get('appended_kws'):
                        kws['appended_kws'] = dict()

                    kws['appended_kws'][arg] = user.get(arg)

            return func(*args, **kws)

        return inner_function

    return factory
