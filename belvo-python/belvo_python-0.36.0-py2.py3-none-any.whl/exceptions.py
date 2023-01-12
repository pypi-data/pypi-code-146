from typing import Any


class BelvoAPIException(Exception):
    ...


class RequestError(BelvoAPIException):
    def __init__(self, status_code: int, detail: Any):
        self.status_code = status_code  # HTTP Code
        self.detail = detail  # String with a brief description of the error. For detailed information, check our Error documentation on our DevPortal.
