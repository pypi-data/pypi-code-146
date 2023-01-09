from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, Optional, TypeVar

from ..interfaces.context import Context
from ..interfaces.deserializer import Deserializer
from ..interfaces.inputter import Inputter
from ..interfaces.processor import Processor
from ..interfaces.serializer import Serializer

T = TypeVar("T")


@dataclass
class ConstantInputter(Inputter[T]):
    value: T
    metadata: Dict[str, Any] = field(default_factory=dict)

    def read(self) -> Context[T]:
        return Context(self.value, **self.metadata)


class NullDeserializer(Deserializer[T, T]):
    def deserialize(self, value: T) -> T:
        return value


class NullSerializer(Serializer[T, T]):
    def serialize(self, value: T) -> T:
        return value


class NullProcessor(Processor[T, T]):
    def process(
        self, data: T, *, context: Optional[Context[T]] = None
    ) -> Iterable[T]:
        yield data
