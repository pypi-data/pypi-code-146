from dataclasses import (
    dataclass,
)


@dataclass(frozen=True)
class SchemaId:
    name: str


@dataclass(frozen=True)
class TableId:
    schema: SchemaId
    name: str
