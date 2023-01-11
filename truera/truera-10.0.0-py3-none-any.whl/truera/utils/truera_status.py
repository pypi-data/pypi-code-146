from enum import Enum
from enum import unique
from typing import Optional

import grpc

from truera.client.errors import SimpleException
from truera.client.errors import TruException
from truera.protobuf.public.error_details_pb2 import \
    ErrorDetails  # pylint: disable=no-name-in-module


@unique
class TruEraStatusCode(Enum):
    """
    Mirrors gRPC status codes, see https://developers.google.com/maps-booking/reference/grpc-api/status_codes
    """
    CANCELLED = 1
    UNKNOWN = 2
    INVALID_ARGUMENT = 3
    DEADLINE_EXCEEDED = 4
    NOT_FOUND = 5
    ALREADY_EXISTS = 6
    PERMISSION_DENIED = 7
    RESOURCE_EXHASUTED = 8
    FAILED_PRECONDITION = 9
    ABORTED = 10
    OUT_OF_RANGE = 11
    UNIMPLEMENTED = 12
    INTERNAL = 13
    UNAVAILABLE = 14
    DATA_LOSS = 15
    UNAUTHENTICATED = 16


class TruEraError(TruException):

    def __init__(
        self, code: TruEraStatusCode, message: str,
        details: Optional[ErrorDetails]
    ):
        super().__init__(message)
        self.code = code
        self.message = message
        if not details:
            self.details = ErrorDetails()
        else:
            self.details = details

    def get_code_name(self):
        return self.code.name


class TruEraNotFoundError(TruEraError):

    def __init__(self, message: str, details: Optional[ErrorDetails] = None):
        super().__init__(TruEraStatusCode.NOT_FOUND, message, details)


class TruEraInvalidArgumentError(TruEraError):

    def __init__(self, message: str, details: Optional[ErrorDetails] = None):
        super().__init__(TruEraStatusCode.INVALID_ARGUMENT, message, details)


class TruEraAlreadyExistsError(TruEraError):

    def __init__(self, message: str, details: Optional[ErrorDetails] = None):
        super().__init__(TruEraStatusCode.ALREADY_EXISTS, message, details)


class TruEraInternalError(TruEraError):

    def __init__(self, message: str, details: Optional[ErrorDetails] = None):
        super().__init__(TruEraStatusCode.INTERNAL, message, details)


class TruEraNotImplementedError(TruEraError):

    def __init__(self, message: str, details: Optional[ErrorDetails] = None):
        super().__init__(TruEraStatusCode.UNIMPLEMENTED, message, details)


class TruEraInvalidConfigError(TruEraError):

    def __init__(self, message: str, details: Optional[ErrorDetails] = None):
        super().__init__(TruEraStatusCode.FAILED_PRECONDITION, message, details)


class TruEraUnsupportedError(TruEraError):

    def __init__(self, message: str, details: Optional[ErrorDetails] = None):
        super().__init__(TruEraStatusCode.FAILED_PRECONDITION, message, details)


class TruEraPermissionDeniedError(TruEraError, SimpleException):

    def __init__(self, message: str, details: Optional[ErrorDetails] = None):
        super().__init__(TruEraStatusCode.PERMISSION_DENIED, message, details)


class TruEraPredictionComputationError(TruEraError):

    def __init__(self, message: str, details: Optional[ErrorDetails] = None):
        super().__init__(TruEraStatusCode.INTERNAL, message, details)


class TruEraPredictionUnavailableError(TruEraError):

    def __init__(self, message: str, details: Optional[ErrorDetails] = None):
        super().__init__(TruEraStatusCode.NOT_FOUND, message, details)


class TruEraInfluenceUnavailableError(TruEraError):

    def __init__(self, message: str, details: Optional[ErrorDetails] = None):
        super().__init__(TruEraStatusCode.NOT_FOUND, message, details)


class TruEraUnauthenticatedError(TruEraError):

    def __init__(self, message: str, details: Optional[ErrorDetails] = None):
        super().__init__(TruEraStatusCode.UNAUTHENTICATED, message, details)


class TruEraDeadlineExceededError(TruEraError):

    def __init__(self, message: str, details: Optional[ErrorDetails] = None):
        super().__init__(TruEraStatusCode.DEADLINE_EXCEEDED, message, details)


def set_grpc_context_from_truera_error(truera_error, context):
    grpc_code = getattr(
        grpc.StatusCode, truera_error.get_code_name(), grpc.StatusCode.UNKNOWN
    )
    context.abort_with_details(
        grpc_code, truera_error.message, truera_error.details
    )
