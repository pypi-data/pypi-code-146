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
import math
import re
from collections import OrderedDict
from copy import deepcopy
from functools import wraps

from flask import abort
from flask import current_app
from flask import has_request_context
from flask import request

import kadi.lib.constants as const
from .models import AccessToken
from kadi.ext.db import db
from kadi.lib.cache import memoize_request
from kadi.lib.db import get_class_by_tablename
from kadi.lib.utils import rgetattr
from kadi.lib.web import url_for


def status(status_code, description):
    """Decorator to add response status information to an API endpoint.

    This information is currently only used when generating the API documentation.

    :param status_code: The status code of the response.
    :param description: The description corresponding to the status code, describing
        when the status code occurs or whether there is a response body. Supports reST
        syntax.
    """

    def decorator(func):
        if hasattr(func, "_apidoc"):
            if "status_codes" in func._apidoc:
                func._apidoc["status_codes"][status_code] = description
                func._apidoc["status_codes"].move_to_end(status_code, last=False)
            else:
                func._apidoc["status_codes"] = OrderedDict([(status_code, description)])
        else:
            func._apidoc = {"status_codes": OrderedDict([(status_code, description)])}

        return func

    return decorator


def reqschema(schema, description="", bind=True):
    """Decorator to add request body information to an API endpoint using a schema.

    This information is mainly used when generating the API documentation.

    :param schema: The schema class or instance to use as base for the request body
        information.
    :param description: (optional) Additional description of the request body. Supports
        reST syntax.
    :param bind: (optional) Flag indicating whether the schema should also be injected
        into the decorated function as keyword argument ``schema``.
    """
    if isinstance(schema, type):
        schema = schema()

    def decorator(func):
        apidoc_meta = {"schema": schema, "description": description}

        if hasattr(func, "_apidoc"):
            func._apidoc["reqschema"] = apidoc_meta
        else:
            func._apidoc = {"reqschema": apidoc_meta}

        @wraps(func)
        def wrapper(*args, **kwargs):
            if bind:
                kwargs["schema"] = schema

            return func(*args, **kwargs)

        return wrapper

    return decorator


def reqform(form_data, description="", enctype="multipart/form-data"):
    """Decorator to add request body information to an API endpoint using form data.

    This information is currently only used when generating the API documentation.

    :param form_data: The request body information as a list of tuples in the following
        form:

        .. code-block:: python3

            [
                (
                    "<field>",
                    {
                        # Defaults to "String".
                        "type": "Integer",
                        # Defaults to False.
                        "required": True,
                        # The default value will be converted to a string.
                        "default": 1,
                    }

                )
            ]

    :param description: (optional) Additional description of the request body. Supports
        reST syntax.
    :param enctype: (optional) The encoding type of the form data.
    """

    def decorator(func):
        apidoc_meta = {
            "form_data": form_data,
            "description": description,
            "enctype": enctype,
        }

        if hasattr(func, "_apidoc"):
            func._apidoc["reqform"] = apidoc_meta
        else:
            func._apidoc = {"reqform": apidoc_meta}

        return func

    return decorator


def is_api_request():
    """Check if the current request is an API request.

    A request is an API request if the path of the current request path starts with
    ``"/api"``.

    :return: ``True`` if the request is an API request, ``False`` otherwise.
    """
    return (
        has_request_context() and re.match(r"^\/api($|\/.*)$", request.path) is not None
    )


def is_internal_api_request():
    """Check if the current API request is an "internal" one.

    An API request is marked as internal if it includes a query parameter ``_internal``
    with any value (e.g. ``"https://...?_internal=true"``). It does not matter whether
    the request uses the session or a personal access token. This can be useful for e.g.
    returning additional data that is only relevant for internal use.

    :return: ``True`` if the request is internal, ``False`` otherwise.
    """
    return is_api_request() and request.args.get("_internal") is not None


def get_api_version():
    """Get the API version from the current request path.

    :return: The current API version or ``None`` if the current request is not an API
        request or no valid version is found.
    """
    if is_api_request():
        parts = request.path[1:].split("/")

        if len(parts) >= 2:
            api_version = parts[1]

            if api_version in const.API_VERSIONS:
                return api_version

    return None


@memoize_request
def get_access_token():
    """Get a personal access token from the current request.

    The token has to be included as a "Bearer" token within an "Authorization" header.

    :return: An access token object or ``None`` if no valid token can be found or no
        request context currently exists.
    """
    if has_request_context():
        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return None

        parts = auth_header.split(None, 1)

        if len(parts) == 2 and parts[0].lower() == "bearer":
            return AccessToken.get_by_token(parts[1])

    return None


def get_access_token_scopes():
    """Get all possible access token scopes.

    The possible scopes are combined from all possible permissions (i.e. regular and
    global actions) of the different resources and some additional scopes as defined in
    :const:`kadi.lib.constants.ACCESS_TOKEN_SCOPES`.

    :return: A dictionary mapping a scope's object to its respective actions.
    """
    scopes = deepcopy(const.ACCESS_TOKEN_SCOPES)

    for object_name in db.metadata.tables:
        model = get_class_by_tablename(object_name)
        permissions = rgetattr(model, "Meta.permissions")

        if permissions is not None:
            scopes[object_name] = []

            for action, _ in permissions.get("global_actions", []) + permissions.get(
                "actions", []
            ):
                scopes[object_name].append(action)

    return scopes


def create_pagination_data(total, page, per_page, endpoint=None, **kwargs):
    r"""Create pagination information for use in a JSON response.

    Since the pagination data will include links to the current, next and previous
    "pages", the necessary information to build said links needs to be given as well,
    i.e. the endpoint and its corresponding URL parameters.

    :param total: The total amount of items.
    :param page: The current page.
    :param per_page: Items per page.
    :param endpoint: The endpoint used to build links to the current, next and previous
        page. Defaults to the endpoint of the current request.
    :param \**kwargs: Additional keyword arguments to build the links with.
    :return: The pagination information as dictionary in the following form:

        .. code-block:: python3

            {
                "_pagination": {
                    "page": 2,
                    "per_page": 10,
                    "total_pages": 3,
                    "total_items": 25,
                    "_links": {
                        "prev": "https://...?page=1&...",
                        "self": "https://...?page=2&...",
                        "next": "https://...?page=3&...",
                    }
                }
            }

        The list of items is initially empty and can be filled afterwards with whatever
        data should be returned. Note that the links to the previous and next pages are
        only present if the respective page actually exists.
    """
    endpoint = endpoint if endpoint is not None else request.endpoint

    has_next = total > page * per_page
    has_prev = page > 1
    total_pages = math.ceil(total / per_page) or 1

    url_args = {"endpoint": endpoint, "per_page": per_page, **kwargs}

    data = {
        "_pagination": {
            "page": page,
            "per_page": per_page,
            "total_pages": total_pages,
            "total_items": total,
            "_links": {"self": url_for(page=page, **url_args)},
        },
    }

    if has_next:
        data["_pagination"]["_links"]["next"] = url_for(page=page + 1, **url_args)
    if has_prev:
        data["_pagination"]["_links"]["prev"] = url_for(page=page - 1, **url_args)

    return data


def check_max_content_length():
    """Check whether the current request exceeds the maximum configured content length.

    This can be used in places where the content length is not checked automatically,
    which currently is only done when parsing form data.

    Will make use of the ``MAX_CONTENT_LENGTH`` in the application's configuration. If
    the content length is exceeded, automatically aborts the current request with a JSON
    error response and status code 413.
    """
    from .core import json_error_response

    if (
        request.content_length is not None
        and request.content_length > current_app.config["MAX_CONTENT_LENGTH"]
    ):
        # Make sure to explicitely exhaust the stream when using the development server.
        if current_app.environment == const.ENV_DEVELOPMENT:
            request.stream.exhaust()

        abort(json_error_response(413))
