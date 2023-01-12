import logging
from typing import Any, Dict
from django.http import Http404
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from rest_framework import exceptions, status
from rest_framework.response import Response
from rest_framework.views import set_rollback
from vanoma_api_utils.constants import ERROR_CODE
from .responses import generic_error
from ..exceptions import BackendServiceException

EMPTY_STRING = ""


def _extract_message_from_detail(detail: Any) -> str:
    if isinstance(detail, list):
        errors = [_extract_message_from_detail(d) for d in detail]
        # Return the first error. Subsequent errors will be shown once the user fixes the first one.
        # This is so we can keep the "message" returned in the error as a whole string.
        for error in errors:
            # It's possible for error to be an empty string (see below). Return the first non-None error.
            if error != EMPTY_STRING:
                return error
        # We shouldn't get here in theory, but just in case we returned empty strings from below.
        return EMPTY_STRING
    elif isinstance(detail, dict):
        # Return the first error. Subsequent errors will be shown once the user fixes the first one.
        # This is so we can keep the "message" returned in the error as a whole string.
        for key, value in detail.items():
            if str(key).strip().lower() == "non_field_errors":
                return _extract_message_from_detail(value)

            return f"{key}: {_extract_message_from_detail(value)}"
        # We have an empty dictionary which can happen if one of the fields of a modal has no validation
        # errors. See https://sentry.io/share/issue/a031ebc008fe4aee8c0c131e1c747418/
        return EMPTY_STRING
    else:
        return str(detail)


def exception_handler(exc: Exception, context: Dict[str, Any]) -> Response:
    """
    Mostly copied from https://github.com/encode/django-rest-framework/blob/master/rest_framework/views.py#L71
    """
    if isinstance(exc, Http404) or isinstance(exc, ObjectDoesNotExist):
        return generic_error(
            status.HTTP_404_NOT_FOUND,
            ERROR_CODE.RESOURCE_NOT_FOUND,
            str(exc),
        )

    if isinstance(exc, PermissionDenied):
        return generic_error(
            status.HTTP_403_FORBIDDEN,
            ERROR_CODE.AUTHORIZATION_ERROR,
            str(exc),
        )

    if isinstance(exc, exceptions.APIException):
        set_rollback()
        return generic_error(
            exc.status_code,
            ERROR_CODE.INVALID_REQUEST,
            _extract_message_from_detail(exc.detail),
        )

    if isinstance(exc, BackendServiceException) and exc.is_client_side():
        set_rollback()
        return generic_error(
            exc.status_code,
            ERROR_CODE(exc.error_code),
            exc.error_message,
        )

    # This will sent the current exception to sentry - https://docs.sentry.io/platforms/python/guides/logging/
    logging.exception(str(exc))

    return generic_error(
        status.HTTP_500_INTERNAL_SERVER_ERROR, ERROR_CODE.INTERNAL_ERROR, str(exc)
    )
