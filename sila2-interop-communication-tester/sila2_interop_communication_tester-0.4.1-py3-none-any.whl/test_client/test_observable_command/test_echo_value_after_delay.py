import time
import uuid
from datetime import datetime

from sila2_interop_communication_tester.grpc_stubs.ObservableCommandTest_pb2 import EchoValueAfterDelay_Parameters
from sila2_interop_communication_tester.grpc_stubs.SiLAFramework_pb2 import (
    CommandExecutionUUID,
    ExecutionInfo,
    Integer,
    Real,
)
from sila2_interop_communication_tester.helpers.utils import string_is_uuid
from sila2_interop_communication_tester.test_client.helpers.error_handling import (
    raises_command_execution_not_finished_error,
    raises_invalid_command_execution_uuid_error,
    raises_validation_error,
)


def test_echo_value_after_delay_rejects_missing_parameters(observablecommandtest_stub):
    """
    ObservableCommandTest.EchoValueAfterDelay should fail with a Validation Error unless both parameters
    (Value and Delay) are provided
    """
    with raises_validation_error(
        "org.silastandard/test/ObservableCommandTest/v1/Command/EchoValueAfterDelay/Parameter/(Value|Delay)"
    ):
        observablecommandtest_stub.EchoValueAfterDelay(EchoValueAfterDelay_Parameters())
    with raises_validation_error(
        "org.silastandard/test/ObservableCommandTest/v1/Command/EchoValueAfterDelay/Parameter/Value"
    ):
        observablecommandtest_stub.EchoValueAfterDelay(EchoValueAfterDelay_Parameters(Delay=Real(value=5)))
    with raises_validation_error(
        "org.silastandard/test/ObservableCommandTest/v1/Command/EchoValueAfterDelay/Parameter/Delay"
    ):
        observablecommandtest_stub.EchoValueAfterDelay(EchoValueAfterDelay_Parameters(Value=Integer(value=5)))


def test_echo_value_after_delay_info_rejects_non_uuid_strings(observablecommandtest_stub):
    """
    RPC ObservableCommandTest.EchoValueAfterDelay_Info should reject non-UUID strings with a
    Invalid Command Execution UUID error
    """
    stream = observablecommandtest_stub.EchoValueAfterDelay_Info(CommandExecutionUUID(value="abcde"))
    with raises_invalid_command_execution_uuid_error():
        next(stream)


def test_echo_value_after_delay_info_rejects_unknown_uuids(observablecommandtest_stub):
    """
    RPC ObservableCommandTest.EchoValueAfterDelay_Info should reject randomly created UUIDs with an
    Invalid Command Execution UUID error
    """
    stream = observablecommandtest_stub.EchoValueAfterDelay_Info(CommandExecutionUUID(value=str(uuid.uuid4())))
    with raises_invalid_command_execution_uuid_error():
        next(stream)


def test_echo_value_after_delay_result_rejects_non_uuid_strings(observablecommandtest_stub):
    """
    RPC ObservableCommandTest.EchoValueAfterDelay_Result should reject non-UUID strings with a
    Invalid Command Execution UUID error
    """
    with raises_invalid_command_execution_uuid_error():
        observablecommandtest_stub.EchoValueAfterDelay_Result(CommandExecutionUUID(value="abcde"))


def test_echo_value_after_delay_result_rejects_unknown_uuids(observablecommandtest_stub):
    """
    RPC ObservableCommandTest.EchoValueAfterDelay_Result should reject randomly created UUIDs with an
    Invalid Command Execution UUID error
    """
    with raises_invalid_command_execution_uuid_error():
        observablecommandtest_stub.EchoValueAfterDelay_Result(CommandExecutionUUID(value=str(uuid.uuid4())))


def test_echo_value_after_delay_returns_valid_uuid(observablecommandtest_stub):
    """ObservableCommandTest.EchoValueAfterDelay should return a valid UUID string"""
    exec_info = observablecommandtest_stub.EchoValueAfterDelay(
        EchoValueAfterDelay_Parameters(Value=Integer(value=2), Delay=Real(value=0.5))
    )
    assert string_is_uuid(exec_info.commandExecutionUUID.value)


def test_echo_value_after_delay_result_raises_command_execution_not_finished(observablecommandtest_stub):
    """
    ObservableCommandTest.EchoValueAfterDelay_Result should fail with a SiLA Command Execution Not Finished Error
    if called before the requested command instance completed its execution
    """
    exec_info = observablecommandtest_stub.EchoValueAfterDelay(
        EchoValueAfterDelay_Parameters(Value=Integer(value=2), Delay=Real(value=0.5))
    )

    with raises_command_execution_not_finished_error():
        observablecommandtest_stub.EchoValueAfterDelay_Result(exec_info.commandExecutionUUID)


def test_echo_value_after_delay_info_reports_success_when_subscribing_after_command_finished(
    observablecommandtest_stub,
):
    """
    ObservableCommandTest.EchoValueAfterDelay_Info should return a `finishedSuccessfully` status when called after
    command completion
    """
    exec_info = observablecommandtest_stub.EchoValueAfterDelay(
        EchoValueAfterDelay_Parameters(Value=Integer(value=2), Delay=Real(value=1))
    )
    time.sleep(2)  # wait until command finishes

    info_stream = observablecommandtest_stub.EchoValueAfterDelay_Info(exec_info.commandExecutionUUID)
    infos = list(info_stream)
    assert infos, "Client did not receive execution information when subscribing after command finished"
    assert all(info.commandStatus == ExecutionInfo.CommandStatus.finishedSuccessfully for info in infos)


def test_echo_value_after_delay_works(observablecommandtest_stub):
    """
    ObservableCommandTest.EchoValueAfterDelay should behave as follows:
    - Execution Info should have status `waiting` until `Delay` seconds passed, it should switch to `running` and
      `finishedSuccessfull` immediately
    - Result should return `Value` after `Delay` seconds passed
    """
    start_timestamp = datetime.now()
    exec_info = observablecommandtest_stub.EchoValueAfterDelay(
        EchoValueAfterDelay_Parameters(Value=Integer(value=3), Delay=Real(value=5))
    )

    info_stream = observablecommandtest_stub.EchoValueAfterDelay_Info(exec_info.commandExecutionUUID)
    infos = list(info_stream)  # block until stream ends, collect all items

    assert 5 < (datetime.now() - start_timestamp).total_seconds() < 5.5, "Waiting for 5 seconds took much longer"
    assert (
        observablecommandtest_stub.EchoValueAfterDelay_Result(exec_info.commandExecutionUUID).ReceivedValue.value == 3
    )

    assert len(infos) >= 3, (
        "EchoValueAfterDelay_Info emitted less than 3 ExecutionInfos, "
        "expected `waiting`, `running`, and `finishedSuccessfully` at least once"
    )

    statuses = [info.commandStatus for info in infos]
    assert statuses[0] == ExecutionInfo.CommandStatus.waiting
    assert ExecutionInfo.CommandStatus.running in statuses
    assert statuses[-1] == ExecutionInfo.CommandStatus.finishedSuccessfully
