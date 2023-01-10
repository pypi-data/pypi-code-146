from __future__ import annotations

from typing import Tuple


class StrangeworksError(Exception):
    """
    StrangeworksError is a standardized error message
    that can easily be parsed by the Strangeworks-Python-Core
    """

    def __init__(
        self,
        message: str = "",
        status_code: int = 0,
        error: str = "",
    ):
        self.message = message
        self.status_code = status_code
        self.error = error

    @classmethod
    def authentication_error(cls, message: str = None):
        default_message = (
            "authentication is invalid, utilize client.authenticate() to refresh",
        )
        return StrangeworksError(message=message or default_message, status_code=401)

    @classmethod
    def user_error(cls, message) -> StrangeworksError:
        return StrangeworksError(message, 400, "")

    @classmethod
    def not_found_error(cls, message) -> StrangeworksError:
        return StrangeworksError(message, 404, "")

    @classmethod
    def forbidden_error(cls, message="") -> StrangeworksError:
        return StrangeworksError(message, 401, "")

    @classmethod
    def vendor_error(cls, exception="") -> StrangeworksError:
        msg = "There was an issue reaching the vendor with the request."

        return StrangeworksError(
            "There was an issue reaching the vendor with the request.",
            msg,
            400,
            exception,
        )

    @classmethod
    def unknown_error(cls, exception) -> StrangeworksError:
        msg = "Something went wrong while processing this request."

        return StrangeworksError(
            msg,
            400,
            exception,
        )

    @classmethod
    def key_error(cls) -> StrangeworksError:
        return StrangeworksError(
            "No valid keys found.",
            401,
            "",
        )

    @classmethod
    def server_error(cls, e: Exception) -> StrangeworksError:
        msg = (
            e.message if hasattr(e, "message") else "An error ocurred at Strangeworks."
        )

        return StrangeworksError(
            msg,
            400,
            str(e),
        )

    def return_error(self) -> Tuple[dict, int]:
        """
        return error is used at the custom error handler
        to return known errors from strangeworks
        """
        return {"message": self.message, "error": self.error}, self.status_code
