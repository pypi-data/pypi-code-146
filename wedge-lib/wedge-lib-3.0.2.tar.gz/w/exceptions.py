from rest_framework.exceptions import APIException
from w.django.utils import _  # noqa


class ServiceUnavailable(APIException):
    status_code = 503
    default_detail = "Service temporarily unavailable, try again later."


class WError(Exception):
    """
    Base class for exceptions

    Attributes:
        message (str): Error message
        params (dict) : message string params
        code (int): code like HTTP status code
    """

    status_code = 400
    message = "message undefined"

    def __init__(self, message=None, params=None, code=None) -> None:
        if not message:
            message = self.message
        if not code:
            code = self.status_code
        params = params if params else {}
        self.message = _(message) % params
        self.code = code

    def __str__(self) -> str:
        return f"{self.code} - {self.message}"

    def get_message(self):
        return self.message

    def get_code(self):
        return self.code


class InvalidCredentialsError(WError):
    """
    Raised when credentials are invalid
    """

    status_code = 401
    message = "Invalid Credentials"


class NotFoundError(WError):
    """Raised when somethings is not found"""

    status_code = 404

    def __init__(self, message, params=None) -> None:
        super().__init__(message, params)


class AlreadyExistsError(WError):
    """Raised when somethings already exists"""

    status_code = 409

    def __init__(self, message, params=None) -> None:
        super().__init__(message, params)


class ValidationError(WError):
    """Raised when data validation failed"""

    status_code = 422
    message = "Unprocessable Entity"
    detail = None

    def __init__(self, detail=None, params=None) -> None:
        super().__init__(self.message, params)
        self.detail = detail


class AuthenticationTimeoutError(WError):
    """Raise when Authentification Timeout"""

    status_code = 403
    message = "Authentication Timeout"

    def __init__(self, message=None, params=None) -> None:
        super().__init__(message, params)


class AccessForbiddenError(WError):
    """Raise when access is forbidden"""

    status_code = 403
    message = "Access Forbidden"

    def __init__(self, message=None, params=None) -> None:
        super().__init__(message, params)


class BadRequestError(WError):
    """
    Raise on an apparent client (e.g., malformed request syntax, size too large, ...)
    """

    message = "Bad Request"
