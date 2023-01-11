"""Defines context managers to assert that SiLA Errors are raised"""
import binascii
import re
from base64 import standard_b64decode
from types import TracebackType
from typing import Callable, Generic, Literal, Optional, Type, TypeVar

import google.protobuf.message
import grpc
from pytest import fail

from sila2_interop_communication_tester.grpc_stubs.SiLABinaryTransfer_pb2 import BinaryTransferError
from sila2_interop_communication_tester.grpc_stubs.SiLAFramework_pb2 import (
    DefinedExecutionError,
    FrameworkError,
    SiLAError,
    UndefinedExecutionError,
    ValidationError,
)

_ErrorType = TypeVar(
    "_ErrorType", ValidationError, FrameworkError, DefinedExecutionError, UndefinedExecutionError, BinaryTransferError
)
_ErrorTypeName = Literal[
    "validationError", "frameworkError", "definedExecutionError", "undefinedExecutionError", "BinaryTransferError"
]
_FrameworkErrorType = Literal[
    "COMMAND_EXECUTION_NOT_ACCEPTED",
    "INVALID_COMMAND_EXECUTION_UUID",
    "COMMAND_EXECUTION_NOT_FINISHED",
    "INVALID_METADATA",
    "NO_METADATA_ALLOWED",
]
_BinaryTransferErrorType = Literal[
    "BINARY_UPLOAD_FAILED",
    "BINARY_DOWNLOAD_FAILED",
    "INVALID_BINARY_TRANSFER_UUID",
]


class ErrorOption(Generic[_ErrorType]):
    def __init__(self):
        self.error: Optional[_ErrorType] = None


class RaisesContext(Generic[_ErrorType]):
    # adapted from pytest.raises
    def __init__(self, error_type: _ErrorTypeName, check_func: Optional[Callable[[_ErrorType], None]] = None) -> None:
        self.error_type = error_type
        self.error_option: ErrorOption[_ErrorType] = ErrorOption()
        self.check_func: Optional[Callable[[_ErrorType], None]] = check_func

    def __enter__(self) -> ErrorOption[_ErrorType]:
        return self.error_option

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> Optional[bool]:
        __tracebackhide__ = True

        if exc_type is None:
            fail("Expected a gRPC error, but no exception was caught")

        if not issubclass(exc_type, grpc.RpcError):
            return False

        assert isinstance(exc_val, grpc.RpcError), "Caught a non-gRPC error (probably an internal error in test suite)"
        assert isinstance(exc_val, grpc.Call), "Caught a non-gRPC error (probably an internal error in test suite)"
        assert (
            exc_val.code() == grpc.StatusCode.ABORTED
        ), f"Caught gRPC error with wrong status code (expected {grpc.StatusCode.ABORTED}, got {exc_val.code()})"

        try:
            proto_bytes = standard_b64decode(exc_val.details())
        except binascii.Error:
            fail("Failed to decode error details as Base64")
            return

        specific_error: _ErrorType
        if self.error_type != "BinaryTransferError":
            try:
                error = SiLAError.FromString(proto_bytes)
            except google.protobuf.message.DecodeError:
                fail("Failed to decode error details as SiLAFramework.SiLAError Protobuf message")
                return

            assert error.HasField(
                self.error_type
            ), f"Caught SiLA Error of wrong type (expected '{self.error_type}', got '{error.WhichOneof('error')}')"

            specific_error = getattr(error, self.error_type)
        else:
            try:
                specific_error = BinaryTransferError.FromString(proto_bytes)
            except google.protobuf.message.DecodeError:
                fail("Failed to decode error details as SiLAFramework.SiLAError Protobuf message")
                return

        assert (
            len(specific_error.message) > 10
        ), "Error message was less than 10 characters long (SiLA Errors must include information about the error)"

        if self.check_func is not None:
            self.check_func(specific_error)

        self.error_option.error = specific_error
        return True


def raises_defined_execution_error(error_identifier: str) -> RaisesContext[DefinedExecutionError]:
    """
    Equivalent to `pytest.raises` for a SiLA Defined Execution Error with the given fully qualified error identifier
    """

    def check_func(error: DefinedExecutionError) -> None:
        assert error.errorIdentifier == error_identifier, (
            f"Caught DefinedExecutionError with wrong errorIdentifier "
            f"(expected '{error_identifier}', got '{error.errorIdentifier}')"
        )

    return RaisesContext("definedExecutionError", check_func)


def raises_undefined_execution_error() -> RaisesContext[UndefinedExecutionError]:
    """Equivalent to `pytest.raises` for a SiLA Undefined Execution Error"""
    return RaisesContext("undefinedExecutionError")


def raises_validation_error(parameter_identifier_regex: str) -> RaisesContext[ValidationError]:
    """
    Equivalent to `pytest.raises` for a SiLA Validation Error with a fully qualified parameter identifier
    matching the given pattern
    """

    def check_func(error: ValidationError) -> None:
        assert re.fullmatch(parameter_identifier_regex, error.parameter), (
            f"Caught ValidationError for wrong parameter "
            f"(expected '{parameter_identifier_regex}', got '{error.parameter}')"
        )

    return RaisesContext("validationError", check_func)


def __raises_framework_error(error_type: _FrameworkErrorType) -> RaisesContext[FrameworkError]:
    error_type = getattr(FrameworkError.ErrorType, error_type)

    def check_func(error: FrameworkError) -> None:
        assert (
            error.errorType == error_type
        ), f"Caught FrameworkError with wrong errorType (expected '{error_type}', got '{error.errorType}')"

    return RaisesContext("frameworkError", check_func)


def raises_command_execution_not_accepted_error():
    """Equivalent to `pytest.raises` for a SiLA Command Execution Not Accepted Error"""
    return __raises_framework_error("COMMAND_EXECUTION_NOT_ACCEPTED")


def raises_invalid_command_execution_uuid_error():
    """Equivalent to `pytest.raises` for a SiLA Invalid Command Execution UUID Error"""
    return __raises_framework_error("INVALID_COMMAND_EXECUTION_UUID")


def raises_command_execution_not_finished_error():
    """Equivalent to `pytest.raises` for a SiLA Command Execution Not Finished Error"""
    return __raises_framework_error("COMMAND_EXECUTION_NOT_FINISHED")


def raises_invalid_metadata_error():
    """Equivalent to `pytest.raises` for a SiLA Invalid Metadata Error"""
    return __raises_framework_error("INVALID_METADATA")


def raises_no_metadata_allowed_error():
    """Equivalent to `pytest.raises` for a SiLA No Metadata Allowed Error"""
    return __raises_framework_error("NO_METADATA_ALLOWED")


def __raises_binary_transfer_error(error_type: _BinaryTransferErrorType) -> RaisesContext[BinaryTransferError]:
    error_type = getattr(BinaryTransferError.ErrorType, error_type)

    def check_func(error: BinaryTransferError) -> None:
        assert error.errorType == error_type, (
            f"Caught BinaryTransferError with wrong errorType "
            f"(expected '{BinaryTransferError.ErrorType.Name(error_type)}', "
            f"got '{BinaryTransferError.ErrorType.Name(error.errorType)}')"
        )

    return RaisesContext("BinaryTransferError", check_func)


def raises_binary_upload_failed_error():
    """Equivalent to `pytest.raises` for a SiLA Binary Upload Failed Error"""
    return __raises_binary_transfer_error("BINARY_UPLOAD_FAILED")


def raises_binary_download_failed_error():
    """Equivalent to `pytest.raises` for a SiLA Binary Download Failed Error"""
    return __raises_binary_transfer_error("BINARY_DOWNLOAD_FAILED")


def raises_invalid_binary_transfer_uuid_error():
    """Equivalent to `pytest.raises` for a SiLA Invalid Binary Transfer UUID Error"""
    return __raises_binary_transfer_error("INVALID_BINARY_TRANSFER_UUID")
