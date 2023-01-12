from http import HTTPStatus
from typing import Self, TypedDict


class ResponseData(TypedDict):
    code: int
    message: str


class Response:
    """Generic response class for all default responses"""

    code: int
    message: str
    __success: bool

    def __init__(self, data: ResponseData) -> None:
        code = data["code"]
        message = data["message"]

        try:
            assert 100 < code < 600
        except AssertionError:
            code = 500

        self.code = code
        self.message = message

    # Reason for ignoring type: Self is actually valid. In new version of Mypy this will be supported.
    @classmethod
    def from_http_status(cls, status: HTTPStatus) -> Self:  # type: ignore
        return cls({"code": status.value, "message": status.phrase})

    @property
    def success(self) -> bool:
        return 200 <= self.code <= 299
