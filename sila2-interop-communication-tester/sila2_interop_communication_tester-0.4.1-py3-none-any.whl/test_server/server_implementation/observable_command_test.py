import time
import typing
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from threading import Condition, Thread

import grpc

from sila2_interop_communication_tester.grpc_stubs import ObservableCommandTest_pb2, SiLAFramework_pb2
from sila2_interop_communication_tester.grpc_stubs.ObservableCommandTest_pb2_grpc import ObservableCommandTestServicer
from sila2_interop_communication_tester.helpers.utils import string_is_uuid
from sila2_interop_communication_tester.test_server.helpers.protobuf import duration_from_seconds
from sila2_interop_communication_tester.test_server.helpers.raise_error import (
    raise_command_execution_not_finished_error,
    raise_invalid_command_execution_uuid_error,
    raise_validation_error,
)


@dataclass
class CountInstance:
    delay: float
    target_value: int
    start_timestamp: datetime = field(default_factory=datetime.now)
    condition: Condition = field(default_factory=Condition)
    current_value: int = 0

    @property
    def end_timestamp(self) -> datetime:
        return self.start_timestamp + timedelta(seconds=self.delay * (self.target_value + 1))

    @property
    def done(self) -> bool:
        return datetime.now() >= self.end_timestamp

    @property
    def status(self) -> SiLAFramework_pb2.ExecutionInfo.CommandStatus:
        if self.done:
            return SiLAFramework_pb2.ExecutionInfo.CommandStatus.finishedSuccessfully
        else:
            return SiLAFramework_pb2.ExecutionInfo.CommandStatus.running

    @property
    def progress(self) -> SiLAFramework_pb2.Real:
        return SiLAFramework_pb2.Real(value=(self.current_value / self.target_value))

    @property
    def remaining(self) -> SiLAFramework_pb2.Duration:
        raw = (self.end_timestamp - datetime.now()).total_seconds()
        return duration_from_seconds(max(raw, 0))

    @property
    def info(self) -> SiLAFramework_pb2.ExecutionInfo:
        return SiLAFramework_pb2.ExecutionInfo(
            progressInfo=self.progress, commandStatus=self.status, estimatedRemainingTime=self.remaining
        )

    @property
    def intermediate(self) -> ObservableCommandTest_pb2.Count_IntermediateResponses:
        return ObservableCommandTest_pb2.Count_IntermediateResponses(
            CurrentIteration=SiLAFramework_pb2.Integer(value=self.current_value)
        )


@dataclass
class EchoValueAfterDelayInstance:
    delay: float
    value: int
    start_timestamp: datetime = field(default_factory=datetime.now)

    @property
    def done(self) -> bool:
        return self.seconds_remaining <= 0

    @property
    def status(self) -> SiLAFramework_pb2.ExecutionInfo.CommandStatus:
        if self.done:
            return SiLAFramework_pb2.ExecutionInfo.CommandStatus.finishedSuccessfully
        else:
            return SiLAFramework_pb2.ExecutionInfo.CommandStatus.waiting

    @property
    def progress(self) -> SiLAFramework_pb2.Real:
        return SiLAFramework_pb2.Real(value=(self.seconds_remaining - self.delay))

    @property
    def seconds_remaining(self) -> float:
        raw = self.delay - (datetime.now() - self.start_timestamp).total_seconds()
        return max(raw, 0)

    @property
    def remaining(self) -> SiLAFramework_pb2.Duration:
        return duration_from_seconds(self.seconds_remaining)

    @property
    def info(self) -> SiLAFramework_pb2.ExecutionInfo:
        return SiLAFramework_pb2.ExecutionInfo(
            progressInfo=self.progress, commandStatus=self.status, estimatedRemainingTime=self.remaining
        )

    @property
    def running_info(self) -> SiLAFramework_pb2.ExecutionInfo:
        return SiLAFramework_pb2.ExecutionInfo(
            progressInfo=self.progress,
            commandStatus=SiLAFramework_pb2.ExecutionInfo.CommandStatus.running,
            estimatedRemainingTime=self.remaining,
        )


class ObservableCommandTestImpl(ObservableCommandTestServicer):
    def __init__(self):
        self.count_instances: dict[uuid.UUID, CountInstance] = {}
        self.echo_value_after_delay_instances: dict[uuid.UUID, EchoValueAfterDelayInstance] = {}

    def Count(
        self, request: ObservableCommandTest_pb2.Count_Parameters, context: grpc.ServicerContext
    ) -> SiLAFramework_pb2.CommandConfirmation:
        if not request.HasField("N"):
            raise_validation_error(
                context,
                "org.silastandard/test/ObservableCommandTest/v1/Command/Count/Parameter/N",
                "Missing parameter 'N'",
            )
        if not request.HasField("Delay"):
            raise_validation_error(
                context,
                "org.silastandard/test/ObservableCommandTest/v1/Command/Count/Parameter/Delay",
                "Missing parameter 'Delay'",
            )

        instance = CountInstance(target_value=request.N.value - 1, delay=request.Delay.value)

        def count_func():
            for i in range(instance.target_value + 1):
                instance.current_value = i
                with instance.condition:
                    instance.condition.notify_all()
                time.sleep(request.Delay.value)

        Thread(target=count_func).start()
        exec_id = uuid.uuid4()
        self.count_instances[exec_id] = instance

        return SiLAFramework_pb2.CommandConfirmation(
            commandExecutionUUID=SiLAFramework_pb2.CommandExecutionUUID(value=str(exec_id))
        )

    def Count_Info(
        self, request: SiLAFramework_pb2.CommandExecutionUUID, context: grpc.ServicerContext
    ) -> typing.Iterator[SiLAFramework_pb2.ExecutionInfo]:
        if not string_is_uuid(request.value):
            raise_invalid_command_execution_uuid_error(context, f"String is not a valid UUID: '{request.value}'")
        if uuid.UUID(request.value) not in self.count_instances:
            raise_invalid_command_execution_uuid_error(context, f"No command instance with UUID {request.value}")
        instance = self.count_instances[uuid.UUID(request.value)]

        while context.is_active() and not instance.done:
            yield instance.info
            time.sleep(0.5)
        yield instance.info

    def Count_Intermediate(
        self, request: SiLAFramework_pb2.CommandExecutionUUID, context: grpc.ServicerContext
    ) -> typing.Iterator[ObservableCommandTest_pb2.Count_IntermediateResponses]:
        if not string_is_uuid(request.value):
            raise_invalid_command_execution_uuid_error(context, f"String is not a valid UUID: '{request.value}'")
        if uuid.UUID(request.value) not in self.count_instances:
            raise_invalid_command_execution_uuid_error(context, f"No command instance with UUID {request.value}")
        instance = self.count_instances[uuid.UUID(request.value)]

        if instance.done:
            return

        yield instance.intermediate
        while context.is_active() and not instance.done:
            with instance.condition:
                if instance.condition.wait(timeout=0.1):
                    yield instance.intermediate

    def Count_Result(
        self, request: SiLAFramework_pb2.CommandExecutionUUID, context: grpc.ServicerContext
    ) -> ObservableCommandTest_pb2.Count_Responses:
        if not string_is_uuid(request.value):
            raise_invalid_command_execution_uuid_error(context, f"String is not a valid UUID: '{request.value}'")
        if uuid.UUID(request.value) not in self.count_instances:
            raise_invalid_command_execution_uuid_error(context, f"No command instance with UUID {request.value}")
        instance = self.count_instances[uuid.UUID(request.value)]

        if not instance.done:
            raise_command_execution_not_finished_error(context, "Command is still running")
        return ObservableCommandTest_pb2.Count_Responses(
            IterationResponse=SiLAFramework_pb2.Integer(value=instance.target_value)
        )

    def EchoValueAfterDelay(
        self, request: ObservableCommandTest_pb2.EchoValueAfterDelay_Parameters, context: grpc.ServicerContext
    ) -> SiLAFramework_pb2.CommandConfirmation:
        if not request.HasField("Value"):
            raise_validation_error(
                context,
                "org.silastandard/test/ObservableCommandTest/v1/Command/EchoValueAfterDelay/Parameter/Value",
                "Missing parameter 'N'",
            )
        if not request.HasField("Delay"):
            raise_validation_error(
                context,
                "org.silastandard/test/ObservableCommandTest/v1/Command/EchoValueAfterDelay/Parameter/Delay",
                "Missing parameter 'Delay'",
            )

        instance = EchoValueAfterDelayInstance(value=request.Value.value, delay=request.Delay.value)
        exec_id = uuid.uuid4()
        self.echo_value_after_delay_instances[exec_id] = instance

        return SiLAFramework_pb2.CommandConfirmation(
            commandExecutionUUID=SiLAFramework_pb2.CommandExecutionUUID(value=str(exec_id))
        )

    def EchoValueAfterDelay_Info(
        self, request: SiLAFramework_pb2.CommandExecutionUUID, context: grpc.ServicerContext
    ) -> typing.Iterator[SiLAFramework_pb2.ExecutionInfo]:
        if not string_is_uuid(request.value):
            raise_invalid_command_execution_uuid_error(context, f"String is not a valid UUID: '{request.value}'")
        if uuid.UUID(request.value) not in self.echo_value_after_delay_instances:
            raise_invalid_command_execution_uuid_error(context, f"No command instance with UUID {request.value}")
        instance = self.echo_value_after_delay_instances[uuid.UUID(request.value)]

        if instance.done:
            yield instance.info
            return

        while not instance.done:
            yield instance.info
            time.sleep(1)
        yield instance.running_info
        yield instance.info

    def EchoValueAfterDelay_Result(
        self, request: SiLAFramework_pb2.CommandExecutionUUID, context: grpc.ServicerContext
    ) -> ObservableCommandTest_pb2.EchoValueAfterDelay_Responses:
        if not string_is_uuid(request.value):
            raise_invalid_command_execution_uuid_error(context, f"String is not a valid UUID: '{request.value}'")
        if uuid.UUID(request.value) not in self.echo_value_after_delay_instances:
            raise_invalid_command_execution_uuid_error(context, f"No command instance with UUID {request.value}")
        instance = self.echo_value_after_delay_instances[uuid.UUID(request.value)]

        if not instance.done:
            raise_command_execution_not_finished_error(context, "Command is still running")
        return ObservableCommandTest_pb2.EchoValueAfterDelay_Responses(
            ReceivedValue=SiLAFramework_pb2.Integer(value=instance.value)
        )
