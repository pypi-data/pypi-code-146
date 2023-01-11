import time
import uuid
from datetime import datetime

from sila2_interop_communication_tester.grpc_stubs.ObservableCommandTest_pb2 import Count_Parameters
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


def test_count_rejects_missing_parameters(observablecommandtest_stub):
    with raises_validation_error("org.silastandard/test/ObservableCommandTest/v1/Command/Count/Parameter/N"):
        observablecommandtest_stub.Count(Count_Parameters(Delay=Real(value=5)))
    with raises_validation_error("org.silastandard/test/ObservableCommandTest/v1/Command/Count/Parameter/Delay"):
        observablecommandtest_stub.Count(Count_Parameters(N=Integer(value=5)))


def test_count_info_rejects_non_uuid_strings(observablecommandtest_stub):
    """RPC ObservableCommandTest.Count_Info should reject non-UUID strings with a Invalid Command Execution UUID error"""
    stream = observablecommandtest_stub.Count_Info(CommandExecutionUUID(value="abcde"))
    with raises_invalid_command_execution_uuid_error():
        next(stream)


def test_count_info_rejects_unknown_uuids(observablecommandtest_stub):
    """RPC ObservableCommandTest.Count_Info should reject randomly created UUIDs with an Invalid Command Execution UUID error"""
    stream = observablecommandtest_stub.Count_Info(CommandExecutionUUID(value=str(uuid.uuid4())))
    with raises_invalid_command_execution_uuid_error():
        next(stream)


def test_count_intermediate_rejects_non_uuid_strings(observablecommandtest_stub):
    """RPC ObservableCommandTest.Count_Intermediate should reject non-UUID strings with a Command Execution Transfer UUID error"""
    stream = observablecommandtest_stub.Count_Intermediate(CommandExecutionUUID(value="abcde"))
    with raises_invalid_command_execution_uuid_error():
        next(stream)


def test_count_intermediate_rejects_unknown_uuids(observablecommandtest_stub):
    """RPC ObservableCommandTest.Count_Intermediate should reject randomly created UUIDs with an Invalid Command Execution UUID error"""
    stream = observablecommandtest_stub.Count_Intermediate(CommandExecutionUUID(value=str(uuid.uuid4())))
    with raises_invalid_command_execution_uuid_error():
        next(stream)


def test_count_result_rejects_non_uuid_strings(observablecommandtest_stub):
    """RPC ObservableCommandTest.Count_Result should reject non-UUID strings with a Invalid Command Execution UUID error"""
    with raises_invalid_command_execution_uuid_error():
        observablecommandtest_stub.Count_Result(CommandExecutionUUID(value="abcde"))


def test_count_result_rejects_unknown_uuids(observablecommandtest_stub):
    """RPC ObservableCommandTest.Count_Result should reject randomly created UUIDs with an Invalid Command Execution UUID error"""
    with raises_invalid_command_execution_uuid_error():
        observablecommandtest_stub.Count_Result(CommandExecutionUUID(value=str(uuid.uuid4())))


def test_count_returns_valid_uuid(observablecommandtest_stub):
    exec_info = observablecommandtest_stub.Count(Count_Parameters(N=Integer(value=2), Delay=Real(value=1)))
    assert string_is_uuid(exec_info.commandExecutionUUID.value)


def test_count_result_raises_command_execution_not_finished(observablecommandtest_stub):
    exec_info = observablecommandtest_stub.Count(Count_Parameters(N=Integer(value=2), Delay=Real(value=1)))

    with raises_command_execution_not_finished_error():
        observablecommandtest_stub.Count_Result(exec_info.commandExecutionUUID)


def test_count_info_reports_success_when_subscribing_after_command_finished(observablecommandtest_stub):
    exec_info = observablecommandtest_stub.Count(Count_Parameters(N=Integer(value=2), Delay=Real(value=0.5)))
    time.sleep(2)  # wait until command finishes

    info_stream = observablecommandtest_stub.Count_Info(exec_info.commandExecutionUUID)
    infos = list(info_stream)
    assert infos, "Client did not receive execution information when subscribing after command finished"
    assert all(info.commandStatus == ExecutionInfo.CommandStatus.finishedSuccessfully for info in infos)


def test_count_intermediate_works_when_subscribing_after_command_finished(
    observablecommandtest_stub,
):
    """
    - Initiate ObservableCommandTest.Count
    - Wait until it finishes
    - Subscribe to intermediate responses, request all
    - Expected behavior: no error
    """
    exec_info = observablecommandtest_stub.Count(Count_Parameters(N=Integer(value=2), Delay=Real(value=0.5)))
    time.sleep(2)  # wait until command finishes

    intermediate_stream = observablecommandtest_stub.Count_Intermediate(exec_info.commandExecutionUUID)
    list(intermediate_stream)


def test_count_works(observablecommandtest_stub):
    start_timestamp = datetime.now()
    exec_info = observablecommandtest_stub.Count(Count_Parameters(N=Integer(value=5), Delay=Real(value=1)))

    time.sleep(0.5)  # time for the server to actually start execution (status `waiting` -> `running`)
    info_stream = observablecommandtest_stub.Count_Info(exec_info.commandExecutionUUID)
    intermediate_stream = observablecommandtest_stub.Count_Intermediate(exec_info.commandExecutionUUID)
    infos = list(info_stream)  # block until stream ends, collect all items
    intermediates = list(intermediate_stream)

    assert 5 < (datetime.now() - start_timestamp).total_seconds() < 6
    assert observablecommandtest_stub.Count_Result(exec_info.commandExecutionUUID).IterationResponse.value == 4

    assert len(infos) >= 4, "Count_Info emitted less than 4 ExecutionInfos (N=5, Delay=1)"
    assert infos[0].commandStatus == ExecutionInfo.CommandStatus.running
    assert infos[-1].commandStatus == ExecutionInfo.CommandStatus.finishedSuccessfully

    # intermediate responses: server must emit [0, 1, 2, 3, 4], maybe we didn't receive the first one
    assert len(intermediates) in (4, 5), "Count_Intermediate did not emit emit 4 or 5 intermediate responses"
    assert all(intermediate.HasField("CurrentIteration") for intermediate in intermediates)
    intermediate_numbers = [i.CurrentIteration.value for i in intermediates]
    assert intermediate_numbers in ([0, 1, 2, 3, 4], [1, 2, 3, 4])
