import uuid

from sila2_interop_communication_tester.grpc_stubs.BinaryTransferTest_pb2 import EchoBinaryValue_Parameters
from sila2_interop_communication_tester.grpc_stubs.SiLABinaryTransfer_pb2 import (
    DeleteBinaryRequest,
    GetBinaryInfoRequest,
    GetChunkRequest,
)
from sila2_interop_communication_tester.grpc_stubs.SiLAFramework_pb2 import Binary
from sila2_interop_communication_tester.test_client.helpers.binary_transfer import upload_binary
from sila2_interop_communication_tester.test_client.helpers.error_handling import (
    raises_binary_download_failed_error,
    raises_invalid_binary_transfer_uuid_error,
)


def test_get_binary_info_rejects_non_uuid_strings(binary_download_stub):
    """RPC BinaryDownload.GetBinaryInfo should reject non-UUID strings with a Invalid Binary Transfer UUID error"""
    with raises_invalid_binary_transfer_uuid_error():
        binary_download_stub.GetBinaryInfo(GetBinaryInfoRequest(binaryTransferUUID="abc"))


def test_get_binary_info_rejects_unknown_uuids(binary_download_stub):
    """
    RPC BinaryDownload.GetBinaryInfo should reject randomly created UUIDs with an Invalid Binary Transfer UUID error
    """
    with raises_invalid_binary_transfer_uuid_error():
        binary_download_stub.GetBinaryInfo(GetBinaryInfoRequest(binaryTransferUUID=str(uuid.uuid4())))


def test_upload_chunk_rejects_non_uuid_strings(binary_download_stub):
    """RPC BinaryDownload.GetChunk should reject non-UUID strings with a Invalid Binary Transfer UUID error"""
    call = binary_download_stub.GetChunk(iter((GetChunkRequest(binaryTransferUUID="abc", offset=0, length=10),)))
    with raises_invalid_binary_transfer_uuid_error():
        next(call)


def test_upload_chunk_rejects_unknown_uuids(binary_download_stub):
    """RPC BinaryDownload.GetChunk should reject randomly created UUIDs with an Invalid Binary Transfer UUID error"""
    call = binary_download_stub.GetChunk(
        iter((GetChunkRequest(binaryTransferUUID=str(uuid.uuid4()), offset=0, length=10),))
    )
    with raises_invalid_binary_transfer_uuid_error():
        next(call)


def test_delete_binary_rejects_non_uuid_strings(binary_download_stub):
    """RPC BinaryDownload.DeleteBinary should reject non-UUID strings with a Invalid Binary Transfer UUID error"""
    with raises_invalid_binary_transfer_uuid_error():
        binary_download_stub.DeleteBinary(DeleteBinaryRequest(binaryTransferUUID="abc"))


def test_delete_binary_rejects_unknown_uuids(binary_download_stub):
    """
    RPC BinaryDownload.DeleteBinary should reject randomly created UUIDs with an Invalid Binary Transfer UUID error
    """
    with raises_invalid_binary_transfer_uuid_error():
        binary_download_stub.DeleteBinary(DeleteBinaryRequest(binaryTransferUUID=str(uuid.uuid4())))


def test_get_chunk_rejects_read_out_of_bounds(binary_download_stub, binarytransfertest_stub, binary_upload_stub):
    """
    Setup:
    - Upload 3 MB binary for BinaryTransferTest.EchoBinaryValue parameter 'BinaryValue'
    - Call BinaryTransferTest.EchoBinaryValue with that binary

    Test:
    - Send a GetChunkRequest to BinaryDownload.GetChunk, asking for the last MB plus one more byte of the response
      - This should fail with a Binary Download Error, since that last byte does not exist
    """
    # upload parameter
    binary_id = upload_binary(
        binary_upload_stub,
        b"a" * 3 * 1024 * 1024,
        "org.silastandard/test/BinaryTransferTest/v1/Command/EchoBinaryValue/Parameter/BinaryValue",
    )
    # call command
    response = binarytransfertest_stub.EchoBinaryValue(
        EchoBinaryValue_Parameters(BinaryValue=Binary(binaryTransferUUID=str(binary_id)))
    )
    # try to download response binary out of bounds
    call = binary_download_stub.GetChunk(
        iter(
            (
                GetChunkRequest(
                    binaryTransferUUID=str(response.ReceivedValue.binaryTransferUUID),
                    offset=2 * 1024 * 1024,
                    length=1024 * 1024 + 1,
                ),
            )
        )
    )
    with raises_binary_download_failed_error():
        next(call)


def test_delete_binary(binary_download_stub, binarytransfertest_stub, binary_upload_stub):
    """
    Setup:
    - Upload 3 MB binary for BinaryTransferTest.EchoBinaryValue parameter 'BinaryValue'
    - Call BinaryTransferTest.EchoBinaryValue with that binary
    - Call BinaryDownload.DeleteBinary for the response binary

    Test:
    - BinaryDownload.GetBinaryInfo for the response binary should fail with an Invalid Binary Transfer UUID error
    - BinaryDownload.DeleteBinary for the response binary should fail with an Invalid Binary Transfer UUID error
    - BinaryDownload.GetChunk for the response binary should fail with an Invalid Binary Transfer UUID error
    """
    # upload parameter
    upload_uuid = upload_binary(
        binary_upload_stub,
        b"a" * 3 * 1024 * 1024,
        "org.silastandard/test/BinaryTransferTest/v1/Command/EchoBinaryValue/Parameter/BinaryValue",
    )

    # call command
    response = binarytransfertest_stub.EchoBinaryValue(
        EchoBinaryValue_Parameters(BinaryValue=Binary(binaryTransferUUID=str(upload_uuid)))
    )
    response_uuid = response.ReceivedValue.binaryTransferUUID

    # delete response binary
    binary_download_stub.DeleteBinary(DeleteBinaryRequest(binaryTransferUUID=str(response_uuid)))

    # try to read it
    with raises_invalid_binary_transfer_uuid_error():
        binary_download_stub.GetBinaryInfo(GetBinaryInfoRequest(binaryTransferUUID=str(response_uuid)))
    with raises_invalid_binary_transfer_uuid_error():
        binary_download_stub.DeleteBinary(DeleteBinaryRequest(binaryTransferUUID=str(response_uuid)))
    call = binary_download_stub.GetChunk(
        iter((GetChunkRequest(binaryTransferUUID=str(response_uuid), offset=0, length=1024 * 1024),))
    )
    with raises_invalid_binary_transfer_uuid_error():
        next(call)


def test_download_of_chunk_greater_than_2mib_is_rejected(
    binary_download_stub, binarytransfertest_stub, binary_upload_stub
):
    """
    Setup:
    - Upload 3 MB binary for BinaryTransferTest.EchoBinaryValue parameter 'BinaryValue'
    - Call BinaryTransferTest.EchoBinaryValue with that binary

    Test:
    - Send a GetChunkRequest to BinaryDownload.GetChunk, asking for 512 kiB and then 2 MiB plus one more byte
      - This should fail with a Binary Download Error, since a chunk must not be larger than 2 MiB
    """
    # upload parameter
    binary_id = upload_binary(
        binary_upload_stub,
        b"a" * 3 * 1024 * 1024,
        "org.silastandard/test/BinaryTransferTest/v1/Command/EchoBinaryValue/Parameter/BinaryValue",
    )
    # call command
    response = binarytransfertest_stub.EchoBinaryValue(
        EchoBinaryValue_Parameters(BinaryValue=Binary(binaryTransferUUID=str(binary_id)))
    )
    # try to download response binary with too large chunk size
    chunk_requests = [
        GetChunkRequest(
            binaryTransferUUID=str(response.ReceivedValue.binaryTransferUUID),
            offset=0,
            length=1024 * 512,
        ),
        GetChunkRequest(
            binaryTransferUUID=str(response.ReceivedValue.binaryTransferUUID),
            offset=1024 * 512,
            length=1024 * 1024 * 2 + 1,
        ),
    ]
    call = binary_download_stub.GetChunk(iter(chunk_requests))
    next(call)

    with raises_binary_download_failed_error():
        next(call)
