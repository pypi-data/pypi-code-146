import time
import typing
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from functools import cached_property
from threading import Condition, Thread

import grpc

from sila2_interop_communication_tester.grpc_stubs import SiLAFramework_pb2
from sila2_interop_communication_tester.grpc_stubs.BinaryTransferTest_pb2 import (
    EchoBinariesObservably_IntermediateResponses,
    EchoBinariesObservably_Parameters,
    EchoBinariesObservably_Responses,
    EchoBinaryAndMetadataString_Parameters,
    EchoBinaryAndMetadataString_Responses,
    EchoBinaryValue_Parameters,
    EchoBinaryValue_Responses,
    Get_BinaryValueDirectly_Parameters,
    Get_BinaryValueDirectly_Responses,
    Get_BinaryValueDownload_Parameters,
    Get_BinaryValueDownload_Responses,
    Get_FCPAffectedByMetadata_String_Parameters,
    Get_FCPAffectedByMetadata_String_Responses,
    Metadata_String,
)
from sila2_interop_communication_tester.grpc_stubs.BinaryTransferTest_pb2_grpc import BinaryTransferTestServicer
from sila2_interop_communication_tester.helpers.utils import string_is_uuid
from sila2_interop_communication_tester.test_server.helpers.binary_transfer import get_binary, pack_binary
from sila2_interop_communication_tester.test_server.helpers.protobuf import duration_from_seconds
from sila2_interop_communication_tester.test_server.helpers.raise_error import (
    raise_command_execution_not_finished_error,
    raise_invalid_command_execution_uuid_error,
    raise_invalid_metadata_error,
    raise_validation_error,
)
from sila2_interop_communication_tester.test_server.helpers.spy import extract_metadata


@dataclass
class EchoBinariesObservablyInstance:
    parameters: list[bytes]
    start_timestamp: datetime = field(default_factory=datetime.now)
    current_index: int = 0
    condition: Condition = field(default_factory=Condition)

    @cached_property
    def end_timestamp(self) -> datetime:
        return self.start_timestamp + timedelta(seconds=len(self.parameters))

    @property
    def done(self) -> bool:
        return datetime.now() >= self.end_timestamp

    @property
    def intermediate(self) -> EchoBinariesObservably_IntermediateResponses:
        return EchoBinariesObservably_IntermediateResponses(Binary=pack_binary(self.parameters[self.current_index]))

    @property
    def status(self) -> SiLAFramework_pb2.ExecutionInfo.CommandStatus:
        if self.done:
            return SiLAFramework_pb2.ExecutionInfo.CommandStatus.finishedSuccessfully
        else:
            return SiLAFramework_pb2.ExecutionInfo.CommandStatus.running

    @cached_property
    def total_seconds(self) -> float:
        return (self.end_timestamp - self.start_timestamp).total_seconds()

    @property
    def remaining(self) -> float:
        raw = (self.end_timestamp - datetime.now()).total_seconds()
        return max(raw, 0)

    @property
    def progress(self) -> float:
        return (self.total_seconds - self.remaining) / self.total_seconds

    @property
    def info(self) -> SiLAFramework_pb2.ExecutionInfo:
        return SiLAFramework_pb2.ExecutionInfo(
            progressInfo=SiLAFramework_pb2.Real(value=self.progress),
            commandStatus=self.status,
            estimatedRemainingTime=duration_from_seconds(self.remaining),
        )


class BinaryTransferTestImpl(BinaryTransferTestServicer):
    def __init__(self):
        self.echo_binaries_observably_instances: dict[uuid.UUID, EchoBinariesObservablyInstance] = {}

    def EchoBinaryValue(
        self, request: EchoBinaryValue_Parameters, context: grpc.ServicerContext
    ) -> EchoBinaryValue_Responses:
        if not request.HasField("BinaryValue"):
            raise_validation_error(
                context,
                "org.silastandard/test/BinaryTransferTest/v1/Command/EchoBinaryValue/Parameter/BinaryValue",
                "Missing parameter 'BinaryValue'",
            )

        binary = get_binary(
            request.BinaryValue,
            "org.silastandard/test/BinaryTransferTest/v1/Command/EchoBinaryValue/Parameter/BinaryValue",
            context,
        )

        return EchoBinaryValue_Responses(ReceivedValue=pack_binary(binary))

    def EchoBinariesObservably(
        self, request: EchoBinariesObservably_Parameters, context: grpc.ServicerContext
    ) -> SiLAFramework_pb2.CommandConfirmation:
        binaries = []
        for item in request.Binaries:
            binaries.append(
                get_binary(
                    item,
                    "org.silastandard/test/BinaryTransferTest/v1/Command/EchoBinariesObservably/Parameter/Binaries",
                    context,
                )
            )

        instance = EchoBinariesObservablyInstance(binaries)

        def func():
            time.sleep(1)
            for _ in binaries:
                instance.current_index += 1
                with instance.condition:
                    instance.condition.notify_all()
                time.sleep(1)

        Thread(target=func).start()
        exec_id = uuid.uuid4()
        self.echo_binaries_observably_instances[exec_id] = instance

        return SiLAFramework_pb2.CommandConfirmation(
            commandExecutionUUID=SiLAFramework_pb2.CommandExecutionUUID(value=str(exec_id))
        )

    def EchoBinariesObservably_Info(
        self, request: SiLAFramework_pb2.CommandExecutionUUID, context: grpc.ServicerContext
    ) -> typing.Iterator[SiLAFramework_pb2.ExecutionInfo]:
        if not string_is_uuid(request.value):
            raise_invalid_command_execution_uuid_error(context, f"String is not a valid UUID: '{request.value}'")
        if uuid.UUID(request.value) not in self.echo_binaries_observably_instances:
            raise_invalid_command_execution_uuid_error(context, f"No command instance with UUID {request.value}")
        instance = self.echo_binaries_observably_instances[uuid.UUID(request.value)]

        if instance.done:
            yield instance.info
            return

        while context.is_active() and not instance.done:
            yield instance.info
            time.sleep(0.5)
        yield instance.info

    def EchoBinariesObservably_Intermediate(
        self, request: SiLAFramework_pb2.CommandExecutionUUID, context: grpc.ServicerContext
    ) -> typing.Iterator[EchoBinariesObservably_IntermediateResponses]:
        if not string_is_uuid(request.value):
            raise_invalid_command_execution_uuid_error(context, f"String is not a valid UUID: '{request.value}'")
        if uuid.UUID(request.value) not in self.echo_binaries_observably_instances:
            raise_invalid_command_execution_uuid_error(context, f"No command instance with UUID {request.value}")
        instance = self.echo_binaries_observably_instances[uuid.UUID(request.value)]

        if instance.done:
            return

        yield instance.intermediate
        while context.is_active() and not instance.done:
            with instance.condition:
                if instance.condition.wait(timeout=0.1):
                    yield instance.intermediate

    def EchoBinariesObservably_Result(
        self, request: SiLAFramework_pb2.CommandExecutionUUID, context: grpc.ServicerContext
    ) -> EchoBinariesObservably_Responses:
        if not string_is_uuid(request.value):
            raise_invalid_command_execution_uuid_error(context, f"String is not a valid UUID: '{request.value}'")
        if uuid.UUID(request.value) not in self.echo_binaries_observably_instances:
            raise_invalid_command_execution_uuid_error(context, f"No command instance with UUID {request.value}")
        instance = self.echo_binaries_observably_instances[uuid.UUID(request.value)]

        if not instance.done:
            raise_command_execution_not_finished_error(context, "Command is still running")
        return EchoBinariesObservably_Responses(JointBinary=pack_binary(b"".join(instance.parameters)))

    def Get_BinaryValueDirectly(
        self, request: Get_BinaryValueDirectly_Parameters, context: grpc.ServicerContext
    ) -> Get_BinaryValueDirectly_Responses:
        return Get_BinaryValueDirectly_Responses(
            BinaryValueDirectly=SiLAFramework_pb2.Binary(value="SiLA2_Test_String_Value".encode("UTF-8"))
        )

    def Get_BinaryValueDownload(
        self, request: Get_BinaryValueDownload_Parameters, context: grpc.ServicerContext
    ) -> Get_BinaryValueDownload_Responses:
        return Get_BinaryValueDownload_Responses(
            BinaryValueDownload=pack_binary(
                "A_slightly_longer_SiLA2_Test_String_Value_used_to_demonstrate_the_binary_download".encode("UTF-8")
                * 100_000
            )
        )

    def EchoBinaryAndMetadataString(
        self, request: EchoBinaryAndMetadataString_Parameters, context: grpc.ServicerContext
    ) -> EchoBinaryAndMetadataString_Responses:
        # read metadata
        try:
            metadata = extract_metadata(context)
        except BaseException as ex:
            raise_invalid_metadata_error(context, f"Failed to parse received metadata: {ex!r}")

        try:
            string_metadata = metadata[Metadata_String]
        except KeyError:
            raise_invalid_metadata_error(
                context,
                "Missing metadata, expected 'org.silastandard/test/BinaryTransferTest/v1/Metadata/String'",
            )

        # read parameter
        if not request.HasField("Binary"):
            raise_validation_error(
                context,
                "org.silastandard/test/BinaryTransferTest/v1/Command/EchoBinaryAndMetadataString/Parameter/Binary",
                "Missing parameter 'Binary'",
            )

        binary = get_binary(
            request.Binary,
            "org.silastandard/test/BinaryTransferTest/v1/Command/EchoBinaryAndMetadataString/Parameter/Binary",
            context,
        )

        # return response
        return EchoBinaryAndMetadataString_Responses(
            Binary=pack_binary(binary), StringMetadata=SiLAFramework_pb2.String(value=string_metadata.String.value)
        )

    def Get_FCPAffectedByMetadata_String(
        self, request: Get_FCPAffectedByMetadata_String_Parameters, context: grpc.ServicerContext
    ) -> Get_FCPAffectedByMetadata_String_Responses:
        return Get_FCPAffectedByMetadata_String_Responses(
            AffectedCalls=[
                SiLAFramework_pb2.String(
                    value="org.silastandard/test/BinaryTransferTest/v1/Command/EchoBinaryAndMetadataString"
                )
            ]
        )
