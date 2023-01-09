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
from collections import OrderedDict
from functools import wraps
from io import BytesIO
from mimetypes import guess_type
from urllib.parse import urljoin
from urllib.parse import urlparse

from flask import current_app
from flask import flash
from flask import has_request_context
from flask import request
from flask import send_file
from flask import url_for as _url_for
from flask_login import make_next_param
from werkzeug.exceptions import default_exceptions
from werkzeug.http import HTTP_STATUS_CODES
from werkzeug.routing import BaseConverter

import kadi.lib.constants as const
from kadi.lib.cache import memoize_request
from kadi.lib.utils import as_list


class IdentifierConverter(BaseConverter):
    """Custom URL converter for identifiers.

    Automatically uses the same conversions that are applied when creating or updating
    an identifier. See also :func:`kadi.lib.validation.validate_identifier`.
    """

    regex = r"\s*[a-zA-Z0-9-_]+\s*"

    def to_python(self, value):
        return value.strip().lower()


def flash_danger(message):
    """Flash a danger message to the next request.

    Uses :func:`flash` with a fixed ``"danger"`` category.

    :param message: The message to be flashed.
    """
    flash(message, category="danger")


def flash_info(message):
    """Flash an info message to the next request.

    Uses :func:`flash` with a fixed ``"info"`` category.

    :param message: The message to be flashed.
    """
    flash(message, category="info")


def flash_success(message):
    """Flash a success message to the next request.

    Uses :func:`flash` with a fixed ``"success"`` category.

    :param message: The message to be flashed.
    """
    flash(message, category="success")


def flash_warning(message):
    """Flash a warning message to the next request.

    Uses :func:`flash` with a fixed ``"warning"`` category.

    :param message: The message to be flashed.
    """
    flash(message, category="warning")


@memoize_request
def get_locale():
    """Get the current locale.

    The ``locale`` query parameter of the current request will take precedence, followed
    by the locale cookie as configured by ``LOCALE_COOKIE_NAME`` in the application's
    configuration and finally the default locale.

    :return: The current locale. If no valid locale could be found, the default locale
        will be returned.
    """
    default_locale = const.LOCALE_DEFAULT

    if not has_request_context():
        return default_locale

    locale_cookie_name = current_app.config["LOCALE_COOKIE_NAME"]

    if "locale" in request.args:
        locale = request.args.get("locale")
    elif locale_cookie_name in request.cookies:
        locale = request.cookies.get(locale_cookie_name)
    else:
        locale = default_locale

    if locale in const.LOCALES:
        return locale

    return default_locale


def get_preferred_locale():
    """Get the preferred locale of the current user's client.

    :return: The preferred locale. If no matching locale could be found, the default
        locale will be returned.
    """
    return request.accept_languages.best_match(
        list(const.LOCALES), default=const.LOCALE_DEFAULT
    )


def download_bytes(data, download_name, mimetype=None, as_attachment=True):
    """Send a file-like binary object to a client as a file.

    :param data: The data object to send.
    :param download_name: The default name the browser should use when downloading the
        file.
    :param mimetype: (optional) The MIME type of the file. Defaults to a MIME type based
        on the given ``download_name`` or the default MIME type as defined in
        :const:`kadi.lib.constants.MIMETYPE_DEFAULT` if it cannot be guessed.
    :param as_attachment: (optional) Flag indicating whether the file should be
        displayed in the browser instead of being downloaded. Should only be disabled
        for trusted data or data that is safe for displaying.
    :return: The response object.
    """
    if isinstance(data, bytes):
        data = BytesIO(data)

    if mimetype is None:
        mimetype = guess_type(download_name)[0] or const.MIMETYPE_DEFAULT

    return send_file(
        data,
        download_name=download_name,
        mimetype=mimetype,
        as_attachment=as_attachment,
    )


def download_stream(
    data, download_name, mimetype=None, as_attachment=True, content_length=None
):
    """Send an iterable object or generator producing binary data to a client as a file.

    Useful for cases where :func:`download_bytes` cannot be used, as a raw response
    object is used here instead. Note that the resulting response will never be cached.

    :param data: See :func:`download_bytes`.
    :param download_name: See :func:`download_bytes`.
    :param mimetype: (optional) See :func:`download_bytes`.
    :param as_attachment: (optional) See :func:`download_bytes`.
    :param content_length: (optional) The content length of the data in bytes. Will be
        omitted in the response if not provided.
    :return: The response object.
    """
    if mimetype is None:
        mimetype = guess_type(download_name)[0] or const.MIMETYPE_DEFAULT

    headers = {"Cache-Control": "no-cache, max-age=0"}

    if download_name is not None:
        headers["Content-Disposition"] = f"attachment; filename={download_name}"

    if content_length is not None:
        headers["Content-Length"] = content_length

    return current_app.response_class(data, mimetype=mimetype, headers=headers)


def paginated(page_max=None, per_page_max=100):
    """Decorator to parse paginated query parameters.

    Convenience decorator to get and parse the query parameters ``"page"`` and
    ``"per_page"`` from the current request. The former defaults to 1 while the latter
    defaults to 10 if no valid integer values were found. Both parameters will be
    injected into the decorated function as keyword arguments ``page`` and ``per_page``.

    The query parameters are also used when generating the API documentation.

    :param page_max: (optional) The maximum possible value of the ``"page"`` parameter.
    :param per_page_max: (optional) The maximum possible value of the ``"per_page"``
        parameter.
    """

    def decorator(func):
        apidoc_meta = {"page_max": page_max, "per_page_max": per_page_max}

        if hasattr(func, "_apidoc"):
            func._apidoc["pagination"] = apidoc_meta
        else:
            func._apidoc = {"pagination": apidoc_meta}

        @wraps(func)
        def wrapper(*args, **kwargs):
            page = request.args.get("page", 1, type=int)
            page = max(page, 1)

            if page_max is not None:
                page = min(page, page_max)

            per_page = request.args.get("per_page", 10, type=int)
            per_page = min(max(per_page, 1), per_page_max)

            kwargs["page"] = page
            kwargs["per_page"] = per_page

            return func(*args, **kwargs)

        return wrapper

    # Decoration without parentheses.
    if callable(page_max) and per_page_max == 100:
        return paginated()(page_max)

    return decorator


def qparam(
    name,
    location=None,
    multiple=False,
    default="",
    parse=None,
    description="",
):
    """Decorator to parse a query parameter.

    Convenience decorator to retrieve and parse a specified query parameter from the
    current request. The decorator can be applied multiple times. Each parameter will be
    injected into the decorated function as part a dictionary inside the keyword
    argument ``qparams``. The dictionary maps each given parameter name to its
    respective value.

    The query parameter is also used when generating the API documentation.

    :param name: The name of both the query parameter and the dictionary key that is
        injected into the decorated function.
    :param location: (optional) The name of the query parameter to use instead of
        ``name``.
    :param multiple: (optional) Flag indicating whether the query parameter can be
        specified multiple times and should be retrieved as list value.
    :param default: (optional) The default value or a callable returning a default value
        to use in case the query parameter is missing and ``multiple`` is ``False``,
        otherwise the default value will always be an empty list.
    :param parse: (optional) A callable or list of callables to parse the parameter
        value if it is not missing. Each callable must take and return a single
        parameter value. If parsing fails with a ``ValueError``, the default value is
        taken instead if ``multiple`` is ``False``, otherwise each invalid value is
        removed from the resulting list.
    :param description: (optional) A description of the query parameter, which is only
        used when generating the API documentation. Supports reST syntax.
    """
    location = location if location is not None else name
    parse = parse if parse is not None else []
    parse = as_list(parse)

    def decorator(func):
        # If a callable was provided, it needs to be evaluated each time.
        def _get_default_value(default):
            return default if not callable(default) else default()

        apidoc_meta = {
            "multiple": multiple,
            "default": _get_default_value(default),
            "description": description,
        }

        if hasattr(func, "_apidoc"):
            if "qparams" in func._apidoc:
                func._apidoc["qparams"][location] = apidoc_meta
                func._apidoc["qparams"].move_to_end(location, last=False)
            else:
                func._apidoc["qparams"] = OrderedDict([(location, apidoc_meta)])
        else:
            func._apidoc = {"qparams": OrderedDict([(location, apidoc_meta)])}

        @wraps(func)
        def wrapper(*args, **kwargs):
            parse_value = True

            if multiple:
                value = request.args.getlist(location)
            else:
                if location in request.args:
                    value = request.args.get(location)
                else:
                    value = _get_default_value(default)
                    # Skip parsing in case we fall back to the default value.
                    parse_value = False

            if parse_value:
                for parse_func in parse:
                    if multiple:
                        values = []

                        for _value in value:
                            try:
                                values.append(parse_func(_value))
                            except ValueError:
                                pass

                        value = values
                    else:
                        try:
                            value = parse_func(value)
                        except ValueError:
                            value = _get_default_value(default)
                            break

            if "qparams" in kwargs:
                kwargs["qparams"][name] = value
            else:
                kwargs["qparams"] = {name: value}

            return func(*args, **kwargs)

        return wrapper

    return decorator


def url_for(endpoint, _ignore_version=False, **values):
    r"""Generate an URL based on a given endpoint.

    Wraps Flask's ``url_for`` function with additional support for generating the
    correct URLs when using API versioning. Additionally, generated URLs are always
    external, i.e. absolute.

    :param endpoint: The endpoint (name of the function) of the URL.
    :param _ignore_version: (optional) Flag indicating whether the API version should be
        ignored when building the URL in API requests.
    :param \**values: The variable arguments of the URL rule.
    :return: The generated URL string.
    """
    from kadi.lib.api.utils import get_api_version, is_api_request

    values["_external"] = True

    if not _ignore_version and is_api_request():
        api_version = get_api_version()

        if api_version is not None:
            _endpoint = f"{endpoint}_{api_version}"

            # In case the endpoint is not actually versioned, we just fall back to the
            # original one that was passed in.
            try:
                return _url_for(_endpoint, **values)
            except:
                pass

    return _url_for(endpoint, **values)


def static_url(filename):
    """Generate a static URL for a given filename.

    Will make use of the ``MANIFEST_MAPPING`` if it is defined in the application's
    configuration and if an entry exists for the given filename.

    :param filename: The name of the file to include in the URL.
    :return: The generated URL string.
    """
    manifest_mapping = current_app.config["MANIFEST_MAPPING"]

    if manifest_mapping is None:
        return url_for("static", filename=filename)

    return url_for("static", filename=manifest_mapping.get(filename, filename))


def make_next_url(next_url):
    """Create a URL to redirect a user to after login.

    :param next_url: A URL to redirect to, which will be included as a ``next`` query
        parameter in the generated URL.
    :return: The generated URL.
    """
    next_param = make_next_param(url_for("accounts.login"), next_url)
    return url_for("accounts.login", next=next_param)


def get_next_url(fallback=None):
    """Get the validated target URL to redirect a user to after login.

    The target URL has to be specified as a ``next`` query parameter in the current
    request and needs to redirect to an internal page.

    :param fallback: (optional) The fallback URL to use in case the target URL was
        invalid or could not be found. Defaults to the index page.
    :return: The validated target URL.
    """
    if has_request_context() and "next" in request.args:
        next_url = request.args.get("next")

        ref_url = urlparse(request.host_url)
        test_url = urlparse(urljoin(request.host_url, next_url))

        if test_url.scheme in ["http", "https"] and ref_url.netloc == test_url.netloc:
            return next_url

    return fallback if fallback is not None else url_for("main.index")


def get_error_message(status_code):
    """Get an error message corresponding to an HTTP status code.

    :param status_code: The HTTP status code.
    :return: The error message.
    """
    return HTTP_STATUS_CODES.get(status_code, "Unknown error")


def get_error_description(status_code):
    """Get an error description corresponding to an HTTP status code.

    :param status_code: The HTTP status code.
    :return: The error description.
    """
    exc = default_exceptions.get(status_code)

    if exc is not None:
        return exc.description

    return "An unknown error occured."
