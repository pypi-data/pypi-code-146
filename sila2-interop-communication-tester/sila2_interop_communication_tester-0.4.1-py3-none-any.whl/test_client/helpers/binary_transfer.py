import math
from typing import Iterable, Optional, Union
from uuid import UUID

from google.protobuf.message import Message

from sila2_interop_communication_tester.grpc_stubs.SiLABinaryTransfer_pb2 import (
    CreateBinaryRequest,
    GetBinaryInfoRequest,
    GetChunkRequest,
    UploadChunkRequest,
)
from sila2_interop_communication_tester.grpc_stubs.SiLABinaryTransfer_pb2_grpc import (
    BinaryDownloadStub,
    BinaryUploadStub,
)
from sila2_interop_communication_tester.helpers.utils import string_is_uuid
from sila2_interop_communication_tester.test_client.helpers.utils import pack_metadata

CHUNK_SIZE = 1024**2


def upload_binary(
    binary_upload_stub: BinaryUploadStub, binary: bytes, parameter_id: str, metadata: Optional[Iterable[Message]] = None
) -> UUID:
    size = len(binary)
    n_chunks = math.ceil(size / CHUNK_SIZE)
    info, _ = binary_upload_stub.CreateBinary.with_call(
        CreateBinaryRequest(
            binarySize=len(binary),
            chunkCount=n_chunks,
            parameterIdentifier=parameter_id,
        ),
        metadata=pack_metadata(*metadata) if metadata is not None else None,
    )
    binary_id = info.binaryTransferUUID

    chunk_requests = (
        UploadChunkRequest(
            binaryTransferUUID=binary_id,
            chunkIndex=chunk_index,
            payload=binary[chunk_index * CHUNK_SIZE : (chunk_index + 1) * CHUNK_SIZE],
        )
        for chunk_index in range(n_chunks)
    )

    for chunk_index, chunk_response in enumerate(binary_upload_stub.UploadChunk(chunk_requests)):
        assert chunk_response.binaryTransferUUID == binary_id
        assert chunk_response.chunkIndex == chunk_index

    return UUID(binary_id)


def download_binary(binary_download_stub: BinaryDownloadStub, binary_transfer_uuid: Union[UUID, str]) -> bytes:
    if isinstance(binary_transfer_uuid, str):
        binary_transfer_uuid = UUID(binary_transfer_uuid)

    info = binary_download_stub.GetBinaryInfo(GetBinaryInfoRequest(binaryTransferUUID=str(binary_transfer_uuid)))
    size = info.binarySize

    n_chunks = math.ceil(size / CHUNK_SIZE)

    chunk_requests = (
        GetChunkRequest(
            binaryTransferUUID=str(binary_transfer_uuid),
            offset=chunk_index * CHUNK_SIZE,
            length=min(CHUNK_SIZE, size - chunk_index * CHUNK_SIZE),
        )
        for chunk_index in range(n_chunks)
    )

    binary = bytearray(size)
    for chunk_index, chunk_response in enumerate(binary_download_stub.GetChunk(chunk_requests)):
        assert string_is_uuid(chunk_response.binaryTransferUUID)
        assert UUID(chunk_response.binaryTransferUUID) == binary_transfer_uuid
        assert chunk_response.offset == chunk_index * CHUNK_SIZE
        assert len(chunk_response.payload) == min(CHUNK_SIZE, size - chunk_index * CHUNK_SIZE)
        binary[chunk_response.offset : chunk_response.offset + len(chunk_response.payload)] = chunk_response.payload

    return bytes(binary)
