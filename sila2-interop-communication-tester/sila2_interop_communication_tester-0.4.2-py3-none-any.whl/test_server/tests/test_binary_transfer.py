from pytest import fail

from sila2_interop_communication_tester.grpc_stubs.BinaryTransferTest_pb2 import Metadata_String
from sila2_interop_communication_tester.grpc_stubs.SiLABinaryTransfer_pb2 import UploadChunkRequest
from sila2_interop_communication_tester.grpc_stubs.SiLAFramework_pb2 import Binary
from sila2_interop_communication_tester.test_server.helpers.spy import ServerCall


def binary_was_downloaded(server_calls: dict[str, list[ServerCall]], binary_id: str, binary_length: int) -> bool:
    info_calls = [
        call for call in server_calls["BinaryDownload.GetBinaryInfo"] if call.request.binaryTransferUUID == binary_id
    ]
    if not info_calls:
        return False

    chunk_calls = server_calls["BinaryDownload.GetChunk"]
    chunk_requests = []
    for call in chunk_calls:
        for request in call.request:
            if request.binaryTransferUUID == binary_id:
                chunk_requests.append(request)

    requested_bytes = [False] * binary_length
    for chunk_request in chunk_requests:
        for i in range(chunk_request.offset, chunk_request.offset + chunk_request.length):
            try:
                requested_bytes[i] = True
            except IndexError:
                raise IndexError(
                    f"Expected GetChunk calls for {binary_length} bytes, "
                    f"but byte {i} was requested for binary {binary_id}"
                )

    return all(requested_bytes)


def get_uploaded_binary(server_calls: dict[str, list[ServerCall]], binary_id: str, parameter_id: str) -> bytes:
    creation_calls = [
        call
        for call in server_calls["BinaryUpload.CreateBinary"]
        if call.successful and call.result.binaryTransferUUID == binary_id
    ]
    assert creation_calls, f"No CreateBinary call received for binary with UUID {binary_id}"

    creation_call = creation_calls[0]
    expected_binary_length = creation_call.request.binarySize
    expected_chunk_count = creation_call.request.chunkCount
    requested_parameter_id = creation_call.request.parameterIdentifier

    assert (
        parameter_id == requested_parameter_id
    ), f"binary {binary_id} was uploaded for {requested_parameter_id!r}, expected {parameter_id!r}"

    chunk_calls = server_calls["BinaryUpload.UploadChunk"]
    chunk_requests: list[UploadChunkRequest] = []
    for chunk_call in chunk_calls:
        for chunk_request in chunk_call.request:
            if chunk_request.binaryTransferUUID == binary_id:
                chunk_requests.append(chunk_request)

    expected_chunks = set(range(expected_chunk_count))
    actual_chunks = {request.chunkIndex for request in chunk_requests}
    assert expected_chunks == actual_chunks, f"Expected uploaded chunks {expected_chunks}, got {actual_chunks}"

    chunks: dict[int, bytes] = {}
    for chunk_request in chunk_requests:
        chunks[chunk_request.chunkIndex] = chunk_request.payload

    binary = b"".join(chunks[i] for i in range(expected_chunk_count))
    assert len(binary) == expected_binary_length, f"Expected {expected_binary_length} bytes, got {len(binary)}"

    return binary


def test_small_binary_property_is_read(server_calls):
    get_calls = server_calls["BinaryTransferTest.Get_BinaryValueDirectly"]
    assert get_calls


def test_echo_binary_value_executed_with_abc(server_calls):
    calls = server_calls["BinaryTransferTest.EchoBinaryValue"]
    assert any(
        call
        for call in calls
        if call.request.BinaryValue.HasField("value") and call.request.BinaryValue.value == b"abc"
    )


def test_echo_binary_value_executed_with_1e6_times_abc(server_calls):
    calls = [
        call
        for call in server_calls["BinaryTransferTest.EchoBinaryValue"]
        if call.request.HasField("BinaryValue") and call.request.BinaryValue.HasField("binaryTransferUUID")
    ]
    binary_ids: list[str] = [call.request.BinaryValue.binaryTransferUUID for call in calls]

    for binary_id in binary_ids:
        try:
            binary = get_uploaded_binary(
                server_calls,
                binary_id,
                "org.silastandard/test/BinaryTransferTest/v1/Command/EchoBinaryValue/Parameter/BinaryValue",
            )
            if binary == b"abc" * 1_000_000:
                return
        except:  # noqa: E722
            pass
    fail("No large binary used as parameter for EchoBinaryValue was 'abc' repeated 1,000,000 times")


def test_large_binary_property_is_read(server_calls):
    get_calls = server_calls["BinaryTransferTest.Get_BinaryValueDownload"]
    assert get_calls, "BinaryTransferTest.Get_BinaryValueDownload was never called"

    binary_ids: list[str] = [call.result.BinaryValueDownload.binaryTransferUUID for call in get_calls]

    for binary_id in binary_ids:
        if binary_was_downloaded(
            server_calls,
            binary_id,
            len("A_slightly_longer_SiLA2_Test_String_Value_used_to_demonstrate_the_binary_download" * 100_000),
        ):
            return

    fail("Full content of property BinaryValueDownload was never requested")


def test_echo_binaries_observably_called_with_abc_and_1e6_times_abc_and_SiLA2_Test_String_Value(server_calls):
    init_calls = server_calls["BinaryTransferTest.EchoBinariesObservably"]
    assert init_calls, "EchoBinariesObservably was not called"

    # check parameters
    for call in init_calls:
        binaries = call.request.Binaries
        if len(binaries) != 3:
            continue
        if not binaries[0].HasField("value"):
            continue
        if not binaries[0].value == b"abc":
            continue
        if not binaries[1].HasField("binaryTransferUUID"):
            continue
        if (
            get_uploaded_binary(
                server_calls,
                binaries[1].binaryTransferUUID,
                "org.silastandard/test/BinaryTransferTest/v1/Command/EchoBinariesObservably/Parameter/Binaries",
            )
            != b"abc" * 1_000_000
        ):
            continue
        if not binaries[2].HasField("value"):
            continue
        if not binaries[2].value == b"SiLA2_Test_String_Value":
            continue
        exec_id: str = call.result.commandExecutionUUID.value
        break
    else:
        fail(
            "EchoBinariesObservably was not called with the list ['abc', 'abc' repeated 1,000,000 times, 'SiLA2_Test_String_Value'] (ascii-encoded)"
        )

    # check response was downloaded
    response_calls = [
        call
        for call in server_calls["BinaryTransferTest.EchoBinariesObservably_Result"]
        if call.request.value == exec_id
    ]
    assert response_calls, "The result of EchoBinariesObservably was never requested"

    for call in response_calls:
        if binary_was_downloaded(
            server_calls, call.result.JointBinary.binaryTransferUUID, 3 * 1_000_001 + len("SiLA2_Test_String_Value")
        ):
            break
    else:
        fail("The response of EchoBinariesObservably was not fully downloaded")

    # check large intermediate responses were downloaded
    intermediate_calls = [
        call
        for call in server_calls["BinaryTransferTest.EchoBinariesObservably_Intermediate"]
        if call.request.value == exec_id
    ]
    assert intermediate_calls, "The intermediate responses of EchoBinariesObservably were never requested"

    for call in intermediate_calls:
        for response in call.result.streamed_responses:
            if response.Binary.HasField("binaryTransferUUID"):
                if binary_was_downloaded(server_calls, response.Binary.binaryTransferUUID, 3 * 1_000_000):
                    return
    fail("The large binary intermediate response of EchoBinariesObservably was not fully downloaded")


def test_echo_binary_and_metadata_string_called_with_abc_and_metadata_abc(server_calls):
    calls = server_calls["BinaryTransferTest.EchoBinaryAndMetadataString"]
    assert calls, "BinaryTransferTest.EchoBinaryAndMetadata was never called"

    for call in calls:
        if Metadata_String not in call.metadata:
            continue
        if call.metadata[Metadata_String].String.value != "abc":
            continue
        if call.request.Binary.value != b"abc":
            continue
        return
    fail(
        "BinaryTransferTest.EchoBinaryAndMetadataString was never call with the binary parameter 'abc' "
        "and String metadata 'abc'"
    )


def test_echo_binary_and_metadata_string_called_with_1_000_000_times_abc_and_metadata_abc(server_calls):
    calls = server_calls["BinaryTransferTest.EchoBinaryAndMetadataString"]
    assert calls, "BinaryTransferTest.EchoBinaryAndMetadata was never called"

    for call in calls:
        if Metadata_String not in call.metadata:
            continue
        if call.metadata[Metadata_String].String.value != "abc":
            continue
        if (
            call.request.Binary.HasField("binaryTransferUUID")
            and get_uploaded_binary(
                server_calls,
                call.request.Binary.binaryTransferUUID,
                "org.silastandard/test/BinaryTransferTest/v1/Command/EchoBinaryAndMetadataString/Parameter/Binary",
            )
            != b"abc" * 1_000_000
        ):
            continue
        return
    fail(
        "BinaryTransferTest.EchoBinaryAndMetadataString was never call with the binary parameter 'abc' "
        "and String metadata 'abc'"
    )
