import typing
import uuid

import grpc

from sila2_interop_communication_tester.grpc_stubs import SiLABinaryTransfer_pb2
from sila2_interop_communication_tester.grpc_stubs.SiLABinaryTransfer_pb2_grpc import BinaryDownloadServicer
from sila2_interop_communication_tester.helpers.utils import string_is_uuid
from sila2_interop_communication_tester.test_server.helpers import binary_transfer
from sila2_interop_communication_tester.test_server.helpers.protobuf import duration_from_seconds
from sila2_interop_communication_tester.test_server.helpers.raise_error import (
    raise_binary_download_failed_error,
    raise_invalid_binary_transfer_uuid_error,
)


class BinaryDownloadImpl(BinaryDownloadServicer):
    def __init__(self) -> None:
        self.binaries: dict[uuid.UUID, bytes] = {}

        binary_transfer.HELPER.downloader = self

    def GetBinaryInfo(
        self, request: SiLABinaryTransfer_pb2.GetBinaryInfoRequest, context: grpc.ServicerContext
    ) -> SiLABinaryTransfer_pb2.GetBinaryInfoResponse:
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

        return SiLABinaryTransfer_pb2.GetBinaryInfoResponse(
            binarySize=len(self.binaries[binary_uuid]), lifetimeOfBinary=duration_from_seconds(600)
        )

    def GetChunk(
        self, request_iterator: typing.Iterator[SiLABinaryTransfer_pb2.GetChunkRequest], context: grpc.ServicerContext
    ) -> typing.Iterator[SiLABinaryTransfer_pb2.GetChunkResponse]:
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

            if request.length > 1024 * 1024 * 2:
                raise_binary_download_failed_error(context, "Requested chunk size is > 2 MiB")

            binary = self.binaries[binary_uuid]
            if request.offset + request.length > len(binary):
                raise_binary_download_failed_error(
                    context,
                    f"Requested range is out of range for binary {request.binaryTransferUUID} of length {len(binary)} "
                    f"(offset: {request.offset}, length: {request.length})",
                )

            yield SiLABinaryTransfer_pb2.GetChunkResponse(
                binaryTransferUUID=request.binaryTransferUUID,
                offset=request.offset,
                payload=binary[request.offset : request.offset + request.length],
            )

    def DeleteBinary(
        self, request: SiLABinaryTransfer_pb2.DeleteBinaryRequest, context: grpc.ServicerContext
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

    def add_binary(self, binary: bytes) -> uuid.UUID:
        binary_uuid = uuid.uuid4()
        self.binaries[binary_uuid] = binary
        return binary_uuid
