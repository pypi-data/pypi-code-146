# Copyright (c) Huawei Technologies Co., Ltd. 2022. All rights reserved.

from enum import Enum


class FieldType(str, Enum):
    Boolean = 'Boolean',
    Byte = 'Byte',
    Short = 'Short',
    Integer = 'Integer',
    Long = 'Long',
    Float = 'Float',
    Double = 'Double',
    ByteArray = 'ByteArray',
    String = 'String',
    Date = 'Date',
    Text = 'Text',
    IntAutoIncrement = 'IntAutoIncrement',
    LongAutoIncrement = 'LongAutoIncrement'
