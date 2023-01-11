import decimal
import datetime
from typing import Any, Mapping, Sequence

from sqlalchemy import sql


def sql_type(t):
    return _type_convert[t]


_type_convert = {
    int: sql.sqltypes.Integer,
    str: sql.sqltypes.Unicode,
    float: sql.sqltypes.Float,
    decimal.Decimal: sql.sqltypes.Numeric,
    datetime.datetime: sql.sqltypes.DateTime,
    bytes: sql.sqltypes.LargeBinary,
    bool: sql.sqltypes.Boolean,
    datetime.date: sql.sqltypes.Date,
    datetime.time: sql.sqltypes.Time,
    datetime.timedelta: sql.sqltypes.Interval,
    list: sql.sqltypes.ARRAY,
    dict: sql.sqltypes.JSON
}

_sql_to_python = {
    sql.sqltypes.Integer: int,
    sql.sqltypes.SmallInteger: int,
    sql.sqltypes.SMALLINT: int,
    sql.sqltypes.BigInteger: int,
    sql.sqltypes.BIGINT: int,
    sql.sqltypes.INTEGER: int,
    sql.sqltypes.Unicode: str,
    sql.sqltypes.NVARCHAR: str,
    sql.sqltypes.NCHAR: str,
    sql.sqltypes.Float: decimal.Decimal,
    sql.sqltypes.REAL: decimal.Decimal,
    sql.sqltypes.FLOAT: decimal.Decimal,
    sql.sqltypes.Numeric: decimal.Decimal,
    sql.sqltypes.NUMERIC: decimal.Decimal,
    sql.sqltypes.DECIMAL: decimal.Decimal,
    sql.sqltypes.DateTime: datetime.datetime,
    sql.sqltypes.TIMESTAMP: datetime.datetime,
    sql.sqltypes.DATETIME: datetime.datetime,
    sql.sqltypes.LargeBinary: bytes,
    sql.sqltypes.BLOB: bytes,
    sql.sqltypes.Boolean: bool,
    sql.sqltypes.BOOLEAN: bool,
    sql.sqltypes.MatchType: bool,
    sql.sqltypes.Date: datetime.date,
    sql.sqltypes.DATE: datetime.date,
    sql.sqltypes.Time: datetime.time,
    sql.sqltypes.TIME: datetime.time,
    sql.sqltypes.Interval: datetime.timedelta,
    sql.sqltypes.ARRAY: list,
    sql.sqltypes.JSON: dict
}


def get_sql_types(data: Mapping[str, Sequence]) -> list:
    return [get_sql_type(values) for values in data.values()]


def get_sql_type(values: Sequence) -> Any:
    for python_type in _type_convert:
        if all(type(val) == python_type for val in values):
            return _type_convert[python_type]
    return _type_convert[str]