from fa_purity.frozen import (
    FrozenDict,
)
from redshift_client.data_type.core import (
    DataType,
    NonStcDataTypes,
    PrecisionType,
    PrecisionTypes,
    ScaleTypes,
    StaticTypes,
)

STC_ALIAS_MAP: FrozenDict[str, DataType] = FrozenDict(
    {
        "INT2": DataType(StaticTypes.SMALLINT),
        "INT": DataType(StaticTypes.INTEGER),
        "INT4": DataType(StaticTypes.INTEGER),
        "INT8": DataType(StaticTypes.BIGINT),
        "FLOAT4": DataType(StaticTypes.REAL),
        "FLOAT8": DataType(StaticTypes.DOUBLE_PRECISION),
        "FLOAT": DataType(StaticTypes.DOUBLE_PRECISION),
        "BOOL": DataType(StaticTypes.BOOLEAN),
        "BPCHAR": DataType(PrecisionType(PrecisionTypes.CHAR, 256)),
        "TEXT": DataType(PrecisionType(PrecisionTypes.VARCHAR, 256)),
        "TIMESTAMP WITHOUT TIME ZONE": DataType(StaticTypes.TIMESTAMP),
        "TIMESTAMP WITH TIME ZONE": DataType(StaticTypes.TIMESTAMPTZ),
        "TIME WITHOUT TIME ZONE": DataType(StaticTypes.TIME),
        "TIME WITH TIME ZONE": DataType(StaticTypes.TIMETZ),
    }
)

NON_STC_ALIAS_MAP: FrozenDict[str, NonStcDataTypes] = FrozenDict(
    {
        "CHARACTER": NonStcDataTypes(PrecisionTypes.CHAR),
        "NCHAR": NonStcDataTypes(PrecisionTypes.CHAR),
        "CHARACTER VARYING": NonStcDataTypes(PrecisionTypes.VARCHAR),
        "NVARCHAR": NonStcDataTypes(PrecisionTypes.VARCHAR),
        "VARBINARY": NonStcDataTypes(PrecisionTypes.VARBYTE),
        "BINARY VARYING": NonStcDataTypes(PrecisionTypes.VARBYTE),
        "NUMERIC": NonStcDataTypes(ScaleTypes.DECIMAL),
    }
)
