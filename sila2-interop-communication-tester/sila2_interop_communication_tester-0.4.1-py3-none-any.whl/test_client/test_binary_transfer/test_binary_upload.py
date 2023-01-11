import uuid

from sila2_interop_communication_tester.grpc_stubs.BinaryTransferTest_pb2 import EchoBinaryValue_Parameters
from sila2_interop_communication_tester.grpc_stubs.SiLABinaryTransfer_pb2 import (
    CreateBinaryRequest,
    DeleteBinaryRequest,
    UploadChunkRequest,
)
from sila2_interop_communication_tester.grpc_stubs.SiLAFramework_pb2 import Binary
from sila2_interop_communication_tester.test_client.helpers.binary_transfer import download_binary, upload_binary
from sila2_interop_communication_tester.test_client.helpers.error_handling import (
    raises_binary_upload_failed_error,
    raises_invalid_binary_transfer_uuid_error,
    raises_validation_error,
)


def test_create_binary_fails_on_non_fully_qualified_parameter_identifier(binary_upload_stub):
    """
    BinaryUpload.CreateBinary should fail with a Binary Upload Failed error if the `parameterIdentifier` does not match
    the pattern for fully qualified parameter identifiers
    """
    with raises_binary_upload_failed_error():
        binary_upload_stub.CreateBinary(
            CreateBinaryRequest(binarySize=3 * 1024 * 1024, chunkCount=3, parameterIdentifier="Binaries")
        )


def test_create_binary_fails_on_unknown_parameter_identifier(binary_upload_stub):
    """
    BinaryUpload.CreateBinary should fail with a Binary Upload Failed error if the `parameterIdentifier` matches the
    pattern for fully qualified parameter identifiers but that parameter does not exist
    """
    with raises_binary_upload_failed_error():
        binary_upload_stub.CreateBinary(
            CreateBinaryRequest(
                binarySize=3 * 1024 * 1024,
                chunkCount=3,
                parameterIdentifier="com.example/unknown/SomeFeature/v1/Command/SomeCommand/Parameter/SomeParameter",
            )
        )


def test_create_binary_fails_on_non_binary_parameter_identifier(binary_upload_stub):
    """
    BinaryUpload.CreateBinary should fail with a Binary Upload Failed error if the `parameterIdentifier` refers to a
    known command parameter but this parameter cannot hold a Binary
    """
    with raises_binary_upload_failed_error():
        binary_upload_stub.CreateBinary(
            CreateBinaryRequest(
                binarySize=3 * 1024 * 1024,
                chunkCount=3,
                parameterIdentifier="org.silastandard/core/SiLAService/v1/Command/SetServerName/Parameter/ServerName",
            )
        )


def test_create_binary_fails_on_parameter_identifier_with_additional_characters(binary_upload_stub):
    """
    BinaryUpload.CreateBinary should fail with a Binary Upload Failed error if the `parameterIdentifier` contains the
    fully qualified identifier of a known command parameter which can hold a binary, but also some other characters
    """
    with raises_binary_upload_failed_error():
        binary_upload_stub.CreateBinary(
            CreateBinaryRequest(
                binarySize=3 * 1024 * 1024,
                chunkCount=3,
                parameterIdentifier=(
                    "sila2-org.silastandard/test/BinaryTransferTest/v1/Command/EchoBinaryValue/Parameter/BinaryValue"
                ),
            )
        )


def test_upload_chunk_rejects_non_uuid_strings(binary_upload_stub):
    """RPC BinaryUpload.UploadChunk should reject non-UUID strings with a Invalid Binary Transfer UUID error"""
    call = binary_upload_stub.UploadChunk(
        (UploadChunkRequest(chunkIndex=i, binaryTransferUUID="abc", payload=b"abc") for i in range(2))
    )
    with raises_invalid_binary_transfer_uuid_error():
        next(call)


def test_upload_chunk_rejects_unknown_uuids(binary_upload_stub):
    """RPC BinaryUpload.UploadChunk should reject randomly created UUIDs with an Invalid Binary Transfer UUID error"""
    call = binary_upload_stub.UploadChunk(
        (UploadChunkRequest(chunkIndex=i, binaryTransferUUID=str(uuid.uuid4()), payload=b"abc") for i in range(2))
    )
    with raises_invalid_binary_transfer_uuid_error():
        next(call)


def test_upload_chunk_rejects_too_large_chunk_indices(binary_upload_stub):
    """Server expects 2 chunks with 4 MB combined payload, client sends 2 2 MB chunks with indices 0 and 2"""
    info = binary_upload_stub.CreateBinary(
        CreateBinaryRequest(
            binarySize=4 * 1024 * 1024,
            chunkCount=2,
            parameterIdentifier=(
                "org.silastandard/test/BinaryTransferTest/v1/Command/EchoBinaryValue/Parameter/BinaryValue"
            ),
        )
    )
    call = binary_upload_stub.UploadChunk(
        (
            UploadChunkRequest(chunkIndex=i, binaryTransferUUID=info.binaryTransferUUID, payload=b"a" * 2 * 1024 * 1024)
            for i in [0, 2]
        )
    )
    next(call)
    with raises_binary_upload_failed_error():
        next(call)


def test_upload_chunk_rejects_too_many_uploaded_bytes(binary_upload_stub):
    """Server expects 3 chunks with 3 MB combined payload, receives 3 chunks with 2 MB payload each"""
    info = binary_upload_stub.CreateBinary(
        CreateBinaryRequest(
            binarySize=3 * 1024 * 1024,
            chunkCount=3,
            parameterIdentifier=(
                "org.silastandard/test/BinaryTransferTest/v1/Command/EchoBinaryValue/Parameter/BinaryValue"
            ),
        )
    )
    call = binary_upload_stub.UploadChunk(
        (
            UploadChunkRequest(chunkIndex=i, binaryTransferUUID=info.binaryTransferUUID, payload=b"a" * 2 * 1024 * 1024)
            for i in range(3)
        )
    )
    next(call)
    with raises_binary_upload_failed_error():
        next(call)


def test_server_handles_multiple_sequential_uploadchunk_streams_for_same_binary(
    binary_upload_stub, binary_download_stub, binarytransfertest_stub
):
    """
    - Call BinaryUpload.CreateBinary to upload a 3 MB binary for the parameter 'BinaryValue' of
        BinaryTransferTest.EchoBinaryValue in 3 chunks
    - Call BinaryUpload.UploadChunk and send one UploadChunkRequest for uploading the first MB
    - Call BinaryUpload.UploadChunk again and send one UploadChunkRequest for uploading the second MB
    - Call BinaryUpload.UploadChunk again and send one UploadChunkRequest for uploading the third MB
    - Expect that the binary can be used as a parameter for BinaryTransferTest.EchoBinaryValue
    """
    # announce upload of 3 MB in 3 chunks
    info = binary_upload_stub.CreateBinary(
        CreateBinaryRequest(
            binarySize=3 * 1024 * 1024,
            chunkCount=3,
            parameterIdentifier=(
                "org.silastandard/test/BinaryTransferTest/v1/Command/EchoBinaryValue/Parameter/BinaryValue"
            ),
        )
    )

    # upload the three chunks in three separate RPC calls
    requests = [
        UploadChunkRequest(chunkIndex=i, binaryTransferUUID=info.binaryTransferUUID, payload=b"a" * 1024 * 1024)
        for i in range(3)
    ]
    for i in range(3):
        next(binary_upload_stub.UploadChunk(iter((requests[i],))))

    # use binary
    response = binarytransfertest_stub.EchoBinaryValue(
        EchoBinaryValue_Parameters(BinaryValue=Binary(binaryTransferUUID=info.binaryTransferUUID))
    )
    assert (
        download_binary(binary_download_stub, uuid.UUID(response.ReceivedValue.binaryTransferUUID))
        == b"a" * 3 * 1024 * 1024
    )


def test_server_rejects_use_of_incompletely_uploaded_binary(binary_upload_stub, binarytransfertest_stub):
    """
    Setup:
    - Call BinaryUpload.CreateBinary to upload a 3 MB binary for the parameter 'BinaryValue' of
        BinaryTransferTest.EchoBinaryValue in 3 chunks
    - Call BinaryUpload.UploadChunk and send two UploadChunkRequest for uploading the first and second MB
    - Expect that using that incompletely uploaded binary for BinaryTransferTest.EchoBinaryValue leads to a
        Validation Error
    """
    # announce upload of 3 MB in 3 chunks
    info = binary_upload_stub.CreateBinary(
        CreateBinaryRequest(
            binarySize=3 * 1024 * 1024,
            chunkCount=3,
            parameterIdentifier=(
                "org.silastandard/test/BinaryTransferTest/v1/Command/EchoBinaryValue/Parameter/BinaryValue"
            ),
        )
    )

    # upload 2 chunks of 1 MB each
    call = binary_upload_stub.UploadChunk(
        (
            UploadChunkRequest(chunkIndex=i, binaryTransferUUID=info.binaryTransferUUID, payload=b"a" * 1024 * 1024)
            for i in range(2)
        )
    )
    list(call)

    # try to use incompletely uploaded binary
    with raises_validation_error(
        "org.silastandard/test/BinaryTransferTest/v1/Command/EchoBinaryValue/Parameter/BinaryValue"
    ):
        binarytransfertest_stub.EchoBinaryValue(
            EchoBinaryValue_Parameters(BinaryValue=Binary(binaryTransferUUID=info.binaryTransferUUID))
        )


def test_delete_binary_rejects_non_uuid_strings(binary_upload_stub):
    """RPC BinaryUpload.DeleteBinary should reject non-UUID strings with a Invalid Binary Transfer UUID error"""
    with raises_invalid_binary_transfer_uuid_error():
        binary_upload_stub.DeleteBinary(DeleteBinaryRequest(binaryTransferUUID="abc"))


def test_delete_binary_rejects_unknown_uuids(binary_upload_stub):
    """RPC BinaryUpload.DeleteBinary should reject randomly created UUIDs with an Invalid Binary Transfer UUID error"""
    with raises_invalid_binary_transfer_uuid_error():
        binary_upload_stub.DeleteBinary(DeleteBinaryRequest(binaryTransferUUID=str(uuid.uuid4())))


def test_server_rejects_usage_of_deleted_binary(binary_upload_stub, binarytransfertest_stub):
    """
    - Upload a binary
    - Delete the binary using BinaryUpload.DeleteBinary
    - Try to use it as parameter, this should lead to a Validation Error
    """
    upload_id = upload_binary(
        binary_upload_stub,
        b"abc" * 1_000_000,
        "org.silastandard/test/BinaryTransferTest/v1/Command/EchoBinaryValue/Parameter/BinaryValue",
    )
    binary_upload_stub.DeleteBinary(DeleteBinaryRequest(binaryTransferUUID=str(upload_id)))

    with raises_validation_error(
        "org.silastandard/test/BinaryTransferTest/v1/Command/EchoBinaryValue/Parameter/BinaryValue"
    ):
        binarytransfertest_stub.EchoBinaryValue(
            EchoBinaryValue_Parameters(BinaryValue=Binary(binaryTransferUUID=str(upload_id)))
        )


def test_upload_chunk_twice(binary_upload_stub, binarytransfertest_stub):
    """
    - Call BinaryUpload.CreateBinary to upload a 3 MB binary for the parameter 'BinaryValue' of
        BinaryTransferTest.EchoBinaryValue in 3 chunks
    - Request the upload of two chunks with index 1
    """
    # announce upload of 3 MB in 3 chunks
    info = binary_upload_stub.CreateBinary(
        CreateBinaryRequest(
            binarySize=3 * 1024 * 1024,
            chunkCount=3,
            parameterIdentifier=(
                "org.silastandard/test/BinaryTransferTest/v1/Command/EchoBinaryValue/Parameter/BinaryValue"
            ),
        )
    )

    # try upload of chunks
    requests = [
        UploadChunkRequest(chunkIndex=0, binaryTransferUUID=info.binaryTransferUUID, payload=b"a" * 1024 * 1024),
        UploadChunkRequest(chunkIndex=1, binaryTransferUUID=info.binaryTransferUUID, payload=b"a" * 1024 * 1024),
        UploadChunkRequest(chunkIndex=1, binaryTransferUUID=info.binaryTransferUUID, payload=b"a" * 1024 * 1024),
    ]
    call = binary_upload_stub.UploadChunk(iter(requests))
    next(call)
    next(call)
    with raises_binary_upload_failed_error():
        next(call)


def test_upload_of_chunk_larger_than_2mb_is_rejected(binary_upload_stub):
    """
    - Call BinaryUpload.CreateBinary to upload a 3 MB binary for the parameter 'BinaryValue' of
        BinaryTransferTest.EchoBinaryValue in 3 chunks
    - Call BinaryUpload.UploadChunk, send a 512 kB chunk and a chunk with 1024 * 1024 * 2 + 1 bytes
    - Expect that the upload fails
    """
    # announce upload of 3 MB in 3 chunks
    info = binary_upload_stub.CreateBinary(
        CreateBinaryRequest(
            binarySize=3 * 1024 * 1024,
            chunkCount=3,
            parameterIdentifier=(
                "org.silastandard/test/BinaryTransferTest/v1/Command/EchoBinaryValue/Parameter/BinaryValue"
            ),
        )
    )

    # upload 2 chunks of 1 MB each
    requests = [
        UploadChunkRequest(chunkIndex=0, binaryTransferUUID=info.binaryTransferUUID, payload=b"a" * 1024 * 512),
        UploadChunkRequest(
            chunkIndex=1, binaryTransferUUID=info.binaryTransferUUID, payload=b"a" * 1024 * 1024 * 2 + b"a"
        ),
        UploadChunkRequest(chunkIndex=2, binaryTransferUUID=info.binaryTransferUUID, payload=b"a"),
    ]
    call = binary_upload_stub.UploadChunk(iter(requests))
    next(call)

    with raises_binary_upload_failed_error():
        next(call)


def test_upload_works_with_reverse_chunk_order(binary_upload_stub, binarytransfertest_stub, binary_download_stub):
    """
    - Call BinaryUpload.CreateBinary to upload a 3 MB binary for the parameter 'BinaryValue' of
        BinaryTransferTest.EchoBinaryValue in 3 chunks
    - Call BinaryUpload.UploadChunk and send three 1MB chunks in reverse order (indices 2, 1, 0)
    - Expect that the command works
    """
    # announce upload of 3 MB in 3 chunks
    info = binary_upload_stub.CreateBinary(
        CreateBinaryRequest(
            binarySize=3 * 1024 * 1024,
            chunkCount=3,
            parameterIdentifier=(
                "org.silastandard/test/BinaryTransferTest/v1/Command/EchoBinaryValue/Parameter/BinaryValue"
            ),
        )
    )

    # upload chunks
    requests = [
        UploadChunkRequest(chunkIndex=2, binaryTransferUUID=info.binaryTransferUUID, payload=b"a" * 1024 * 1024),
        UploadChunkRequest(chunkIndex=1, binaryTransferUUID=info.binaryTransferUUID, payload=b"a" * 1024 * 1024),
        UploadChunkRequest(chunkIndex=0, binaryTransferUUID=info.binaryTransferUUID, payload=b"a" * 1024 * 1024),
    ]
    call = binary_upload_stub.UploadChunk(iter(requests))
    list(call)

    # assert it worked
    response = binarytransfertest_stub.EchoBinaryValue(
        EchoBinaryValue_Parameters(BinaryValue=Binary(binaryTransferUUID=info.binaryTransferUUID))
    )
    assert download_binary(binary_download_stub, response.ReceivedValue.binaryTransferUUID) == b"a" * 1024 * 1024 * 3


def test_empty_chunks_are_accepted(binary_upload_stub, binary_download_stub, binarytransfertest_stub):
    """
    - Call BinaryUpload.CreateBinary to upload a 3 MB binary for the parameter 'BinaryValue' of
        BinaryTransferTest.EchoBinaryValue in 3 chunks
    - Call BinaryUpload.UploadChunk and send two 1.1MB chunks and an empty chunk
    - Expect that the command works
    """
    # announce upload of 3 MB in 3 chunks
    info = binary_upload_stub.CreateBinary(
        CreateBinaryRequest(
            binarySize=3 * 1024 * 1024,
            chunkCount=3,
            parameterIdentifier=(
                "org.silastandard/test/BinaryTransferTest/v1/Command/EchoBinaryValue/Parameter/BinaryValue"
            ),
        )
    )

    # upload 2 chunks of 1.1 MB each
    chunk_size = int(1024 * 1024 * 1.1)
    requests = [
        UploadChunkRequest(chunkIndex=0, binaryTransferUUID=info.binaryTransferUUID, payload=b"a" * chunk_size),
        UploadChunkRequest(chunkIndex=1, binaryTransferUUID=info.binaryTransferUUID, payload=b"a" * chunk_size),
        UploadChunkRequest(chunkIndex=2, binaryTransferUUID=info.binaryTransferUUID, payload=b""),
    ]
    call = binary_upload_stub.UploadChunk(iter(requests))
    list(call)

    # assert it worked
    response = binarytransfertest_stub.EchoBinaryValue(
        EchoBinaryValue_Parameters(BinaryValue=Binary(binaryTransferUUID=info.binaryTransferUUID))
    )
    assert download_binary(binary_download_stub, response.ReceivedValue.binaryTransferUUID) == b"a" * chunk_size * 2


def test_delete_partially_uploaded_binary(binary_upload_stub, binarytransfertest_stub):
    """
    - Create a binary with 3 chunks
    - Upload two chunks
    - Request deletion
    - Try to upload third chunk
    """
    # announce upload of 3 MB in 3 chunks
    info = binary_upload_stub.CreateBinary(
        CreateBinaryRequest(
            binarySize=3 * 1024 * 1024,
            chunkCount=3,
            parameterIdentifier=(
                "org.silastandard/test/BinaryTransferTest/v1/Command/EchoBinaryValue/Parameter/BinaryValue"
            ),
        )
    )

    # upload 2 chunks of 1 MB each
    chunk_size = 1024 * 1024
    requests = [
        UploadChunkRequest(chunkIndex=0, binaryTransferUUID=info.binaryTransferUUID, payload=b"a" * chunk_size),
        UploadChunkRequest(chunkIndex=1, binaryTransferUUID=info.binaryTransferUUID, payload=b"a" * chunk_size),
    ]
    call = binary_upload_stub.UploadChunk(iter(requests))
    next(call)
    next(call)

    # delete binary
    binary_upload_stub.DeleteBinary(DeleteBinaryRequest(binaryTransferUUID=info.binaryTransferUUID))

    # upload of third chunk should fail
    call = binary_upload_stub.UploadChunk(
        iter([UploadChunkRequest(chunkIndex=2, binaryTransferUUID=info.binaryTransferUUID, payload=b"a" * chunk_size)])
    )
    with raises_invalid_binary_transfer_uuid_error():
        next(call)

    # usage of binary as parameter should fail
    with raises_validation_error(
        "org.silastandard/test/BinaryTransferTest/v1/Command/EchoBinaryValue/Parameter/BinaryValue"
    ):
        binarytransfertest_stub.EchoBinaryValue(
            EchoBinaryValue_Parameters(BinaryValue=Binary(binaryTransferUUID=info.binaryTransferUUID))
        )
