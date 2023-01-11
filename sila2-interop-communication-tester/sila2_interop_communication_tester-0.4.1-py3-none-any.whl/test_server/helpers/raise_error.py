from base64 import standard_b64encode
from typing import NoReturn

from grpc import ServicerContext, StatusCode

from sila2_interop_communication_tester.grpc_stubs.SiLABinaryTransfer_pb2 import BinaryTransferError
from sila2_interop_communication_tester.grpc_stubs.SiLAFramework_pb2 import (
    DefinedExecutionError,
    FrameworkError,
    SiLAError,
    UndefinedExecutionError,
    ValidationError,
)


def _raise_as_rpc_error(context: ServicerContext, error_message: SiLAError) -> NoReturn:
    context.abort(StatusCode.ABORTED, details=standard_b64encode(error_message.SerializeToString()).decode("ascii"))


def raise_validation_error(context: ServicerContext, parameter_id: str, message: str) -> NoReturn:
    _raise_as_rpc_error(context, SiLAError(validationError=ValidationError(parameter=parameter_id, message=message)))


def __raise_framework_error(context: ServicerContext, error_type: FrameworkError.ErrorType, message: str) -> NoReturn:
    _raise_as_rpc_error(context, SiLAError(frameworkError=FrameworkError(errorType=error_type, message=message)))


def raise_invalid_metadata_error(context, message: str) -> NoReturn:
    __raise_framework_error(context, FrameworkError.ErrorType.INVALID_METADATA, message)


def raise_no_metadata_allowed_error(context, message: str) -> NoReturn:
    __raise_framework_error(context, FrameworkError.ErrorType.NO_METADATA_ALLOWED, message)


def raise_invalid_command_execution_uuid_error(context, message: str) -> NoReturn:
    __raise_framework_error(context, FrameworkError.ErrorType.INVALID_COMMAND_EXECUTION_UUID, message)


def raise_command_execution_not_accepted_error(context, message: str) -> NoReturn:
    __raise_framework_error(context, FrameworkError.ErrorType.COMMAND_EXECUTION_NOT_ACCEPTED, message)


def raise_command_execution_not_finished_error(context, message: str) -> NoReturn:
    __raise_framework_error(context, FrameworkError.ErrorType.COMMAND_EXECUTION_NOT_FINISHED, message)


def raise_undefined_execution_error(context: ServicerContext, message: str) -> NoReturn:
    _raise_as_rpc_error(context, SiLAError(undefinedExecutionError=UndefinedExecutionError(message=message)))


def raise_defined_execution_error(context: ServicerContext, error_id: str, message: str) -> NoReturn:
    _raise_as_rpc_error(
        context, SiLAError(definedExecutionError=DefinedExecutionError(errorIdentifier=error_id, message=message))
    )


def raise_binary_upload_failed_error(context: ServicerContext, message: str) -> NoReturn:
    _raise_as_rpc_error(
        context, BinaryTransferError(errorType=BinaryTransferError.ErrorType.BINARY_UPLOAD_FAILED, message=message)
    )


def raise_binary_download_failed_error(context: ServicerContext, message: str) -> NoReturn:
    _raise_as_rpc_error(
        context, BinaryTransferError(errorType=BinaryTransferError.ErrorType.BINARY_DOWNLOAD_FAILED, message=message)
    )


def raise_invalid_binary_transfer_uuid_error(context: ServicerContext, message: str) -> NoReturn:
    _raise_as_rpc_error(
        context,
        BinaryTransferError(errorType=BinaryTransferError.ErrorType.INVALID_BINARY_TRANSFER_UUID, message=message),
    )
