import logging
import types
from collections import defaultdict
from collections.abc import Iterator
from datetime import datetime
from functools import wraps
from typing import Any, Mapping, NamedTuple, Type, TypeVar, Union

import google.protobuf.message
import grpc
from google.protobuf.message import Message
from grpc import ServicerContext

from sila2_interop_communication_tester.grpc_stubs import SiLAFramework_pb2
from sila2_interop_communication_tester.helpers.fdl_tools import fdl_xmls, xpath_sila
from sila2_interop_communication_tester.helpers.protobuf_helpers import get_message_class, message_to_string

logger = logging.getLogger(__name__)

T = TypeVar("T")  # subclass of Message. `bound=Message` would be correct, but is buggy in mypy


class MetadataDict(Mapping[Type[T], T]):
    def __init__(self, *messages: T) -> None:
        self.__dict: dict[Type[T], T] = {type(message): message for message in messages}

    def __getitem__(self, message_type: Type[T]) -> T:
        return self.__dict[message_type]

    def __len__(self) -> int:
        return len(self.__dict)

    def __iter__(self) -> Iterator[Type[T]]:
        return iter(self.__dict.keys())

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({', '.join(message_to_string(message) for message in self.values())})"

    def __contains__(self, item: Any) -> bool:
        return item in self.__dict


class GrpcStatus(NamedTuple):
    code: grpc.StatusCode
    details: str
    streamed_responses: list[Message]

    def __str__(self) -> str:
        return "".join(
            (
                self.__class__.__name__,
                "(",
                f"code={self.code!r}, ",
                f"details={self.details!r}, ",
                f"streamed_responses={[message_to_string(r) for r in self.streamed_responses]})",
            )
        )


class ServerCall(NamedTuple):
    timestamp: datetime
    request: Union[Message, list[Message]]
    metadata: MetadataDict
    result: Union[Message, GrpcStatus]
    end_timestamp: datetime

    @property
    def successful(self) -> bool:
        return not isinstance(self.result, GrpcStatus) or self.result.code is None

    def __str__(self) -> str:
        # request
        if isinstance(self.request, Message):
            request_string = f"request={message_to_string(self.request)}"
        else:
            request_string = f"requests=[{', '.join(message_to_string(m) for m in self.request)}]"

        # result
        if isinstance(self.result, Message):
            result_string = f"response={message_to_string(self.result)}"
        elif self.result.code is None and self.result.details is None:
            result_string = f"responses=[{', '.join(message_to_string(m) for m in self.result.streamed_responses)}]"
        else:
            result_string = f"error={self.result}"

        return "".join(
            (
                self.__class__.__name__,
                "(",
                f"timestamp={self.timestamp!r}, ",
                f"{request_string}, ",
                f"metadata={self.metadata}, ",
                f"{result_string}, ",
                f"end_timestamp={self.end_timestamp!r}",
                ")",
            )
        )


ARGS_DICT: dict[str, list[ServerCall]] = defaultdict(list)


def spy_servicer(servicer):
    for name in dir(servicer):
        binding = getattr(servicer, name)
        if callable(binding) and name[0].isupper():
            setattr(servicer, name, _spy_method(binding))
    return servicer


def _spy_method(rpc_method):
    @wraps(rpc_method)
    def wrapper(*args):
        timestamp = datetime.now()
        method_name = rpc_method.__qualname__.replace("Impl.", ".").replace("Servicer.", ".")

        request: Union[Message, list[Message]]
        context: ServicerContext
        request, context = args

        if not isinstance(request, Message):
            request = list(request)

        try:
            metadata = extract_metadata(context)
        except google.protobuf.message.DecodeError:
            metadata = MetadataDict(
                SiLAFramework_pb2.SiLAError(
                    frameworkError=SiLAFramework_pb2.FrameworkError(
                        errorType=SiLAFramework_pb2.FrameworkError.INVALID_METADATA,
                        message=f"Received invalid metadata bytes: {list(context.invocation_metadata())}",
                    )
                )
            )

        def stream_request_handler(stream, wrapped_list):
            try:
                for item in stream:
                    wrapped_list.append(item)
                    yield item
            except BaseException as ex:
                if repr(ex) != "Exception()":
                    logger.error(f"Exception while iterating responses for {method_name}: {ex!r}")

            summary = ServerCall(
                timestamp,
                request,
                metadata,
                result=GrpcStatus(context.code(), context.details(), wrapped_list),
                end_timestamp=datetime.now(),
            )
            ARGS_DICT[method_name].append(summary)
            logger.info(f"{method_name} - {summary}")

        response: Union[list, Message, GrpcStatus, None] = None
        try:
            grpc_response = rpc_method(request, context)
            if isinstance(grpc_response, types.GeneratorType):
                response = []
                return stream_request_handler(grpc_response, response)
            else:
                response = grpc_response
                summary = ServerCall(timestamp, request, metadata, result=response, end_timestamp=datetime.now())
                ARGS_DICT[method_name].append(summary)
                logger.info(f"{method_name} - {summary}")
                return grpc_response
        except BaseException:  # server-side errors throw an empty Exception() and modify the context state
            if not isinstance(response, list):
                response = []
            response = GrpcStatus(context.code(), context.details(), response)
            summary = ServerCall(timestamp, request, metadata, result=response, end_timestamp=datetime.now())
            ARGS_DICT[method_name].append(summary)
            logger.info(f"{method_name} - {summary}")
            raise

    return wrapper


def extract_metadata(context: ServicerContext) -> MetadataDict:
    key: str
    value: bytes
    metadata_messages: list[Message] = []
    for key, value in context.invocation_metadata():
        if not key.startswith("sila-"):
            continue
        _, _, _, lowercase_feature_id, _, _, lowercase_metadata_id, _ = key.split("-")
        feature_id, fdl_root = {f: x for (f, x) in fdl_xmls.items() if f.lower() == lowercase_feature_id}.popitem()
        metadata_items: list[str] = xpath_sila(fdl_root, "/sila:Feature/sila:Metadata/sila:Identifier/text()")
        metadata_id = [m for m in metadata_items if m.lower() == lowercase_metadata_id][0]

        message_class = get_message_class(f"{feature_id}.Metadata_{metadata_id}")
        metadata_messages.append(message_class.FromString(value))

    return MetadataDict(*metadata_messages)
