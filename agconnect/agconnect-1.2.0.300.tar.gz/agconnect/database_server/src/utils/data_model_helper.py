# Copyright (c) Huawei Technologies Co., Ltd. 2022. All rights reserved.

import io
import math
from datetime import datetime
from typing import Any, Callable

from agconnect.common_server.src.log_config import logger
from agconnect.database_server.src.exception.agconnect_cloud_db_exception import AGConnectCloudDBException
from agconnect.database_server.src.exception.cloud_db_error_code import CloudDBErrorCode
from agconnect.database_server.src.exception.error_code_message import ErrorCodeMap
from agconnect.database_server.src.utils.scheme_utils import FieldType
from agconnect.database_server.src.utils import utils

CalculatorFn = Callable[[Any], int]
ValidatorFn = Callable[[Any], bool]

INTEGER_MIN_VALUE = -2147483648
INTEGER_MAX_VALUE = 2147483647
AUTO_INT_MIN_VALUE = 1
AUTO_INT_MAX_VALUE = 2147483647
SHORT_MIN_VALUE = -32768
SHORT_MAX_VALUE = 32767
BYTE_MIN_VALUE = -128
BYTE_MAX_VALUE = 127
FLOAT_MIN_VALUE = (-3.402823e+38)
FLOAT_MAX_VALUE = 3.402823e+38
DOUBLE_MIN_VALUE = (-3.402823e+46)
DOUBLE_MAX_VALUE = 3.402823e+46
LONG_MIN_VALUE = "-9223372036854775808"
LONG_MAX_VALUE = "9223372036854775807"
AUTO_LONG_MIN_VALUE = '1'
AUTO_LONG_MAX_VALUE = '1'
INCREMENT_SUPPORT_FIELD_TYPE = [
    'Byte',
    'Short',
    'Integer',
    'Long',
    'Float',
    'Double',
    'IntAutoIncrement',
    'LongAutoIncrement'
]
MAX_STRING_LENGTH = 200
calculators: [int, CalculatorFn] = {}


def add_calculator(data_type: FieldType, func: CalculatorFn):
    calculators[data_type] = func


def calculator_text_func(text):
    if isinstance(text, str):
        calculate_string_utf8_length(text)
    elif isinstance(text, io.BytesIO):
        calculate_string_utf8_length(text.getvalue().decode('utf-8'))


add_calculator(FieldType.Integer, lambda _: 4)
add_calculator(FieldType.IntAutoIncrement, lambda _: 4)
add_calculator(FieldType.String, lambda value: calculate_string_utf8_length(value))
add_calculator(FieldType.Short, lambda _: 2)
add_calculator(FieldType.Long, lambda _: 8)
add_calculator(FieldType.LongAutoIncrement, lambda _: 8)
add_calculator(FieldType.Boolean, lambda _: 1)
add_calculator(FieldType.Byte, lambda _: 1)
add_calculator(FieldType.Float, lambda _: 4)
add_calculator(FieldType.Double, lambda _: 8)
add_calculator(FieldType.ByteArray, lambda value: len(value) if value and isinstance(value, bytearray) else 0)
add_calculator(FieldType.Date, lambda _: 8)
add_calculator(FieldType.Text,
               lambda text: calculate_string_utf8_length(text.getvalue().decode('utf-8'))
               if text and isinstance(text, io.BytesIO) else calculate_string_utf8_length(text))

validators: [int, ValidatorFn] = {}


def is_number(obj):
    check_obj_is_nan = math.isnan(obj)
    if isinstance(obj, (int, float)) and not check_obj_is_nan:
        return True
    else:
        return False


def add_validator(data_type: FieldType, func: ValidatorFn):
    validators[data_type] = func


add_validator(
    FieldType.Byte,
    lambda value: True
    if (type(value) == bytes or type(value) == int) and -math.pow(2, 53) < value < math.pow(2, 53)
       and BYTE_MIN_VALUE <= value <= BYTE_MAX_VALUE
    else False,
)

add_validator(
    FieldType.Short,
    lambda value: True
    if type(value) == int and -math.pow(2, 53) < value < math.pow(2, 53)
       and SHORT_MIN_VALUE <= value <= SHORT_MAX_VALUE
    else False,
)

add_validator(
    FieldType.Integer,
    lambda value: True
    if type(value) == int and INTEGER_MAX_VALUE >= value >= INTEGER_MIN_VALUE
    else False,
)

add_validator(
    FieldType.IntAutoIncrement,
    lambda value: True
    if isinstance(value, int) or (AUTO_INT_MIN_VALUE < value or value < AUTO_INT_MAX_VALUE)
    else False,
)

add_validator(
    FieldType.Long,
    lambda value: True
    if (type(value) == int or (type(value) == str)) and utils.Utils.long_compare_to(
        value, LONG_MIN_VALUE) >= 0 >= utils.Utils.long_compare_to(value, LONG_MAX_VALUE) else False,
)

add_validator(
    FieldType.LongAutoIncrement,
    lambda value: True
    if type(value) == int == (type(value) is str) and (
            utils.Utils.long_compare_to(str(
                value), AUTO_LONG_MIN_VALUE) >= 0) and (
               utils.Utils.long_compare_to(str(value), AUTO_LONG_MAX_VALUE) <= 0) else False, )

add_validator(
    FieldType.Float,
    lambda value: True
    if value is not None and type(
        value) is float and FLOAT_MIN_VALUE <= value <= FLOAT_MAX_VALUE and is_number(value) else False)

add_validator(
    FieldType.Double,
    lambda value: True
    if value is not None and type(
        value) is float and DOUBLE_MIN_VALUE <= value <= DOUBLE_MAX_VALUE
    else False
)
add_validator(
    FieldType.String,
    lambda value: True
    if isinstance(value, str) and len(value) <= MAX_STRING_LENGTH
    else False,
)
add_validator(FieldType.Text, lambda value: True if isinstance(value, str) or isinstance(value, io.BytesIO) else False)
add_validator(
    FieldType.Boolean, lambda value: True if isinstance(value, bool) else False
)
add_validator(FieldType.ByteArray, lambda value: True if isinstance(value, bytearray) else False)
add_validator(
    FieldType.Date,
    lambda value: True
    if isinstance(value, datetime) and not math.isnan(
        value.timestamp())
    else False,
)
add_validator(FieldType.UNKNOWN, lambda: False)


def calculate_string_utf8_length(c_str: str):
    if c_str:
        return len(c_str.encode('utf-8'))
    return 0


class DataModelHelper:
    @staticmethod
    def calculate_object(obj: Any) -> int:
        if not utils.Utils.is_not_null_object(obj):
            raise TypeError("object is not valid data model object")
        field_type_map = obj.get_field_type_map()
        properties = obj.__dict__
        memory_size = 0
        for key in properties:
            field_type = FieldType.get_field_type(field_type_map.get(key))
            size = calculators.get(field_type)(obj.__dict__.get(key)) if calculators.get(field_type) else len(
                "" + str(obj.__dict__.get(key)))
            memory_size += size
        for key in field_type_map.keys():
            field_type = FieldType.get_field_type(field_type_map.get(key))
            if key in properties or not calculators.get(field_type):
                continue
            if field_type == FieldType.Text.name \
                    or field_type == FieldType.String.name:
                continue
            elif field_type == FieldType.ByteArray.name:
                continue
            size = calculators.get(field_type)(None)
            memory_size += size
        return memory_size

    @staticmethod
    def validate(obj: Any, is_query=None):
        if not utils.Utils.is_not_null_object(obj):
            raise TypeError("'object is not valid data model object!'")
        properties = obj.__dict__
        field_type_map = obj.get_field_type_map()
        if utils.Utils.is_null_object(properties) or utils.Utils.is_null_object(field_type_map):
            return False
        for name in properties:
            type_str = field_type_map.get(name)
            if not type_str:
                return False
            value = obj.__dict__.get(name)
            if value is None:
                continue
            if is_query:
                if not DataModelHelper.validate_query_field_value(type_str, value):
                    return False
                continue
            if not DataModelHelper.validate_field_value(type_str, value):
                return False
        return True

    @staticmethod
    def validate_field_value(field_type: Any, value: Any) -> bool:
        if field_type == 'ByteArray' and isinstance(value, str):
            print('byte array str')
        if FieldType.get_field_type(field_type) == FieldType.UNKNOWN.value:
            logger.warning(ErrorCodeMap.get([CloudDBErrorCode.INVALID_FIELD_TYPE]))
            raise AGConnectCloudDBException(error_code=CloudDBErrorCode.INVALID_FIELD_TYPE,
                                            error_message=ErrorCodeMap.get(
                                                CloudDBErrorCode.INVALID_FIELD_TYPE))
        return validators.get(FieldType.get_field_type(field_type))(value)

    @staticmethod
    def validate_query_field_value(field_type: Any, value: Any) -> bool:
        if FieldType.get_field_type(field_type) == FieldType.IntAutoIncrement:
            field_type = "Integer"
        if FieldType.get_field_type(field_type) == FieldType.LongAutoIncrement:
            field_type = "Long"
        return DataModelHelper.validate_field_value(field_type, value)

    @staticmethod
    def check_primary_keys(obj: Any):
        primary_keys = obj.get_primary_key_list()
        field_type_map = obj.get_field_type_map()
        if not primary_keys or len(primary_keys) == 0:
            raise TypeError('There is at least one primary key.')
        for primary_key in primary_keys:
            entity_class_variables = [attr for attr in dir(obj) if
                                      not callable(getattr(obj, attr)) and not attr.startswith("__")]
            if primary_key not in entity_class_variables or obj.get_id() is None:
                logger.warning(ErrorCodeMap.get(CloudDBErrorCode.PRIMARY_KEY_REQUIRED))
                raise AGConnectCloudDBException(error_code=CloudDBErrorCode.PRIMARY_KEY_REQUIRED,
                                                error_message=ErrorCodeMap.get(
                                                    CloudDBErrorCode.PRIMARY_KEY_REQUIRED))
            if not DataModelHelper.validate_field_value(field_type_map.get(primary_key), getattr(obj, primary_key)):
                logger.warning(ErrorCodeMap.get(CloudDBErrorCode.ERROR_CODE_DATA_INVALID))
                raise AGConnectCloudDBException(error_code=CloudDBErrorCode.ERROR_CODE_DATA_INVALID,
                                                error_message=ErrorCodeMap.get(
                                                    CloudDBErrorCode.
                                                    ERROR_CODE_DATA_INVALID))

    @staticmethod
    def check_operator_field(field_name: Any, value: Any, obj: Any, is_increment: bool = False):
        field_type_map = obj.get_field_type_map()
        encrypted_fields = obj.get_encrypted_field_list()
        primary_keys = obj.get_primary_key_list()
        if field_name not in field_type_map:
            logger.warning(ErrorCodeMap.get(CloudDBErrorCode.FIELD_NOT_EXIST))
            raise AGConnectCloudDBException(error_code=CloudDBErrorCode.FIELD_NOT_EXIST,
                                            error_message=ErrorCodeMap.get(CloudDBErrorCode.FIELD_NOT_EXIST))
        if field_name in primary_keys or field_name in encrypted_fields:
            logger.warning(ErrorCodeMap.get(CloudDBErrorCode.PRIMARY_KEY_ENCRYPTED_FIELD_CANNOT_BE_UPDATED))
            raise AGConnectCloudDBException(error_code=CloudDBErrorCode.PRIMARY_KEY_ENCRYPTED_FIELD_CANNOT_BE_UPDATED,
                                            error_message=ErrorCodeMap.get(
                                                CloudDBErrorCode.PRIMARY_KEY_ENCRYPTED_FIELD_CANNOT_BE_UPDATED))
        field_type = field_type_map.get(field_name)
        if not field_type:
            logger.warning(ErrorCodeMap.get(CloudDBErrorCode.INVALID_FIELD_TYPE))
            raise AGConnectCloudDBException(error_code=CloudDBErrorCode.INVALID_FIELD_TYPE,
                                            error_message=ErrorCodeMap.get(CloudDBErrorCode.INVALID_FIELD_TYPE))
        if is_increment and field_type not in INCREMENT_SUPPORT_FIELD_TYPE:
            logger.warning(ErrorCodeMap.get(CloudDBErrorCode.INCREMENTAL_FIELD_ONLY_SUPPORT_NUMERIC))
            raise AGConnectCloudDBException(error_code=CloudDBErrorCode.INCREMENTAL_FIELD_ONLY_SUPPORT_NUMERIC,
                                            error_message=ErrorCodeMap.get(
                                                CloudDBErrorCode.INCREMENTAL_FIELD_ONLY_SUPPORT_NUMERIC))
        if not is_increment and value is None:
            return
        if not DataModelHelper.validate_field_value(field_type, value):
            logger.warning(ErrorCodeMap.get(CloudDBErrorCode.ERROR_CODE_DATA_INVALID))
            raise AGConnectCloudDBException(error_code=CloudDBErrorCode.ERROR_CODE_DATA_INVALID,
                                            error_message=ErrorCodeMap.get(
                                                CloudDBErrorCode.ERROR_CODE_DATA_INVALID))
