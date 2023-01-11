import uuid
from dataclasses import dataclass, field
from functools import cached_property
from typing import Callable, Iterable, Iterator, Optional

from grpc import ServicerContext

from sila2_interop_communication_tester.grpc_stubs import SiLABinaryTransfer_pb2
from sila2_interop_communication_tester.grpc_stubs.SiLABinaryTransfer_pb2_grpc import BinaryUploadServicer
from sila2_interop_communication_tester.helpers.utils import string_is_uuid
from sila2_interop_communication_tester.test_server.helpers import binary_transfer
from sila2_interop_communication_tester.test_server.helpers.protobuf import duration_from_seconds
from sila2_interop_communication_tester.test_server.helpers.raise_error import (
    raise_binary_upload_failed_error,
    raise_invalid_binary_transfer_uuid_error,
)
from sila2_interop_communication_tester.test_server.helpers.spy import MetadataDict, extract_metadata


@dataclass
class Binary:
    num_chunks: int
    size: int
    chunks: dict[int, bytes] = field(default_factory=dict)

    @property
    def completed(self) -> bool:
        return len(self.chunks) == self.num_chunks

    @property
    def current_size(self) -> int:
        return sum(len(chunk) for chunk in self.chunks.values())

    @cached_property
    def uploaded_binary(self) -> bytes:
        return b"".join(self.chunks[i] for i in range(self.num_chunks))


class BinaryUploadImpl(BinaryUploadServicer):
    def __init__(
        self,
        allowed_parameters: Iterable[str],
        metadata_validate_funcs: Optional[dict[str, Callable[[MetadataDict, ServicerContext], None]]] = None,
    ) -> None:
        self.allowed_parameters = set(allowed_parameters)
        self.binaries: dict[uuid.UUID, Binary] = {}

        self.metadata_validate_funcs: dict[str, Callable[[MetadataDict, ServicerContext], None]] = (
            metadata_validate_funcs if metadata_validate_funcs is not None else {}
        )

        binary_transfer.HELPER.uploader = self

    def CreateBinary(
        self, request: SiLABinaryTransfer_pb2.CreateBinaryRequest, context: ServicerContext
    ) -> SiLABinaryTransfer_pb2.CreateBinaryResponse:
        target_parameter = request.parameterIdentifier
        if target_parameter not in self.allowed_parameters:
            raise_binary_upload_failed_error(context, f"Binary upload not allowed for parameter '{target_parameter}'")

        metadata = extract_metadata(context)
        if target_parameter in self.metadata_validate_funcs:
            self.metadata_validate_funcs[target_parameter](metadata, context)

        binary_id = uuid.uuid4()
        binary = Binary(num_chunks=request.chunkCount, size=request.binarySize)
        self.binaries[binary_id] = binary

        return SiLABinaryTransfer_pb2.CreateBinaryResponse(
            binaryTransferUUID=str(binary_id), lifetimeOfBinary=duration_from_seconds(600)
        )

    def UploadChunk(
        self,
        request_iterator: Iterator[SiLABinaryTransfer_pb2.UploadChunkRequest],
        context: ServicerContext,
    ) -> Iterator[SiLABinaryTransfer_pb2.UploadChunkResponse]:
        for request in request_iterator:
            binary_id = request.binaryTransferUUID
            if not string_is_uuid(binary_id):
                raise_invalid_binary_transfer_uuid_error(
                    context, f"Given id is not a valid UUID: {request.binaryTransferUUID}"
                )

            binary_uuid = uuid.UUID(binary_id)
            if binary_uuid not in self.binaries:
                raise_invalid_binary_transfer_uuid_error(
                    context, f"No binary exists with UUID {request.binaryTransferUUID}"
                )

            binary = self.binaries[binary_uuid]
            chunk_index = request.chunkIndex
            if chunk_index >= binary.num_chunks:
                raise_binary_upload_failed_error(
                    context,
                    f"Failed to upload chunk for {request.binaryTransferUUID}:"
                    f"Chunk index {chunk_index} out of range for binary with {binary.num_chunks} chunks",
                )

            if len(request.payload) > 1024 * 1024 * 2:
                raise_binary_upload_failed_error(
                    context,
                    f"Failed to upload chunk for {request.binaryTransferUUID}:" f"Chunks must not be larger than 2 MiB",
                )

            if binary.current_size + len(request.payload) > binary.size:
                raise_binary_upload_failed_error(
                    context,
                    f"Failed to upload chunk for {request.binaryTransferUUID}:"
                    f"Tried to upload more bytes than originally announced",
                )

            if chunk_index in binary.chunks:
                raise_binary_upload_failed_error(
                    context, f"Tried to upload chunk {chunk_index} twice for binary {binary_id}"
                )

            binary.chunks[chunk_index] = request.payload

            yield SiLABinaryTransfer_pb2.UploadChunkResponse(
                binaryTransferUUID=binary_id, chunkIndex=chunk_index, lifetimeOfBinary=duration_from_seconds(600)
            )

    def DeleteBinary(
        self, request: SiLABinaryTransfer_pb2.DeleteBinaryRequest, context: ServicerContext
    ) -> SiLABinaryTransfer_pb2.DeleteBinaryResponse:
        binary_id = request.binaryTransferUUID
        if not string_is_uuid(binary_id):
            raise_invalid_binary_transfer_uuid_error(
                context, f"Given id is not a valid UUID: {request.binaryTransferUUID}"
            )

        binary_uuid = uuid.UUID(binary_id)
        if binary_uuid not in self.binaries:
            raise_invalid_binary_transfer_uuid_error(
                context, f"No binary exists with UUID {request.binaryTransferUUID}"
            )

        del self.binaries[binary_uuid]

        return SiLABinaryTransfer_pb2.DeleteBinaryResponse()

    def get_binary(self, binary_uuid: uuid.UUID) -> bytes:
        return self.binaries[binary_uuid].uploaded_binary
