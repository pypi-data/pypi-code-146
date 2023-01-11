# ref https://docs.aws.amazon.com/redshift/latest/dg/c_Supported_data_types.html

from dataclasses import (
    dataclass,
)
from enum import (
    Enum,
)
from typing import (
    Union,
)


class StaticTypes(Enum):
    SMALLINT = "SMALLINT"
    INTEGER = "INTEGER"
    BIGINT = "BIGINT"
    REAL = "REAL"
    DOUBLE_PRECISION = "DOUBLE PRECISION"
    BOOLEAN = "BOOLEAN"
    DATE = "DATE"
    TIMESTAMP = "TIMESTAMP"
    TIMESTAMPTZ = "TIMESTAMPTZ"
    TIME = "TIME"
    TIMETZ = "TIMETZ"
    GEOMETRY = "GEOMETRY"
    GEOGRAPHY = "GEOGRAPHY"
    HLLSKETCH = "HLLSKETCH"
    SUPER = "SUPER"


class PrecisionTypes(Enum):
    CHAR = "CHAR"
    VARCHAR = "VARCHAR"
    VARBYTE = "VARBYTE"


class ScaleTypes(Enum):
    DECIMAL = "DECIMAL"


@dataclass(frozen=True)
class NonStcDataTypes:
    value: Union[PrecisionTypes, ScaleTypes]


@dataclass(frozen=True)
class PrecisionType:
    data_type: PrecisionTypes
    precision: int


@dataclass(frozen=True)
class DecimalType:
    precision: int
    scale: int


@dataclass(frozen=True)
class DataType:
    value: Union[StaticTypes, PrecisionType, DecimalType]
