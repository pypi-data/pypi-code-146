# vim: set fileencoding=utf-8:

import json


# --- constants ---

ERRNO = -1
"""
Default value for the `errno` argument in thye CoronadoError constructor.  The
constant name adheres to `man errno` error return codes for BSD and Linux
systems.  `ERRNA ::= "Error - not applicable"`, its value is -1 (out of range
for all UNIX systems), and its name doesn't match anything defined in `errno.h`
- this definition is included to have a good default for the `CoronadoError`
constructor that doesn't conflict with any other integer error values.
"""


# +++ classes +++

class CoronadoError(Exception):
    """
    Abstract class, defines the interface for all Coronado exceptions and
    errors.
    """
    def __init__(self, message: str, errno: int = -1):
        self._info = message
        self._errno = errno


    def __str__(self):
        e = {  'tripleInfo': self._info, 'errno': self._errno, }

        return json.dumps(e)


class AuthTokenAPIError(CoronadoError):
    """
    Raised when the access token API fails to produce an access token.
    """

class CallError(CoronadoError):
    """
    Raised when the caller passes an invalid `spec` to any wrapper method, the
    `spec` size is too large, or the `servicePath` or `serviceURL` point to
    a valid resource but have the wrong values.
    """


class DuplicatesDisallowedError(CoronadoError):
    """
    Raised when trying to create a Coronado/triple object based on an
    object spec that already exists (e.g. the externalID for the object
    is already registered with the service, or its assumed name is
    duplicated).
    """


class ForbiddenError(CoronadoError):
    """
    Raised when requesting access to a triple API resource with credentials
    lacking privileges.
    """


class InvalidPayloadError(CoronadoError):
    """
    Raised when a request object is well-formed but somehow violates integrity
    constraints imposed by the service, e.g. providing a duplicate externalID
    to a service that requires  them to be unique.  This exception's textual
    representation is a JSON object with further details regarding the error
    cause.  The object's attributes are:

    - `exception` - set to `InvalidPayloadError`
    - `serviceException` - The remote service exception name, used for
      troubleshooting
    - `info' - A list of strings with further details
    """


class InternalServerError(CoronadoError):
    """
    Raised when the underlying triple API service implementation has fails due
    to an unexpected condition for which there isn't a more suitable error or
    problem description.
    """


class NotFoundError(CoronadoError):
    """
    Raised when performing a search or update operation and the underlying API
    is unable to tie the `objID` to a triple object of the corresponding type.
    """


class NotImplementedError(CoronadoError):
    """
    Raised when the underlying triple service is not implemented.  Similar
    semantics to the built-in `NotImplementedError`.
    """


class ServiceUnavailable(CoronadoError):
    """
    Raised when some back-end service (3rd-party, database, map resolution) is
    not unavailable to process a triple API request.
    """


class UnauthorizedError(CoronadoError):
    """
    Raised when requesting access to a triple API resource without credentials.
    """


class UnexpectedError(CoronadoError):
    """
    Raised when performning a Coronado API call that results in an
    unknown, unexpected, undocumented, weird AF error that nobody knows
    how it happened.
    """


class UnprocessablePayload(CoronadoError):
    """
    Raised when the request payload is well-formed but the server couldn't
    service it for some reason.  This exception's textual representation is a
    JSON object with further details regarding the error cause.
    """


_ERRORS_MAP = {
    400: CallError,
    401: UnauthorizedError,
    403: ForbiddenError,
    404: NotFoundError,
    409: InvalidPayloadError,
    422: UnprocessablePayload,
    501: NotImplementedError,
    503: ServiceUnavailable,
}


# --- service functions ---

def errorFor(statusCode: int, info: str = None) -> object:
    obj = _ERRORS_MAP.get(statusCode, UnexpectedError)

    try:
        d = json.loads(info)
        d['serviceException'] = d['exception']
        d['exception'] = str(obj).replace("'>", '').replace("<class '", '')
        # info = json.dumps(d)
        info = d
    except: # it's a free-form string
        pass

    if issubclass(obj, CoronadoError):
        return obj(info, errno = statusCode)
    elif isinstance(obj, dict):
        return None
    else:
        return UnexpectedError(info, errno = statusCode)

