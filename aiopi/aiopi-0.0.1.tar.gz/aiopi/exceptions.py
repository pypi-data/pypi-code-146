from typing import List



class AioPIError(Exception):
    """Base exception for aiopi errors."""


class ResponseError(AioPIError):
    """Raised when the `Errors` property is present in the body of successful
    HTTP response.
    """
    def __init__(self, errors: List[str]) -> None:
        self.errors = errors

    def __str__(self) -> str:
        return "{} errors returned in response body".format(len(self.errors))


class ContentError(AioPIError):
    """Raised when a required property is not present in the body of a successful
    response.
    """


class NoBatchFound(AioPIError):
    """Raised during a batch search if no batches were found for the criteria."""