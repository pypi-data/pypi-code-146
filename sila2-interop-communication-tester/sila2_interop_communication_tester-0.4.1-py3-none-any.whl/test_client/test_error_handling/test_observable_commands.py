import time
import uuid

from sila2_interop_communication_tester.grpc_stubs import ErrorHandlingTest_pb2, SiLAFramework_pb2
from sila2_interop_communication_tester.helpers.utils import string_is_uuid
from sila2_interop_communication_tester.test_client.helpers.error_handling import (
    raises_defined_execution_error,
    raises_invalid_command_execution_uuid_error,
    raises_undefined_execution_error,
)
from sila2_interop_communication_tester.test_client.helpers.utils import collect_from_stream


def test_raise_defined_execution_error_observably_returns_valid_uuid_string(errorhandlingtest_stub):
    """ErrorHandlingTest.RaiseDefinedExecutionErrorObservably should return a valid UUID string"""
    exec_confirmation = errorhandlingtest_stub.RaiseDefinedExecutionErrorObservably(
        ErrorHandlingTest_pb2.RaiseDefinedExecutionErrorObservably_Parameters()
    )

    assert string_is_uuid(exec_confirmation.commandExecutionUUID.value)


def test_raise_undefined_execution_error_observably_returns_valid_uuid_string(errorhandlingtest_stub):
    """ErrorHandlingTest.RaiseUndefinedExecutionErrorObservably should return a valid UUID string"""
    exec_confirmation = errorhandlingtest_stub.RaiseUndefinedExecutionErrorObservably(
        ErrorHandlingTest_pb2.RaiseUndefinedExecutionErrorObservably_Parameters()
    )

    assert string_is_uuid(exec_confirmation.commandExecutionUUID.value)


def test_raise_defined_execution_error_observably_result_raises_error(errorhandlingtest_stub):
    """
    - Initiate ErrorHandlingTest.RaiseUndefinedExecutionErrorObservably
    - Wait a second
    - Request the command result
      - This should fail with the Defined Execution Error TestError and message "SiLA2_test_error_message"
    """
    exec_confirmation = errorhandlingtest_stub.RaiseDefinedExecutionErrorObservably(
        ErrorHandlingTest_pb2.RaiseDefinedExecutionErrorObservably_Parameters()
    )

    time.sleep(1)

    with raises_defined_execution_error(
        "org.silastandard/test/ErrorHandlingTest/v1/DefinedExecutionError/TestError"
    ) as error:
        errorhandlingtest_stub.RaiseDefinedExecutionErrorObservably_Result(exec_confirmation.commandExecutionUUID)
    assert error.error.message == "SiLA2_test_error_message"


def test_raise_undefined_execution_error_observably_result_raises_error(errorhandlingtest_stub):
    """
    - Initiate ErrorHandlingTest.RaiseUndefinedExecutionErrorObservably
    - Wait a second
    - Request the command result
      - This should fail with an Undefined Execution Error and message "SiLA2_test_error_message"
    """
    exec_confirmation = errorhandlingtest_stub.RaiseUndefinedExecutionErrorObservably(
        ErrorHandlingTest_pb2.RaiseUndefinedExecutionErrorObservably_Parameters()
    )

    time.sleep(1)

    with raises_undefined_execution_error() as error:
        errorhandlingtest_stub.RaiseUndefinedExecutionErrorObservably_Result(exec_confirmation.commandExecutionUUID)
    assert error.error.message == "SiLA2_test_error_message"


def test_raise_defined_execution_error_observably_info_rejects_unknown_uuids(errorhandlingtest_stub):
    """
    RPC ErrorHandlingTest.RaiseDefinedExecutionErrorObservably_Info should reject randomly created UUIDs with an
    Invalid Command Execution UUID error
    """
    info_stream = errorhandlingtest_stub.RaiseDefinedExecutionErrorObservably_Info(
        SiLAFramework_pb2.CommandExecutionUUID(value=str(uuid.uuid4()))
    )
    with raises_invalid_command_execution_uuid_error():
        next(info_stream)


def test_raise_defined_execution_error_observably_result_rejects_unknown_uuids(errorhandlingtest_stub):
    """
    RPC ErrorHandlingTest.RaiseDefinedExecutionErrorObservably_Result should reject randomly created UUIDs with an
    Invalid Command Execution UUID error
    """
    with raises_invalid_command_execution_uuid_error():
        errorhandlingtest_stub.RaiseDefinedExecutionErrorObservably_Result(
            SiLAFramework_pb2.CommandExecutionUUID(value=str(uuid.uuid4()))
        )


def test_raise_undefined_execution_error_observably_info_rejects_unknown_uuids(errorhandlingtest_stub):
    """
    RPC ErrorHandlingTest.RaiseUndefinedExecutionErrorObservably_Info should reject randomly created UUIDs with an
    Invalid Command Execution UUID error
    """
    info_stream = errorhandlingtest_stub.RaiseUndefinedExecutionErrorObservably_Info(
        SiLAFramework_pb2.CommandExecutionUUID(value=str(uuid.uuid4()))
    )
    with raises_invalid_command_execution_uuid_error():
        next(info_stream)


def test_raise_undefined_execution_error_observably_result_rejects_unknown_uuids(errorhandlingtest_stub):
    """
    RPC ErrorHandlingTest.RaiseUndefinedExecutionErrorObservably_Result should reject randomly created UUIDs with an
    Invalid Command Execution UUID error
    """
    with raises_invalid_command_execution_uuid_error():
        errorhandlingtest_stub.RaiseUndefinedExecutionErrorObservably_Result(
            SiLAFramework_pb2.CommandExecutionUUID(value=str(uuid.uuid4()))
        )


def test_raise_defined_execution_error_observably_info_reports_finished_with_error(errorhandlingtest_stub):
    """
    - Execute ErrorHandlingTest.RaiseDefinedExecutionErrorObservably
    - Subscribe to its execution information
    - collect all execution infos sent during the first second
    - assert that execution information was received
    - assert that the last received execution information has the status `finishedWithError`
    """
    exec_confirmation = errorhandlingtest_stub.RaiseDefinedExecutionErrorObservably(
        ErrorHandlingTest_pb2.RaiseDefinedExecutionErrorObservably_Parameters()
    )
    info_stream = errorhandlingtest_stub.RaiseDefinedExecutionErrorObservably_Info(
        exec_confirmation.commandExecutionUUID
    )
    exec_infos = collect_from_stream(info_stream, timeout=1)

    assert exec_infos, "Server did not send execution info for RaiseDefinedExecutionErrorObservably"
    assert exec_infos[-1].commandStatus == SiLAFramework_pb2.ExecutionInfo.CommandStatus.finishedWithError


def test_raise_undefined_execution_error_observably_info_reports_finished_with_error(errorhandlingtest_stub):
    """
    - Execute ErrorHandlingTest.RaiseUndefinedExecutionErrorObservably
    - Subscribe to its execution information
    - collect all execution infos sent during the first second
    - assert that execution information was received
    - assert that the last received execution information has the status `finishedWithError`
    """
    exec_confirmation = errorhandlingtest_stub.RaiseUndefinedExecutionErrorObservably(
        ErrorHandlingTest_pb2.RaiseUndefinedExecutionErrorObservably_Parameters()
    )
    info_stream = errorhandlingtest_stub.RaiseUndefinedExecutionErrorObservably_Info(
        exec_confirmation.commandExecutionUUID
    )
    exec_infos = collect_from_stream(info_stream, timeout=1)

    assert exec_infos, "Server did not send execution info for RaiseUndefinedExecutionErrorObservably"
    assert exec_infos[-1].commandStatus == SiLAFramework_pb2.ExecutionInfo.CommandStatus.finishedWithError


def test_raise_defined_execution_error_observably_info_rejects_invalid_uuid_strings(errorhandlingtest_stub):
    """
    RPC ErrorHandlingTest.RaiseDefinedExecutionErrorObservably_Info should reject strings that are no valid UUIDs with
    an Invalid Command Execution UUID error
    """
    stream = errorhandlingtest_stub.RaiseDefinedExecutionErrorObservably_Info(
        SiLAFramework_pb2.CommandExecutionUUID(value="abcdefg")
    )
    with raises_invalid_command_execution_uuid_error():
        next(stream)


def test_raise_undefined_execution_error_observably_info_rejects_invalid_uuid_strings(errorhandlingtest_stub):
    """
    RPC ErrorHandlingTest.RaiseUndefinedExecutionErrorObservably_Info should reject strings that are no valid UUIDs with
    an Invalid Command Execution UUID error
    """
    stream = errorhandlingtest_stub.RaiseUndefinedExecutionErrorObservably_Info(
        SiLAFramework_pb2.CommandExecutionUUID(value="abcdefg")
    )
    with raises_invalid_command_execution_uuid_error():
        next(stream)


def test_raise_defined_execution_error_observably_result_rejects_invalid_uuid_strings(errorhandlingtest_stub):
    """
    RPC ErrorHandlingTest.RaiseDefinedExecutionErrorObservably_Result should reject strings that are no valid UUIDs with
    an Invalid Command Execution UUID error
    """
    with raises_invalid_command_execution_uuid_error():
        errorhandlingtest_stub.RaiseDefinedExecutionErrorObservably_Result(
            SiLAFramework_pb2.CommandExecutionUUID(value="abcdefg")
        )


def test_raise_undefined_execution_error_observably_result_rejects_invalid_uuid_strings(errorhandlingtest_stub):
    """
    RPC ErrorHandlingTest.RaiseUndefinedExecutionErrorObservably_Result should reject strings that are no valid UUIDs
    with an Invalid Command Execution UUID error
    """
    with raises_invalid_command_execution_uuid_error():
        errorhandlingtest_stub.RaiseUndefinedExecutionErrorObservably_Result(
            SiLAFramework_pb2.CommandExecutionUUID(value="abcdefg")
        )
