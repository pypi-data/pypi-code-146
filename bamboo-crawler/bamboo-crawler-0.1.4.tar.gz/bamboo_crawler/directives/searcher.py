from __future__ import annotations

from dataclasses import dataclass
from typing import Any, TypeVar

from ..constants import NullDeserializer, NullSerializer
from ..interfaces.deserializer import Deserializer
from ..interfaces.inputter import Inputter
from ..interfaces.outputter import Outputter
from ..interfaces.processor import Processor
from ..interfaces.serializer import Serializer
from ..task import Task

InputterType = TypeVar("InputterType", bound=type[Inputter])


@dataclass
class DirectiveSearcher:
    deserializers: dict[str, type[Deserializer]]
    inputters: dict[str, type[Inputter]]
    outputters: dict[str, type[Outputter]]
    processors: dict[str, type[Processor]]
    serializers: dict[str, type[Serializer]]

    @classmethod
    def create(cls) -> DirectiveSearcher:
        return cls({}, {}, {}, {}, {})

    def add_inputter(self, inputter: InputterType) -> None:
        self.inputters[inputter.__name__] = inputter

    def add_outputter(self, outputter: type[Outputter]) -> None:
        self.outputters[outputter.__name__] = outputter

    def add_deserializer(self, deserializer: type[Deserializer]) -> None:
        self.deserializers[deserializer.__name__] = deserializer

    def add_processor(self, processor: type[Processor]) -> None:
        self.processors[processor.__name__] = processor

    def add_serializer(self, serializer: type[Serializer]) -> None:
        self.serializers[serializer.__name__] = serializer

    def get_inputter(self, directive: TypeDirective) -> Inputter:
        return self.inputters[directive.type](**directive.options)

    def get_outputter(self, directive: TypeDirective) -> Outputter:
        return self.outputters[directive.type](**directive.options)

    def get_processor(self, directive: TypeDirective) -> Processor:
        return self.processors[directive.type](**directive.options)

    def get_serializer(self, directive: TypeDirective | None) -> Serializer:
        if directive is None:
            return NullSerializer()
        return self.serializers[directive.type](**directive.options)

    def get_deserializer(
        self, directive: TypeDirective | None
    ) -> Deserializer:
        if directive is None:
            return NullDeserializer()
        return self.deserializers[directive.type](**directive.options)

    def define_task(self, name: str, definitions: Any) -> Task:
        task_directive = TaskDirective.from_raw(name, definitions)
        return Task(
            name=task_directive.name,
            inputter=self.get_inputter(task_directive.input),
            processor=self.get_processor(task_directive.process),
            outputter=self.get_outputter(task_directive.output),
            deserializer=self.get_deserializer(task_directive.deserialize),
            serializer=self.get_serializer(task_directive.serialize),
        )


class InvalidDirectiveError(ValueError):
    pass


@dataclass(frozen=True)
class TypeDirective:
    type: str
    options: dict[str, Any]

    @classmethod
    def from_raw(cls, raw_directive: dict[str, Any]) -> TypeDirective:  # type: ignore
        reserved_keywords = ["type", "options"]
        for keyword in raw_directive.keys():
            if keyword not in reserved_keywords:
                raise InvalidDirectiveError(f"Unexpected keyword: {keyword}")

        return cls(
            type=raw_directive["type"],
            options=raw_directive.get("options", {}),
        )


@dataclass(frozen=True)
class TaskDirective:
    name: str
    deserialize: TypeDirective | None
    input: TypeDirective
    output: TypeDirective
    process: TypeDirective
    serialize: TypeDirective | None

    @classmethod
    def from_raw(cls, name: str, raw_directive: dict[str, Any]) -> TaskDirective:  # type: ignore
        reserved_keywords = [
            "input",
            "output",
            "process",
            "deserialize",
            "serialize",
        ]
        for keyword in raw_directive.keys():
            if keyword not in reserved_keywords:
                raise InvalidDirectiveError(f"Unexpected keyword: {keyword}")

        if "deserialize" in raw_directive:
            deserialize = TypeDirective.from_raw(raw_directive["deserialize"])
        else:
            deserialize = None

        if "serialize" in raw_directive:
            serialize = TypeDirective.from_raw(raw_directive["serialize"])
        else:
            serialize = None

        return cls(
            name,
            deserialize=deserialize,
            input=TypeDirective.from_raw(raw_directive["input"]),
            process=TypeDirective.from_raw(raw_directive["process"]),
            output=TypeDirective.from_raw(raw_directive["output"]),
            serialize=serialize,
        )
