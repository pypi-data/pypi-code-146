#!/usr/bin/env python
#
# Copyright (c) 2022 Katonic Pty Ltd. All rights reserved.
#

import enum


class ValueType(enum.Enum):
    """
    Feature value type. Used to define data types in Feature Tables.
    """

    UNKNOWN = 0
    BYTES = 1
    STRING = 2
    INT32 = 3
    INT64 = 4
    DOUBLE = 5
    FLOAT = 6
    BOOL = 7
    UNIX_TIMESTAMP = 8
    BYTES_LIST = 11
    STRING_LIST = 12
    INT32_LIST = 13
    INT64_LIST = 14
    DOUBLE_LIST = 15
    FLOAT_LIST = 16
    BOOL_LIST = 17
    UNIX_TIMESTAMP_LIST = 18
    NULL = 19

    def to_tfx_schema_feature_type(self):
        if self.value in [
            ValueType.BYTES.value,
            ValueType.STRING.value,
            ValueType.BOOL.value,
            ValueType.BYTES_LIST.value,
            ValueType.STRING_LIST.value,
            ValueType.INT32_LIST.value,
            ValueType.INT64_LIST.value,
            ValueType.DOUBLE_LIST.value,
            ValueType.FLOAT_LIST.value,
            ValueType.BOOL_LIST.value,
            ValueType.UNIX_TIMESTAMP_LIST.value,
        ]:
            return bytes
        elif self.value in [
            ValueType.INT32.value,
            ValueType.INT64.value,
            ValueType.UNIX_TIMESTAMP.value,
        ]:
            return int
        elif self.value in [ValueType.DOUBLE.value, ValueType.FLOAT.value]:
            return float
        else:
            return TypeError