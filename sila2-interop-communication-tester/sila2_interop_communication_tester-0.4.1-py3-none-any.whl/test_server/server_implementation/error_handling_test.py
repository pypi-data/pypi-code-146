import typing
import uuid
from collections import defaultdict

import grpc

from sila2_interop_communication_tester.grpc_stubs import ErrorHandlingTest_pb2, SiLAFramework_pb2
from sila2_interop_communication_tester.grpc_stubs.ErrorHandlingTest_pb2_grpc import ErrorHandlingTestServicer
from sila2_interop_communication_tester.helpers.utils import string_is_uuid
from sila2_interop_communication_tester.test_server.helpers.raise_error import (
    raise_defined_execution_error,
    raise_invalid_command_execution_uuid_error,
    raise_undefined_execution_error,
)


class ErrorHandlingTestImpl(ErrorHandlingTestServicer):
    def __init__(self):
        # command identifier -> set of existing command execution uuids
        self.valid_uuids: dict[str, set[uuid.UUID]] = defaultdict(set)

    def RaiseDefinedExecutionError(
        self, request: ErrorHandlingTest_pb2.RaiseDefinedExecutionError_Parameters, context: grpc.ServicerContext
    ) -> ErrorHandlingTest_pb2.RaiseDefinedExecutionError_Responses:
        raise_defined_execution_error(
            context,
            "org.silastandard/test/ErrorHandlingTest/v1/DefinedExecutionError/TestError",
            "SiLA2_test_error_message",
        )

    def RaiseDefinedExecutionErrorObservably(
        self,
        request: ErrorHandlingTest_pb2.RaiseDefinedExecutionErrorObservably_Parameters,
        context: grpc.ServicerContext,
    ) -> SiLAFramework_pb2.CommandConfirmation:
        execution_id = uuid.uuid4()
        self.valid_uuids["RaiseDefinedExecutionErrorObservably"].add(execution_id)
        # NOTE: not sending a lifetime -> uuid is valid until end of server lifetime
        return SiLAFramework_pb2.CommandConfirmation(
            commandExecutionUUID=SiLAFramework_pb2.CommandExecutionUUID(value=str(execution_id))
        )

    def RaiseDefinedExecutionErrorObservably_Info(
        self, request: SiLAFramework_pb2.CommandExecutionUUID, context: grpc.ServicerContext
    ) -> typing.Iterator[SiLAFramework_pb2.ExecutionInfo]:
        if not string_is_uuid(request.value):
            raise_invalid_command_execution_uuid_error(context, f"String is not a valid UUID: '{request.value}'")
        if uuid.UUID(request.value) not in self.valid_uuids["RaiseDefinedExecutionErrorObservably"]:
            raise_invalid_command_execution_uuid_error(context, f"No command instance with UUID {request.value}")
        yield SiLAFramework_pb2.ExecutionInfo(
            commandStatus=SiLAFramework_pb2.ExecutionInfo.CommandStatus.finishedWithError
        )

    def RaiseDefinedExecutionErrorObservably_Result(
        self, request: SiLAFramework_pb2.CommandExecutionUUID, context: grpc.ServicerContext
    ) -> ErrorHandlingTest_pb2.RaiseDefinedExecutionErrorObservably_Responses:
        if not string_is_uuid(request.value):
            raise_invalid_command_execution_uuid_error(context, f"String is not a valid UUID: '{request.value}'")
        if uuid.UUID(request.value) not in self.valid_uuids["RaiseDefinedExecutionErrorObservably"]:
            raise_invalid_command_execution_uuid_error(context, f"No command instance with UUID {request.value}")
        raise_defined_execution_error(
            context,
            "org.silastandard/test/ErrorHandlingTest/v1/DefinedExecutionError/TestError",
            "SiLA2_test_error_message",
        )

    def RaiseUndefinedExecutionError(
        self, request: ErrorHandlingTest_pb2.RaiseUndefinedExecutionError_Parameters, context: grpc.ServicerContext
    ) -> ErrorHandlingTest_pb2.RaiseUndefinedExecutionError_Responses:
        raise_undefined_execution_error(context, "SiLA2_test_error_message")

    def RaiseUndefinedExecutionErrorObservably(
        self,
        request: ErrorHandlingTest_pb2.RaiseUndefinedExecutionErrorObservably_Parameters,
        context: grpc.ServicerContext,
    ) -> SiLAFramework_pb2.CommandConfirmation:
        execution_id = uuid.uuid4()
        self.valid_uuids["RaiseUndefinedExecutionErrorObservably"].add(execution_id)
        # NOTE: not sending a lifetime -> uuid is valid until end of server lifetime
        return SiLAFramework_pb2.CommandConfirmation(
            commandExecutionUUID=SiLAFramework_pb2.CommandExecutionUUID(value=str(execution_id))
        )

    def RaiseUndefinedExecutionErrorObservably_Info(
        self, request: SiLAFramework_pb2.CommandExecutionUUID, context: grpc.ServicerContext
    ) -> typing.Iterator[SiLAFramework_pb2.ExecutionInfo]:
        if not string_is_uuid(request.value):
            raise_invalid_command_execution_uuid_error(context, f"String is not a valid UUID: '{request.value}'")
        if uuid.UUID(request.value) not in self.valid_uuids["RaiseUndefinedExecutionErrorObservably"]:
            raise_invalid_command_execution_uuid_error(context, f"No command instance with UUID {request.value}")
        yield SiLAFramework_pb2.ExecutionInfo(
            commandStatus=SiLAFramework_pb2.ExecutionInfo.CommandStatus.finishedWithError
        )

    def RaiseUndefinedExecutionErrorObservably_Result(
        self, request: SiLAFramework_pb2.CommandExecutionUUID, context: grpc.ServicerContext
    ) -> ErrorHandlingTest_pb2.RaiseUndefinedExecutionErrorObservably_Responses:
        if not string_is_uuid(request.value):
            raise_invalid_command_execution_uuid_error(context, f"String is not a valid UUID: '{request.value}'")
        if uuid.UUID(request.value) not in self.valid_uuids["RaiseUndefinedExecutionErrorObservably"]:
            raise_invalid_command_execution_uuid_error(context, f"No command instance with UUID {request.value}")
        raise_undefined_execution_error(
            context,
            "SiLA2_test_error_message",
        )

    def Get_RaiseDefinedExecutionErrorOnGet(
        self,
        request: ErrorHandlingTest_pb2.Get_RaiseDefinedExecutionErrorOnGet_Parameters,
        context: grpc.ServicerContext,
    ) -> ErrorHandlingTest_pb2.Get_RaiseDefinedExecutionErrorOnGet_Responses:
        raise_defined_execution_error(
            context,
            "org.silastandard/test/ErrorHandlingTest/v1/DefinedExecutionError/TestError",
            "SiLA2_test_error_message",
        )

    def Subscribe_RaiseDefinedExecutionErrorOnSubscribe(
        self,
        request: ErrorHandlingTest_pb2.Subscribe_RaiseDefinedExecutionErrorOnSubscribe_Parameters,
        context: grpc.ServicerContext,
    ) -> typing.Iterator[ErrorHandlingTest_pb2.Subscribe_RaiseDefinedExecutionErrorOnSubscribe_Responses]:
        raise_defined_execution_error(
            context,
            "org.silastandard/test/ErrorHandlingTest/v1/DefinedExecutionError/TestError",
            "SiLA2_test_error_message",
        )

    def Get_RaiseUndefinedExecutionErrorOnGet(
        self,
        request: ErrorHandlingTest_pb2.Get_RaiseUndefinedExecutionErrorOnGet_Parameters,
        context: grpc.ServicerContext,
    ) -> ErrorHandlingTest_pb2.Get_RaiseUndefinedExecutionErrorOnGet_Responses:
        raise_undefined_execution_error(context, "SiLA2_test_error_message")

    def Subscribe_RaiseUndefinedExecutionErrorOnSubscribe(
        self,
        request: ErrorHandlingTest_pb2.Subscribe_RaiseUndefinedExecutionErrorOnSubscribe_Parameters,
        context: grpc.ServicerContext,
    ) -> typing.Iterator[ErrorHandlingTest_pb2.Subscribe_RaiseUndefinedExecutionErrorOnSubscribe_Responses]:
        raise_undefined_execution_error(context, "SiLA2_test_error_message")

    def Subscribe_RaiseDefinedExecutionErrorAfterValueWasSent(
        self,
        request: ErrorHandlingTest_pb2.Subscribe_RaiseDefinedExecutionErrorAfterValueWasSent_Parameters,
        context: grpc.ServicerContext,
    ) -> typing.Iterator[ErrorHandlingTest_pb2.Subscribe_RaiseDefinedExecutionErrorAfterValueWasSent_Responses]:
        yield ErrorHandlingTest_pb2.Subscribe_RaiseDefinedExecutionErrorAfterValueWasSent_Responses(
            RaiseDefinedExecutionErrorAfterValueWasSent=SiLAFramework_pb2.Integer(value=1)
        )
        raise_defined_execution_error(
            context,
            "org.silastandard/test/ErrorHandlingTest/v1/DefinedExecutionError/TestError",
            "SiLA2_test_error_message",
        )

    def Subscribe_RaiseUndefinedExecutionErrorAfterValueWasSent(
        self,
        request: ErrorHandlingTest_pb2.Subscribe_RaiseUndefinedExecutionErrorAfterValueWasSent_Parameters,
        context: grpc.ServicerContext,
    ) -> typing.Iterator[ErrorHandlingTest_pb2.Subscribe_RaiseUndefinedExecutionErrorAfterValueWasSent_Responses]:
        yield ErrorHandlingTest_pb2.Subscribe_RaiseUndefinedExecutionErrorAfterValueWasSent_Responses(
            RaiseUndefinedExecutionErrorAfterValueWasSent=SiLAFramework_pb2.Integer(value=1)
        )
        raise_undefined_execution_error(context, "SiLA2_test_error_message")
