from __future__ import annotations

import uuid
from dataclasses import dataclass
from typing import TYPE_CHECKING, Optional

import grpc

from sila2_interop_communication_tester.grpc_stubs import SiLAFramework_pb2
from sila2_interop_communication_tester.helpers.utils import string_is_uuid
from sila2_interop_communication_tester.test_server.helpers.raise_error import raise_validation_error

if TYPE_CHECKING:
    from sila2_interop_communication_tester.test_server.server_implementation.binary_download import BinaryDownloadImpl
    from sila2_interop_communication_tester.test_server.server_implementation.binary_upload import BinaryUploadImpl


@dataclass
class BinaryTransferHelper:
    uploader: Optional[BinaryUploadImpl] = None
    downloader: Optional[BinaryDownloadImpl] = None


HELPER = BinaryTransferHelper()


def get_binary(
    binary_message: SiLAFramework_pb2.Binary, parameter_identifier: str, context: grpc.ServicerContext
) -> bytes:
    if binary_message.WhichOneof("union") is None:
        raise_validation_error(context, parameter_identifier, "Received empty SiLAFramework.Binary message")

    if binary_message.HasField("value"):
        return binary_message.value
    else:
        if not string_is_uuid(binary_message.binaryTransferUUID):
            raise_validation_error(
                context, parameter_identifier, f"Not a valid UUID: {binary_message.binaryTransferUUID}"
            )

        try:
            return HELPER.uploader.get_binary(uuid.UUID(binary_message.binaryTransferUUID))
        except BaseException:
            raise_validation_error(
                context, parameter_identifier, f"Failed to get binary with UUID {binary_message.binaryTransferUUID}"
            )


def pack_binary(binary: bytes) -> SiLAFramework_pb2.Binary:
    if len(binary) < 2 * 1024**2:
        return SiLAFramework_pb2.Binary(value=binary)
    return SiLAFramework_pb2.Binary(binaryTransferUUID=str(HELPER.downloader.add_binary(binary)))
