#!/usr/bin/env python
#
# Copyright (c) 2022 Katonic Pty Ltd. All rights reserved.
#

from datetime import datetime
from typing import Any, Dict, List

import pyarrow as pa

from katonic.fs.value_type import ValueType


def arrow_to_pg_type(t_str: str) -> str:
    try:
        # issue with timezone timedata in postgres, offline_store_data, entity_data
        if t_str.startswith("timestamp") or t_str.startswith("datetime64"): 
            return "timestamptz" if "tz=" in t_str else "timestamp"
        return {
            "null": "null",
            "bool": "boolean",
            "int8": "tinyint",
            "int16": "smallint",
            "int32": "int",
            "int64": "bigint",
            "list<item: int32>": "int[]",
            "list<item: int64>": "bigint[]",
            "list<item: bool>": "boolean[]",
            "list<item: double>": "double precision[]",
            "uint8": "smallint",
            "uint16": "int",
            "uint32": "bigint",
            "uint64": "bigint",
            "float": "float",
            "float32": "float",
            "float64": "float",
            "double": "double precision",
            "binary": "binary",
            "string": "text",
            "object": "text",
            # "datetime64[ns]": "TIME",
        }[t_str]
    except KeyError:
        raise ValueError(f"Unsupported type: {t_str}")


def pg_type_to_arrow_type(t_str: str) -> str:
    try:
        if t_str.startswith("timestamp"):
            return "timestamptz" if "tz=" in t_str else "timestamp"
        return {
            "null": "null",
            "boolean": "bool",
            "tinyint": "int8",
            "smallint": "int16",
            "int": "int32",
            "bigint": "int64",
            "bigint[]": "list<item: int64>",
            "decimal": "double",
            "float": "float",
            "double": "double",
            "binary": "binary",
            "text": "string",
        }[t_str]
    except KeyError:
        raise ValueError(f"Unsupported type: {t_str}")


def pg_type_to_kfs_value_type(type_str: str) -> ValueType:
    type_map: Dict[str, ValueType] = {
        "boolean": ValueType.BOOL,
        "bytea": ValueType.BYTES,
        "char": ValueType.STRING,
        "bigint": ValueType.INT64,
        "smallint": ValueType.INT32,
        "integer": ValueType.INT32,
        "real": ValueType.DOUBLE,
        "double precision": ValueType.DOUBLE,
        "boolean[]": ValueType.BOOL_LIST,
        "bytea[]": ValueType.BYTES_LIST,
        "char[]": ValueType.STRING_LIST,
        "smallint[]": ValueType.INT32_LIST,
        "integer[]": ValueType.INT32_LIST,
        "text": ValueType.STRING,
        "text[]": ValueType.STRING_LIST,
        "character[]": ValueType.STRING_LIST,
        "bigint[]": ValueType.INT64_LIST,
        "real[]": ValueType.DOUBLE_LIST,
        "double precision[]": ValueType.DOUBLE_LIST,
        "character": ValueType.STRING,
        "character varying": ValueType.STRING,
        "date": ValueType.UNIX_TIMESTAMP,
        "time without time zone": ValueType.UNIX_TIMESTAMP,
        "timestamp without time zone": ValueType.UNIX_TIMESTAMP,
        "timestamp without time zone[]": ValueType.UNIX_TIMESTAMP_LIST,
        "date[]": ValueType.UNIX_TIMESTAMP_LIST,
        "time without time zone[]": ValueType.UNIX_TIMESTAMP_LIST,
        "timestamp with time zone": ValueType.UNIX_TIMESTAMP,
        "timestamp with time zone[]": ValueType.UNIX_TIMESTAMP_LIST,
        "numeric[]": ValueType.DOUBLE_LIST,
        "numeric": ValueType.DOUBLE,
        "uuid": ValueType.STRING,
        "uuid[]": ValueType.STRING_LIST,
    }
    value = type_map.get(type_str.lower(), ValueType.UNKNOWN)
    if value == ValueType.UNKNOWN:
        print("unknown type:", type_str)
    return value


def kfs_value_type_to_pa(kfs_type: ValueType) -> pa.DataType:
    type_map = {
        ValueType.INT32: pa.int32(),
        ValueType.INT64: pa.int64(),
        ValueType.DOUBLE: pa.float64(),
        ValueType.FLOAT: pa.float32(),
        ValueType.STRING: pa.string(),
        ValueType.BYTES: pa.binary(),
        ValueType.BOOL: pa.bool_(),
        ValueType.UNIX_TIMESTAMP: pa.timestamp("us"),
        ValueType.INT32_LIST: pa.list_(pa.int32()),
        ValueType.INT64_LIST: pa.list_(pa.int64()),
        ValueType.DOUBLE_LIST: pa.list_(pa.float64()),
        ValueType.FLOAT_LIST: pa.list_(pa.float32()),
        ValueType.STRING_LIST: pa.list_(pa.string()),
        ValueType.BYTES_LIST: pa.list_(pa.binary()),
        ValueType.BOOL_LIST: pa.list_(pa.bool_()),
        ValueType.UNIX_TIMESTAMP_LIST: pa.list_(pa.timestamp("us")),
        ValueType.NULL: pa.null(),
    }
    return type_map[kfs_type]

def kfs_value_type_to_general_type(kfs_type: ValueType) -> Any:
    type_map = {
        ValueType.INT32: int,
        ValueType.INT64: int,
        ValueType.DOUBLE: float,
        ValueType.FLOAT: float,
        ValueType.STRING: str,
        ValueType.BYTES: bytes,
        ValueType.BOOL: bool,
        ValueType.UNIX_TIMESTAMP: datetime,
        ValueType.INT32_LIST: List[int],
        ValueType.INT64_LIST: List[int],
        ValueType.DOUBLE_LIST: List[float],
        ValueType.FLOAT_LIST: List[float],
        ValueType.STRING_LIST: List[str],
        ValueType.BYTES_LIST: List[bytes],
        ValueType.BOOL_LIST: List[bool],
        ValueType.UNIX_TIMESTAMP_LIST: List[datetime],
        ValueType.NULL: None,
    }
    return type_map[kfs_type]


def pg_type_code_to_pg_type(code: int) -> str:
    return {
        16: "boolean",
        17: "bytea",
        20: "bigint",
        21: "smallint",
        23: "integer",
        25: "text",
        700: "real",
        701: "double precision",
        1000: "boolean[]",
        1001: "bytea[]",
        1005: "smallint[]",
        1007: "integer[]",
        1009: "text[]",
        1014: "character[]",
        1016: "bigint[]",
        1021: "real[]",
        1022: "double precision[]",
        1042: "character",
        1043: "character varying",
        1082: "date",
        1083: "time without time zone",
        1114: "timestamp without time zone",
        1115: "timestamp without time zone[]",
        1182: "date[]",
        1183: "time without time zone[]",
        1184: "timestamp with time zone",
        1185: "timestamp with time zone[]",
        1231: "numeric[]",
        1700: "numeric",
        2950: "uuid",
        2951: "uuid[]",
    }[code]


def pg_type_code_to_arrow(code: int) -> str:
    return kfs_value_type_to_pa(
        pg_type_to_kfs_value_type(pg_type_code_to_pg_type(code))
    )