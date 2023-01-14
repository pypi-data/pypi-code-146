import inspect
from typing import Any, Callable, List, Optional, Type, TypeVar, Union

from pydantic import BaseModel
from typing_extensions import ParamSpec

from chalk.state import KeyedState
from chalk.streams._file_source import FileSource
from chalk.streams._kafka_source import KafkaSource
from chalk.streams._windows import Windowed, get_duration_secs, get_name_with_duration, windowed
from chalk.streams.base import StreamSource
from chalk.utils import MachineType

__all__ = [
    "FileSource",
    "KafkaSource",
    "KeyedState",
    "StreamSource",
    "Windowed",
    "stream",
    "windowed",
    "get_name_with_duration",
    "get_duration_secs",
]

P = ParamSpec("P")
T = TypeVar("T")

MessageType = TypeVar("MessageType", bound=BaseModel)


def stream(
    *,
    source: StreamSource,
    mode: Optional[str] = None,
    environment: Optional[Union[List[str], str]] = None,
    machine_type: Optional[MachineType] = None,
    message: Optional[Type[Any]] = None,
) -> Callable[[Callable[P, T]], Callable[P, T]]:
    caller_frame = inspect.stack()[1]
    caller_filename = caller_frame.filename
    caller_globals = caller_frame.frame.f_globals
    caller_locals = caller_frame.frame.f_locals
    from chalk.features.resolver import parse_and_register_stream_resolver

    def decorator(fn: Callable[P, T]) -> Callable[P, T]:
        return parse_and_register_stream_resolver(
            caller_globals=caller_globals,
            caller_locals=caller_locals,
            fn=fn,
            source=source,
            mode=mode,
            caller_filename=caller_filename,
            environment=environment,
            machine_type=machine_type,
            message=message,
        )

    return decorator
