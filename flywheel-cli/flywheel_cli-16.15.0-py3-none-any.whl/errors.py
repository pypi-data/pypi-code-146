"""Flywheel CLI global errors"""

from typing import Optional


class BaseError(Exception):
    """Base exception"""

    message: str = "Unknown exception"

    def __init__(self, msg: Optional[str] = None):
        if msg:
            self.message = msg
        super().__init__(self.message)


class AuthenticationError(BaseError):
    """Authentication failed"""

    message: str = "Authentication error"
    code = 403

    def __init__(self, msg: str, code: Optional[int] = None):
        super().__init__(msg)
        if code:
            self.code = code


class NotEnoughPermissions(BaseError):
    """Permission error"""

    message: str = "The user does not have the required permissions for this action"


class S3AccessDeniedError(BaseError):
    """AccessDenied on S3"""

    message: str = "Access denied"
    code = 403

    def __init__(
        self,
        s3_location: str,
        s3_user: str,
        msg: Optional[str] = None,
        code: Optional[int] = None,
    ):
        if not msg:
            msg = f"User {s3_user} cannot perform scan on {s3_location} "
        super().__init__(msg)
        if code:
            self.code = code
        self.s3_location = s3_location
        self.s3_user = s3_user
