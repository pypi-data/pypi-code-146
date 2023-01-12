from __future__ import annotations

import threading
import time
from typing import TYPE_CHECKING, TypeVar

from google.protobuf.message import Message

from sila2_interop_communication_tester.helpers.fdl_tools import get_fully_qualified_identifier

if TYPE_CHECKING:
    from grpc import CallIterator

T = TypeVar("T")


def collect_from_stream(stream: CallIterator[T], timeout: float = 1) -> list[T]:
    """Collect all items from a gRPC stream until the timeout expires"""
    # `list(stream)` finishes when the stream finishes, but cancelled streams cannot be iterated further,
    # so we call `list(stream)`, start the timer, and cancel it from a separate thread
    def cancel_after_timeout():
        time.sleep(timeout)
        stream.cancel()

    threading.Thread(target=cancel_after_timeout).start()
    return list(stream)


def pack_metadata(*messages: Message) -> tuple[tuple[str, bytes], ...]:
    metadata_tuples = []
    for message in messages:
        message_name = message.__class__.__name__.removeprefix("Metadata_")
        feature_fqi = get_fully_qualified_identifier(message.__module__.removesuffix("_pb2")).fully_qualified_identifier
        metadata_fqi = "/".join((feature_fqi, "Metadata", message_name))
        key = f"sila-{metadata_fqi.replace('/', '-').lower()}-bin"
        value = message.SerializeToString()
        metadata_tuples.append((key, value))

    return tuple(metadata_tuples)
