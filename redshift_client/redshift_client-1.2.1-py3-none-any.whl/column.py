from dataclasses import (
    dataclass,
)
from redshift_client.data_type.core import (
    DataType,
)
from redshift_client.sql_client import (
    PrimitiveVal,
)


@dataclass(frozen=True)
class ColumnId:
    name: str


@dataclass(frozen=True)
class Column:
    data_type: DataType
    nullable: bool
    default: PrimitiveVal


@dataclass(frozen=True)
class ColumnObj:
    id_obj: ColumnId
    column: Column
