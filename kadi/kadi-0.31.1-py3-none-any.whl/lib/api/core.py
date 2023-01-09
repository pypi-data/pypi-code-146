# Copyright 2020 Karlsruhe Institute of Technology
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from functools import wraps

from flask import abort
from flask import current_app
from flask_login import current_user

import kadi.lib.constants as const
from .models import AccessToken
from .models import AccessTokenScope
from .utils import get_access_token_scopes
from kadi.ext.db import db
from kadi.lib.api.utils import get_access_token
from kadi.lib.utils import compact_json
from kadi.lib.web import get_error_description
from kadi.lib.web import get_error_message


def json_response(status_code, body=None, headers=None):
    """Return a JSON response to a client.

    :param status_code: The HTTP status code of the response.
    :param body: (optional) The response body, which must be JSON serializable.
    :param headers: (optional) A dictionary of additional response headers.
    :return: The JSON response.
    """
    body = body if body is not None else {}
    headers = headers if headers is not None else {}

    response = current_app.response_class(
        response=compact_json(body), status=status_code, mimetype=const.MIMETYPE_JSON
    )

    for key, value in headers.items():
        response.headers[key] = value

    return response


def json_error_response(
    status_code, message=None, description=None, headers=None, **kwargs
):
    r"""Return a JSON error response to a client.

    Uses :func:`json_response` with the given headers and a body in the following form,
    assuming no additional error information was provided:

    .. code-block:: js

        {
            "code": 404,
            "message": "<message>",
            "description": "<description>",
        }

    :param status_code: See :func:`json_response`.
    :param message: (optional) The error message. Defaults to the result of
        :func:`kadi.lib.web.get_error_message` using the given status code.
    :param description: (optional) The error description. Defaults to the result of
        :func:`kadi.lib.web.get_error_description` using the given status code.
    :param headers: (optional) See :func:`json_response`.
    :param \**kwargs: Additional error information that will be included in the response
        body. All values need to be JSON serializable.
    :return: The JSON response.
    """
    message = message if message is not None else get_error_message(status_code)
    description = (
        description if description is not None else get_error_description(status_code)
    )

    body = {
        "code": status_code,
        "message": message,
        "description": description,
        **kwargs,
    }
    return json_response(status_code, body=body, headers=headers)


def create_access_token(*, name, user=None, expires_at=None, token=None, scopes=None):
    """Convenience function to create a new personal access token including its scopes.

    Uses :meth:`.AccessToken.create` to create the access token and also creates and
    links all given scopes.

    :param user: The user the access token belongs to. Defaults to the current user.
    :param name: The name of the access token.
    :param expires_at: (optional) The expiration date of the access token.
    :param token: (optional) The actual token. Defaults to a token created by
        :meth:`.AccessToken.new_token`.
    :param scopes: (optional) List of scopes in the form of ``"<object>.<action>"``.
    :return: The created access token.
    """
    user = user if user is not None else current_user
    scopes = scopes if scopes is not None else []

    access_token = AccessToken.create(
        user=user, name=name, expires_at=expires_at, token=token
    )
    db.session.flush()

    access_token_scopes = get_access_token_scopes()

    for scope in scopes:
        parts = scope.split(".", 1)
        if len(parts) != 2:
            continue

        object_name, action = parts

        if action in access_token_scopes.get(object_name, []):
            AccessTokenScope.create(
                access_token=access_token, object=object_name, action=action
            )

    return access_token


def check_access_token_scopes(*scopes, operator="and"):
    r"""Check if the current personal access token contains certain scopes.

    :param \*scopes: One or multiple scopes in the form of ``"<object>.<action>"``. See
        :class:`.AccessTokenScope`.
    :param operator: (optional) The operator the given scopes should be combined with.
        One of ``"and"`` or ``"or"``.
    :return: ``True`` if the access token either contains all required scopes, has full
        access or the current request contains no valid access token at all, ``False``
        otherwise or if the given operator is invalid.
    """
    access_token = get_access_token()

    # Either no access token is supplied in the current request or it has full access.
    if access_token is None or access_token.scopes.count() == 0:
        return True

    access_token_scopes = access_token.scopes.with_entities(
        AccessTokenScope.object, AccessTokenScope.action
    ).all()

    required_scopes = []
    for scope in scopes:
        required_scopes.append(tuple(scope.split(".", 1)))

    valid_scopes = [scope in access_token_scopes for scope in required_scopes]

    if (
        operator not in ["and", "or"]
        or (operator == "and" and not all(valid_scopes))
        or (operator == "or" and not any(valid_scopes))
    ):
        return False

    return True


def scopes_required(*scopes, operator="and"):
    r"""Decorator to add required access token scopes to an API endpoint.

    The scopes are only checked if the current request actually contains a valid
    personal access token. Therefore, this decorator only makes sense for public API
    endpoints that can be accessed using a token.

    The scopes are also used when generating the API documentation.

    **Example:**

    .. code-block:: python3

        @blueprint.route("/records")
        @login_required
        @scopes_required("record.read")
        def get_records():
            pass

    :param \*scopes: See :func:`check_access_token_scopes`.
    :param operator: (optional) See :func:`check_access_token_scopes`.
    """

    def decorator(func):
        apidoc_meta = {"scopes": scopes, "operator": operator}

        if hasattr(func, "_apidoc"):
            func._apidoc["scopes_required"] = apidoc_meta
        else:
            func._apidoc = {"scopes_required": apidoc_meta}

        @wraps(func)
        def wrapper(*args, **kwargs):
            if not check_access_token_scopes(*scopes, operator=operator):
                abort(
                    json_error_response(
                        401,
                        description="Access token has insufficient scope.",
                        scopes=scopes,
                    )
                )

            return func(*args, **kwargs)

        return wrapper

    return decorator


def internal(func):
    """Decorator to mark an API endpoint as internal.

    Internal endpoints can only be accessed via the session, not via personal access
    tokens. This is not to be confused with
    :func:`kadi.lib.api.utils.is_internal_api_request`.
    """

    # Save the information about an endpoint being internal for use in the API
    # documentation.
    func._internal = True

    @wraps(func)
    def wrapper(*args, **kwargs):
        access_token = get_access_token()

        if access_token is not None:
            abort(404)

        return func(*args, **kwargs)

    return wrapper


def experimental(func):
    """Decorator to mark an API endpoint as experimental.

    Experimental endpoints can only be called if the ``EXPERIMENTAL_FEATURES`` flag in
    the application's configuration is set.
    """

    # Save the information about an endpoint being experimental for use in the API
    # documentation.
    func._experimental = True

    @wraps(func)
    def wrapper(*args, **kwargs):
        if not current_app.config["EXPERIMENTAL_FEATURES"]:
            abort(404)

        return func(*args, **kwargs)

    return wrapper
