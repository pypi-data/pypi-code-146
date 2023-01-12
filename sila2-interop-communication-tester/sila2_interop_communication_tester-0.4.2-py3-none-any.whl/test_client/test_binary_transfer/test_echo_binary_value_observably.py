import time
import uuid
from datetime import datetime

from sila2_interop_communication_tester.grpc_stubs.BinaryTransferTest_pb2 import EchoBinariesObservably_Parameters
from sila2_interop_communication_tester.grpc_stubs.SiLAFramework_pb2 import Binary, CommandExecutionUUID, ExecutionInfo
from sila2_interop_communication_tester.helpers.utils import string_is_uuid
from sila2_interop_communication_tester.test_client.helpers.binary_transfer import download_binary, upload_binary
from sila2_interop_communication_tester.test_client.helpers.error_handling import (
    raises_command_execution_not_finished_error,
    raises_invalid_command_execution_uuid_error,
    raises_validation_error,
)


def test_echo_binary_value_observably_rejects_empty_binary_message(
    binarytransfertest_stub,
):
    """
    BinaryTransferTest.EchoBinariesObservably should reject empty Binary messages with a Validation Error
    """
    with raises_validation_error(
        "org.silastandard/test/BinaryTransferTest/v1/Command/EchoBinariesObservably/Parameter/Binaries"
    ):
        binarytransfertest_stub.EchoBinariesObservably(EchoBinariesObservably_Parameters(Binaries=[Binary()]))


def test_echo_binary_value_observably_rejects_invalid_binary_uuid_strings(
    binarytransfertest_stub,
):
    """
    BinaryTransferTest.EchoBinariesObservably should reject Binary messages containing a `binaryTransferUUID` value that
    is not a valid UUID string with a Validation Error
    """
    with raises_validation_error(
        "org.silastandard/test/BinaryTransferTest/v1/Command/EchoBinariesObservably/Parameter/Binaries"
    ):
        binarytransfertest_stub.EchoBinariesObservably(
            EchoBinariesObservably_Parameters(Binaries=[Binary(binaryTransferUUID="abc")])
        )


def test_echo_binaries_observably_rejects_unknown_binary_uuids(binarytransfertest_stub):
    """
    BinaryTransferTest.EchoBinariesObservably should reject Binary messages containing a `binaryTransferUUID` that is
    randomly generated with a Validation Error
    """
    with raises_validation_error(
        "org.silastandard/test/BinaryTransferTest/v1/Command/EchoBinariesObservably/Parameter/Binaries"
    ):
        binarytransfertest_stub.EchoBinariesObservably(
            EchoBinariesObservably_Parameters(Binaries=[Binary(binaryTransferUUID=str(uuid.uuid4()))])
        )


def test_echo_binaries_observably_info_rejects_empty_parameter(binarytransfertest_stub):
    """
    BinaryTransferTest.EchoBinariesObservably_Info should reject empty CommandExecutionUUID messages with a
    Validation Error
    """
    info_stream = binarytransfertest_stub.EchoBinariesObservably_Info(CommandExecutionUUID())
    with raises_invalid_command_execution_uuid_error():
        next(info_stream)


def test_echo_binaries_observably_info_rejects_non_uuid_strings(
    binarytransfertest_stub,
):
    """
    BinaryTransferTest.EchoBinariesObservably_Info should reject CommandExecutionUUID messages containing non-UUID
    strings with a Invalid Command Execution UUID error
    """
    info_stream = binarytransfertest_stub.EchoBinariesObservably_Info(CommandExecutionUUID(value="abc"))
    with raises_invalid_command_execution_uuid_error():
        next(info_stream)


def test_echo_binaries_observably_info_rejects_unknown_uuids(binarytransfertest_stub):
    """
    RPC BinaryTransferTest.EchoBinariesObservably_Info should reject randomly created UUIDs with an Invalid Command
    Execution UUID error
    """
    info_stream = binarytransfertest_stub.EchoBinariesObservably_Info(CommandExecutionUUID(value=str(uuid.uuid4())))
    with raises_invalid_command_execution_uuid_error():
        next(info_stream)


def test_echo_binaries_observably_intermediate_rejects_empty_parameter(
    binarytransfertest_stub,
):
    """
    BinaryTransferTest.EchoBinariesObservably_Intermediate should reject empty CommandExecutionUUID messages with a
    Validation Error
    """
    intermediate_stream = binarytransfertest_stub.EchoBinariesObservably_Intermediate(CommandExecutionUUID())
    with raises_invalid_command_execution_uuid_error():
        next(intermediate_stream)


def test_echo_binaries_observably_intermediate_rejects_non_uuid_strings(
    binarytransfertest_stub,
):
    """
    RPC BinaryTransferTest.EchoBinariesObservably_Intermediate should reject non-UUID strings with a Invalid
    Command Execution UUID error
    """
    intermediate_stream = binarytransfertest_stub.EchoBinariesObservably_Intermediate(CommandExecutionUUID(value="abc"))
    with raises_invalid_command_execution_uuid_error():
        next(intermediate_stream)


def test_echo_binaries_observably_intermediate_rejects_unknown_uuids(
    binarytransfertest_stub,
):
    """
    RPC BinaryTransferTest.EchoBinariesObservably_Intermediate should reject randomly created UUIDs with an
    Invalid Command Execution UUID error
    """
    intermediate_stream = binarytransfertest_stub.EchoBinariesObservably_Intermediate(
        CommandExecutionUUID(value=str(uuid.uuid4()))
    )
    with raises_invalid_command_execution_uuid_error():
        next(intermediate_stream)


def test_echo_binaries_observably_result_rejects_empty_parameter(
    binarytransfertest_stub,
):
    """
    BinaryTransferTest.EchoBinariesObservably_Result should reject empty CommandExecutionUUID messages with a
    Validation Error
    """
    with raises_invalid_command_execution_uuid_error():
        binarytransfertest_stub.EchoBinariesObservably_Result(CommandExecutionUUID())


def test_echo_binaries_observably_result_rejects_non_uuid_strings(
    binarytransfertest_stub,
):
    """
    RPC BinaryTransferTest.EchoBinariesObservably_Result should reject non-UUID strings with a Invalid Command Execution
    UUID error
    """
    with raises_invalid_command_execution_uuid_error():
        binarytransfertest_stub.EchoBinariesObservably_Result(CommandExecutionUUID(value="abc"))


def test_echo_binaries_observably_result_rejects_unknown_uuids(binarytransfertest_stub):
    """
    RPC BinaryTransferTest.EchoBinariesObservably_Result should reject randomly created UUIDs with an Invalid Command
    Execution UUID error
    """
    with raises_invalid_command_execution_uuid_error():
        binarytransfertest_stub.EchoBinariesObservably_Result(CommandExecutionUUID(value=str(uuid.uuid4())))


def test_echo_binaries_observably_returns_valid_uuid_string(binarytransfertest_stub):
    """RPC BinaryTransferTest.EchoBinariesObservably should return a valid UUID string as command execution UUID"""
    info = binarytransfertest_stub.EchoBinariesObservably(
        EchoBinariesObservably_Parameters(Binaries=[Binary(value=b"abc"), Binary(value=b"def")])
    )
    assert string_is_uuid(info.commandExecutionUUID.value)


def test_echo_binaries_observably_result_throws_if_not_finished(
    binarytransfertest_stub,
):
    """
    - Start BinaryTransferTest.EchoBinariesObservably
    - Call BinaryTransferTest.EchoBinariesObservably_Result with the received command execution UUID without waiting
        for the command to finish
        - Should fail with a Command Execution Not Finished error
    """
    info = binarytransfertest_stub.EchoBinariesObservably(
        EchoBinariesObservably_Parameters(Binaries=[Binary(value=b"abc"), Binary(value=b"def")])
    )

    with raises_command_execution_not_finished_error():
        binarytransfertest_stub.EchoBinariesObservably_Result(info.commandExecutionUUID)


def test_echo_binaries_observably_info_works_after_command_finished(
    binarytransfertest_stub,
):
    """
    - Start BinaryTransferTest.EchoBinariesObservably with one binary parameter
    - Wait for two seconds (command should be finished afterwards)
    - Call BinaryTransferTest.EchoBinariesObservably_Info and read all received responses until the server
        finished the stream
    - Assert that at least one response was received
    - Assert that all received responses have the status `finishedSuccessfully`
    """
    info = binarytransfertest_stub.EchoBinariesObservably(
        EchoBinariesObservably_Parameters(Binaries=[Binary(value=b"def")])
    )
    time.sleep(2)
    info_stream = binarytransfertest_stub.EchoBinariesObservably_Info(info.commandExecutionUUID)
    infos = list(info_stream)
    assert infos, "EchoBinariesObservably_Info did not send any responses when subscribing after command finished"
    assert all(
        info.commandStatus == ExecutionInfo.CommandStatus.finishedSuccessfully for info in infos
    ), "EchoBinariesObservably_Info reported other status than finishedSuccessfully after command finished"


def test_echo_binaries_observably_intermediate_works_after_command_finished(
    binarytransfertest_stub,
):
    """
    - Start BinaryTransferTest.EchoBinariesObservably with one binary parameter
    - Wait for two seconds (command should be finished afterwards)
    - Call BinaryTransferTest.EchoBinariesObservably_Intermediate and read all received responses until the server
        finished the stream
    - Assert that at most one response was received (none: server does not cache intermediate responses,
        one: server caches intermediate responses)
    """
    info = binarytransfertest_stub.EchoBinariesObservably(
        EchoBinariesObservably_Parameters(Binaries=[Binary(value=b"def")])
    )
    time.sleep(2)
    intermediate_stream = binarytransfertest_stub.EchoBinariesObservably_Intermediate(info.commandExecutionUUID)
    list(intermediate_stream)
    # test is successful if the call is not rejected


def test_echo_binaries_observably_works(binarytransfertest_stub, binary_upload_stub, binary_download_stub):
    """
    Setup:
    - Upload a large binary for the parameter 'Binaries' of BinaryTransferTest.EchoBinariesObservably
    - Start BinaryTransferTest.EchoBinariesObservably with two small one the large binary parameters
    - Call BinaryTransferTest.EchoBinariesObservably_Intermediate to subscribe to all intermediate responses
    - Call BinaryTransferTest.EchoBinariesObservably_Info to subscribe to all execution infos
    - Wait until the server finishes both streams
    - Request the result

    Tests:
    - Assert that this took between 2 and 5 seconds
    - Assert that the result is equal to the concatenation of the three parameter binaries
    - Assert that the intermediate responses are equal to the three parameter binaries
    - Assert that at least two execution infos were received
    - Assert that the first execution info has the status `waiting` or `running`
    - Assert that the last execution info has the status `finishedSuccessfully`
    """
    # upload parameter
    large_binary_id = upload_binary(
        binary_upload_stub,
        b"abc" * 1_000_000,
        "org.silastandard/test/BinaryTransferTest/v1/Command/EchoBinariesObservably/Parameter/Binaries",
    )

    # initialize command
    start_timestamp = datetime.now()
    info = binarytransfertest_stub.EchoBinariesObservably(
        EchoBinariesObservably_Parameters(
            Binaries=[
                Binary(value=b"abc"),
                Binary(binaryTransferUUID=str(large_binary_id)),
                Binary(value=b"SiLA2_Test_String_Value"),
            ]
        )
    )

    # subscribe to streams
    info_stream = binarytransfertest_stub.EchoBinariesObservably_Info(info.commandExecutionUUID)
    intermediate_stream = binarytransfertest_stub.EchoBinariesObservably_Intermediate(info.commandExecutionUUID)

    # stream consumption blocks until stream ends
    infos = list(info_stream)
    intermediates = list(intermediate_stream)
    end_timestamp = datetime.now()

    assert (
        2 < (end_timestamp - start_timestamp).total_seconds() < 5
    ), "EchoBinariesObservably with 3 parameters took <2 or >5 seconds"

    # check result
    result_message = binarytransfertest_stub.EchoBinariesObservably_Result(info.commandExecutionUUID)
    result_binary = download_binary(binary_download_stub, uuid.UUID(result_message.JointBinary.binaryTransferUUID))
    assert result_binary == b"abc" * 1_000_001 + b"SiLA2_Test_String_Value"

    # check infos
    assert len(infos) >= 2, "EchoBinariesObservably did not yield at least two execution infos"
    assert infos[-1].commandStatus == ExecutionInfo.CommandStatus.finishedSuccessfully
    assert infos[0].commandStatus in (ExecutionInfo.CommandStatus.waiting, ExecutionInfo.CommandStatus.running)

    # check intermediates
    assert len(intermediates) == 3, (
        f"EchoBinariesObservably with 3 parameters yielded {len(intermediates)} intermediate responses "
        f"when subscription started immediately after command initiation. Expected 3."
    )
    assert intermediates[0].Binary.value == b"abc", "First intermediate response was not 'abc'"
    assert intermediates[1].Binary.binaryTransferUUID, (
        "Second intermediate response must be a large binary, but didn't receive a binary transfer UUID"
    )
    assert (
        download_binary(binary_download_stub, uuid.UUID(intermediates[1].Binary.binaryTransferUUID))
        == b"abc" * 1_000_000
    ), "Second intermediate response was not 'abc' repeated 1,000,000 times"
    assert (
        intermediates[2].Binary.value == b"SiLA2_Test_String_Value"
    ), "Third intermediate response was not 'SiLA2_Test_String_Value'"
