# Copyright (c) Huawei Technologies Co., Ltd. 2022. All rights reserved.

from typing import TypeVar, Generic, Type, Any

from agconnect.database_server.src.exception.error_code_message import ErrorCodeMap
from agconnect.database_server.src.utils import data_model_helper
from agconnect.database_server.src.utils.condition_type import ConditionType
from agconnect.database_server.src.exception.agconnect_cloud_db_exception import AGConnectCloudDBException
from agconnect.database_server.src.exception.cloud_db_error_code import CloudDBErrorCode
from agconnect.database_server.src.utils.field_type import FieldType
from agconnect.common_server.src.log_config.common_log import logger
import math

T = TypeVar('T')


class ConditionValidate(Generic[T]):
    __MAX_CONDITION = 30
    __NEED_TO_CHECK_FIELD_NAME = [
        ConditionType.BEGINS_WITH, ConditionType.ENDS_WITH, ConditionType.CONTAINS, ConditionType.EQUAL_TO,
        ConditionType.NOT_EQUAL_TO, ConditionType.GREATER_THAN, ConditionType.GREATER_THAN_OR_EQUAL_TO,
        ConditionType.LESS_THAN, ConditionType.LESS_THAN_OR_EQUAL_TO, ConditionType.IN,
        ConditionType.IS_NULL, ConditionType.IS_NOT_NULL, ConditionType.ORDER_BY, ConditionType.LIMIT,
        ConditionType.ASCEND, ConditionType.DESCEND, ConditionType.START_AT, ConditionType.START_AFTER,
        ConditionType.END_AT, ConditionType.END_BEFORE, ConditionType.UID
    ]

    @staticmethod
    def __empty_fn(condition):
        pass

    __UID_MAX_SIZE = 100
    __clazz: Type[T]

    def __init__(self, clazz: Type[T]):
        self.__clazz = clazz
        obj = clazz()
        self.field_type_map = obj.get_field_type_map()
        self.encryptedFieldList = obj.get_encrypted_field_list()
        self.__condition_validators = dict()
        self.__condition_validators[ConditionType.BEGINS_WITH.value] = self.validate_begin_end_contains
        self.__condition_validators[ConditionType.ENDS_WITH.value] = self.validate_begin_end_contains
        self.__condition_validators[ConditionType.CONTAINS.value] = self.validate_begin_end_contains
        self.__condition_validators[ConditionType.EQUAL_TO.value] = self.validate_equal_or_not_equal
        self.__condition_validators[ConditionType.NOT_EQUAL_TO.value] = self.validate_equal_or_not_equal
        self.__condition_validators[ConditionType.GREATER_THAN.value] = self.validate_greater_or_less_than
        self.__condition_validators[ConditionType.GREATER_THAN_OR_EQUAL_TO.value] = self.validate_greater_or_less_than
        self.__condition_validators[ConditionType.LESS_THAN.value] = self.validate_greater_or_less_than
        self.__condition_validators[ConditionType.LESS_THAN_OR_EQUAL_TO.value] = self.validate_greater_or_less_than
        self.__condition_validators[ConditionType.IN.value] = self.validate_in
        self.__condition_validators[ConditionType.IS_NULL.value] = self.__empty_fn
        self.__condition_validators[ConditionType.IS_NOT_NULL.value] = self.__empty_fn
        self.__condition_validators[ConditionType.ORDER_BY.value] = self.__empty_fn
        self.__condition_validators[ConditionType.LIMIT.value] = self.validate_limit
        self.__condition_validators[ConditionType.START_AT.value] = self.validate_tuple
        self.__condition_validators[ConditionType.START_AFTER.value] = self.validate_tuple
        self.__condition_validators[ConditionType.END_AT.value] = self.validate_tuple
        self.__condition_validators[ConditionType.END_BEFORE.value] = self.validate_tuple
        self.__condition_validators[ConditionType.UID.value] = self.validate_uid

    def check_condition(self, condition: Any):
        if not condition:
            logger.warning(CloudDBErrorCode.INVALID_CONDITION)
            raise AGConnectCloudDBException(error_code=CloudDBErrorCode.INVALID_CONDITION,
                                            error_message=ErrorCodeMap.get(
                                                CloudDBErrorCode.INVALID_CONDITION))
        condition_type = (
            condition.get("conditionType").value
            if isinstance(condition.get("conditionType"), ConditionType)
            else condition.get("conditionType")
        )
        if condition_type in self.__NEED_TO_CHECK_FIELD_NAME:
            self.check_field_name(condition.get('fieldName'))
        condition_validator = self.__condition_validators.get(condition_type)
        if not condition_validator:
            logger.warning(CloudDBErrorCode.INVALID_CONDITION)
            raise AGConnectCloudDBException(error_code=CloudDBErrorCode.INVALID_CONDITION,
                                            error_message=ErrorCodeMap.get(
                                                CloudDBErrorCode.INVALID_CONDITION))
        if condition_validator:
            condition_validator(condition)

    @staticmethod
    def check_condition_len(conditions):
        if len(conditions) > ConditionValidate.__MAX_CONDITION:
            logger.warning(CloudDBErrorCode.CONDITION_EXCEEDS_LIMIT)
            raise AGConnectCloudDBException(error_code=CloudDBErrorCode.CONDITION_EXCEEDS_LIMIT,
                                            error_message=ErrorCodeMap.get(
                                                CloudDBErrorCode.CONDITION_EXCEEDS_LIMIT))

    def validate_equal_or_not_equal(self, condition: {Any}):
        field_name = condition.get('fieldName')
        value = condition.get('value')
        if self.field_type_map.get(field_name) is FieldType.ByteArray:
            logger.warning(CloudDBErrorCode.DO_NOT_SUPPORT_BYTEARRAY)
            raise AGConnectCloudDBException(error_code=CloudDBErrorCode.DO_NOT_SUPPORT_BYTEARRAY,
                                            error_message=ErrorCodeMap.get(
                                                CloudDBErrorCode.DO_NOT_SUPPORT_BYTEARRAY))
        self.check_field_value(field_name, value)
        self.check_illegal_character(field_name, value)

    def validate_begin_end_contains(self, condition: {Any}):
        field_name = condition.get('fieldName')
        value = condition.get('value')
        self.check_string_and_text(field_name)
        self.check_field_value(field_name, value)
        self.check_illegal_character(field_name, value)

    def validate_greater_or_less_than(self, condition: {Any}):
        field_name = condition.get('fieldName')
        value = condition.get('value')
        self.check_byte_array_and_boolean(field_name)
        self.check_field_value(field_name, value)
        self.check_illegal_character(field_name, value)

    def validate_in(self, condition: {Any}):
        field_name = condition.get('fieldName')
        values = condition.get('value')
        self.check_byte_array_and_boolean(field_name)
        self.check_field_value(field_name, *values)
        for value, _index in enumerate(values):
            self.check_illegal_character(field_name, value)

    @staticmethod
    def validate_limit(condition: {Any}):
        limit_object = condition.get('value')
        count = limit_object.get["number"]
        offset = limit_object.get["offset"]
        if not count and count != 0:
            logger.warning(CloudDBErrorCode.QUERY_INPUT_VALUE_IS_NULL)
            raise AGConnectCloudDBException(error_code=CloudDBErrorCode.QUERY_INPUT_VALUE_IS_NULL,
                                            error_message=ErrorCodeMap.get(
                                                CloudDBErrorCode.QUERY_INPUT_VALUE_IS_NULL))
        elif offset is None:
            logger.warning(CloudDBErrorCode.QUERY_INPUT_VALUE_IS_NULL)
            raise AGConnectCloudDBException(error_code=CloudDBErrorCode.QUERY_INPUT_VALUE_IS_NULL,
                                            error_message=ErrorCodeMap.get(
                                                CloudDBErrorCode.QUERY_INPUT_VALUE_IS_NULL))
        elif offset is not None and math.isnan(offset):
            logger.warning(CloudDBErrorCode.QUERY_INPUT_VALUE_IS_NULL)
            raise AGConnectCloudDBException(error_code=CloudDBErrorCode.QUERY_INPUT_VALUE_IS_NULL,
                                            error_message=ErrorCodeMap.get(
                                                CloudDBErrorCode.QUERY_INPUT_VALUE_IS_NULL))
        if count < 0 or (offset is not None and offset < 0):
            logger.warning(CloudDBErrorCode.INPUT_LIMIT_OR_OFFSET_LESS_THAN_ZERO)
            raise AGConnectCloudDBException(error_code=CloudDBErrorCode.INPUT_LIMIT_OR_OFFSET_LESS_THAN_ZERO,
                                            error_message=ErrorCodeMap.get(
                                                CloudDBErrorCode.INPUT_LIMIT_OR_OFFSET_LESS_THAN_ZERO))

    @staticmethod
    def validate_tuple(condition: {Any}):
        query_object = condition.get('value')
        if not query_object:
            logger.warning(CloudDBErrorCode.QUERY_INPUT_QUERY_OBJECT_IS_NULL)
            raise AGConnectCloudDBException(error_code=CloudDBErrorCode.QUERY_INPUT_QUERY_OBJECT_IS_NULL,
                                            error_message=ErrorCodeMap.get(
                                                CloudDBErrorCode.QUERY_INPUT_QUERY_OBJECT_IS_NULL))

        if not data_model_helper.DataModelHelper.validate(query_object, True):
            logger.warning(CloudDBErrorCode.ERROR_CODE_DATA_INVALID)
            raise AGConnectCloudDBException(error_code=CloudDBErrorCode.ERROR_CODE_DATA_INVALID,
                                            error_message=ErrorCodeMap.get(
                                                CloudDBErrorCode.ERROR_CODE_DATA_INVALID))

    @staticmethod
    def validate_uid(condition: {Any}):
        uid = condition.get('value')
        if not uid:
            logger.warning(CloudDBErrorCode.QUERY_INPUT_QUERY_OBJECT_IS_NULL)
            raise AGConnectCloudDBException(error_code=CloudDBErrorCode.QUERY_INPUT_QUERY_OBJECT_IS_NULL,
                                            error_message=ErrorCodeMap.get(
                                                CloudDBErrorCode.QUERY_INPUT_QUERY_OBJECT_IS_NULL))
        if len(uid) > ConditionValidate.__UID_MAX_SIZE:
            logger.warning(CloudDBErrorCode.USERID_IS_INVALID)
            raise AGConnectCloudDBException(error_code=CloudDBErrorCode.USERID_IS_INVALID,
                                            error_message=ErrorCodeMap.get(
                                                CloudDBErrorCode.USERID_IS_INVALID))

    def check_string_and_text(self, field_name):
        field_type = self.field_type_map.get(field_name)
        if field_type != FieldType.String.name and field_type != FieldType.Text.name:
            logger.warning(CloudDBErrorCode.ONLY_SUPPORT_TEXT_AND_STRING)
            raise AGConnectCloudDBException(error_code=CloudDBErrorCode.ONLY_SUPPORT_TEXT_AND_STRING,
                                            error_message=ErrorCodeMap.get(
                                                CloudDBErrorCode.ONLY_SUPPORT_TEXT_AND_STRING))

    def check_byte_array_and_boolean(self, field_name):
        field_type = self.field_type_map.get(field_name)
        if field_type == FieldType.Boolean.name or field_type == FieldType.ByteArray.name:
            logger.warning(CloudDBErrorCode.DO_NOT_SUPPORT_BYTEARRAY_OR_BOOLEAN)
            raise AGConnectCloudDBException(error_code=CloudDBErrorCode.DO_NOT_SUPPORT_BYTEARRAY_OR_BOOLEAN,
                                            error_message=ErrorCodeMap.get(
                                                CloudDBErrorCode.DO_NOT_SUPPORT_BYTEARRAY_OR_BOOLEAN))

    def check_field_name(self, field_name):
        if not field_name:
            logger.warning(CloudDBErrorCode.QUERY_INPUT_FIELD_NAME_IS_NULL)
            raise AGConnectCloudDBException(error_code=CloudDBErrorCode.QUERY_INPUT_FIELD_NAME_IS_NULL,
                                            error_message=ErrorCodeMap.get(
                                                CloudDBErrorCode.QUERY_INPUT_FIELD_NAME_IS_NULL))
        if field_name not in self.field_type_map:
            logger.warning(CloudDBErrorCode.QUERY_INPUT_FIELD_NAME_DO_NOT_EXIST)
            raise AGConnectCloudDBException(error_code=CloudDBErrorCode.QUERY_INPUT_FIELD_NAME_DO_NOT_EXIST,
                                            error_message=ErrorCodeMap.get(
                                                CloudDBErrorCode.QUERY_INPUT_FIELD_NAME_DO_NOT_EXIST))
        if field_name in self.encryptedFieldList:
            logger.warning(CloudDBErrorCode.ENCRYPTED_FIELD_NOT_SUPPORT_QUERY)
            raise AGConnectCloudDBException(error_code=CloudDBErrorCode.ENCRYPTED_FIELD_NOT_SUPPORT_QUERY,
                                            error_message=ErrorCodeMap.get(
                                                CloudDBErrorCode.ENCRYPTED_FIELD_NOT_SUPPORT_QUERY))

    def check_field_value(self, field_name, *values):
        field_type = self.field_type_map.get(field_name)
        if field_type == FieldType.ByteArray.name:
            logger.warning(CloudDBErrorCode.DO_NOT_SUPPORT_BYTEARRAY)
            raise AGConnectCloudDBException(error_code=CloudDBErrorCode.DO_NOT_SUPPORT_BYTEARRAY,
                                            error_message=ErrorCodeMap.get(
                                                CloudDBErrorCode.DO_NOT_SUPPORT_BYTEARRAY))
        for value in values:
            if value is None:
                logger.warning(CloudDBErrorCode.QUERY_INPUT_VALUE_IS_NULL)
                raise AGConnectCloudDBException(error_code=CloudDBErrorCode.QUERY_INPUT_VALUE_IS_NULL,
                                                error_message=ErrorCodeMap.get(
                                                    CloudDBErrorCode.QUERY_INPUT_VALUE_IS_NULL))
            if not data_model_helper.DataModelHelper.validate_query_field_value(field_type, value):
                logger.warning(CloudDBErrorCode.ERROR_CODE_DATA_INVALID)
                raise AGConnectCloudDBException(error_code=CloudDBErrorCode.ERROR_CODE_DATA_INVALID,
                                                error_message=ErrorCodeMap.get(
                                                    CloudDBErrorCode.ERROR_CODE_DATA_INVALID))

    def check_object_illegal_character(self, obj):
        field_type_map = obj.get_field_type_map()
        for key, _value in field_type_map:
            self.check_illegal_character(key, obj[key])
        pass

    def check_illegal_character(self, field_name: str, value):
        field_type = self.field_type_map.get(field_name)
        if field_type == FieldType.Text or field_type == FieldType.String:
            if value is None:
                return
            illegal_char = '\\0'
            if illegal_char in str(value):
                logger.warning(CloudDBErrorCode.INPUT_CONTAIN_ILLEGAL_CHARACTER)
                raise AGConnectCloudDBException(error_code=CloudDBErrorCode.INPUT_CONTAIN_ILLEGAL_CHARACTER,
                                                error_message=ErrorCodeMap.get(
                                                    CloudDBErrorCode.INPUT_CONTAIN_ILLEGAL_CHARACTER))
