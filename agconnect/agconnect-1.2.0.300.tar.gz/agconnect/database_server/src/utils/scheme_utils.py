# Copyright (c) Huawei Technologies Co., Ltd. 2022. All rights reserved.

from __future__ import annotations
from enum import Enum


class FieldType(Enum):
    Boolean = 1,
    Byte = 2,
    Short = 3,
    Integer = 4,
    Long = 5,
    Float = 6,
    Double = 7,
    ByteArray = 8,
    String = 9,
    Date = 10,
    Text = 11,
    UNKNOWN = 12,
    IntAutoIncrement = 13
    LongAutoIncrement = 14

    @staticmethod
    def get_field_type(types: str):
        if types == 'Boolean':
            return FieldType.Boolean
        if types == 'Byte':
            return FieldType.Byte
        if types == 'Short':
            return FieldType.Short
        if types == 'Integer':
            return FieldType.Integer
        if types == 'Long':
            return FieldType.Long
        if types == 'Float':
            return FieldType.Float
        if types == 'Double':
            return FieldType.Double
        if types == 'ByteArray':
            return FieldType.ByteArray
        if types == 'Date':
            return FieldType.Date
        if types == 'Text':
            return FieldType.Text
        if types == 'IntAutoIncrement':
            return FieldType.IntAutoIncrement
        if types == 'LongAutoIncrement':
            return FieldType.LongAutoIncrement
        if types == 'String':
            return FieldType.String
        else:
            return FieldType.UNKNOWN

    @staticmethod
    def value_of(types: FieldType) -> int:
        return types
