import logging
from typing import Optional

from the_spymaster_util.http_client import JsonType

log = logging.getLogger(__name__)


class ApiError(Exception):
    def __init__(
        self,
        message: str = "Internal server error",
        status_code: int = 500,
        details: Optional[JsonType] = None,
    ):
        self.message = message
        self.status_code = status_code
        self.details = details
        super().__init__(message)


class BadRequestError(ApiError):
    def __init__(self, message: str, status_code: int = 400, details: Optional[JsonType] = None):
        super().__init__(message=message, status_code=status_code, details=details)


class UnauthorizedError(BadRequestError):
    def __init__(self, message: str):
        super().__init__(message=message, status_code=401)


class ForbiddenError(BadRequestError):
    def __init__(self, message: str):
        super().__init__(message=message, status_code=403)


class NotFoundError(BadRequestError):
    def __init__(self, message: str):
        super().__init__(message=message, status_code=404)
