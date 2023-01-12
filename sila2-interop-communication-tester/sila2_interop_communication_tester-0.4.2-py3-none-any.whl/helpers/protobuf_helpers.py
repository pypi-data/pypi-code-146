import sys
from importlib import import_module
from pathlib import Path
from typing import Type

from google.protobuf.message import Message
from google.protobuf.text_format import MessageToString

import sila2_interop_communication_tester

pb2_dir = Path(sila2_interop_communication_tester.__file__).parent / "grpc_stubs"
pb2_files: dict[str, Path] = {f.name.removeprefix("_pb2.py"): f.absolute() for f in pb2_dir.glob("*_pb2.py")}


def get_message_class(message_id: str) -> Type[Message]:
    """Call with parameters like 'SiLAFramework.Integer' or SiLABinaryTransfer.GetBinaryInfoRequest"""
    proto_name, message_name = message_id.split(".")
    sys.path.append(str(pb2_dir.absolute()))
    try:
        proto_module = import_module(
            f".{proto_name}_pb2", package=sila2_interop_communication_tester.grpc_stubs.__name__
        )
        return getattr(proto_module, message_name)
    finally:
        sys.path.pop()


def message_to_string(message: Message) -> str:
    body = MessageToString(message, as_one_line=True, use_index_order=True)
    if len(body) > 1000:
        body = body[:100] + f"[[omitted {len(body) - 200} chars]]" + body[-100:]
    return message.__class__.__qualname__ + "(" + body + ")"
