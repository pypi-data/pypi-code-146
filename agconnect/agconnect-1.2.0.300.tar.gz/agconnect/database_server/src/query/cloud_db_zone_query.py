# Copyright (c) Huawei Technologies Co., Ltd. 2022. All rights reserved.

from __future__ import annotations

import copy
import math
from typing import TypeVar, Generic, Any, Union, Optional

from agconnect.common_server.src.log_config import logger
from agconnect.database_server.src.exception.agconnect_cloud_db_exception import AGConnectCloudDBException
from agconnect.database_server.src.exception.cloud_db_error_code import CloudDBErrorCode
from agconnect.database_server.src.exception.error_code_message import ErrorCodeMap
from agconnect.database_server.src.utils.condition_type import ConditionType
from agconnect.database_server.src.utils import data_model_helper
from agconnect.database_server.src.utils.field_type import FieldType
from agconnect.database_server.src.utils.utils import Utils

log = logger
T = TypeVar('T')


class CloudDBZoneQuery(Generic[T]):
    __queryConditions: list[Any]
    __encryptedFieldList: list[Any]
    __fieldTypeMap: dict[str, str]
    __clazz: T
    __paginationObject: T | None = None
    __UID_MAX_SIZE = 100

    def __init__(self, clazz):
        self.query_conditions = []
        self.clazz = clazz
        my_object = copy.deepcopy(clazz)
        self.field_type_map = my_object.get_field_type_map()
        self.encrypted_field_list = my_object.get_encrypted_field_list()

    @staticmethod
    def where(clazz: T) -> CloudDBZoneQuery:
        if clazz is None:
            logger.warning(ErrorCodeMap.get(CloudDBErrorCode.QUERY_INPUT_VALUE_IS_NULL))
            raise AGConnectCloudDBException(error_code=CloudDBErrorCode.QUERY_INPUT_VALUE_IS_NULL,
                                            error_message=ErrorCodeMap.get(CloudDBErrorCode.QUERY_INPUT_VALUE_IS_NULL))
        Utils.clazz_check(clazz)
        return CloudDBZoneQuery(clazz)

    def __add_condition(self, condition_type: ConditionType, field_name: str | None, value: Optional[Any] = None) -> \
            None:
        condition_obj: dict[Any] = {"fieldName": field_name, "conditionType": str(condition_type.value), "value": value}
        self.query_conditions.append(condition_obj)

    def __add_pagination_condition(self, condition_type: ConditionType, value: Any) -> None:
        condition_obj: dict[Any] = {"conditionType": str(condition_type.value), "value": value}
        self.query_conditions.append(condition_obj)

    def __add_order_by_condition(self, field_name: str, direction: ConditionType) -> None:
        condition_obj: dict[Any] = {"fieldName": field_name, "conditionType": ConditionType.ORDER_BY.value,
                                    "value": direction.value}
        self.query_conditions.append(condition_obj)

    def equal_to(self, field_name: str, value: Any) -> CloudDBZoneQuery:
        self.__check_field_valid(field_name)
        self.__check_byte_array(field_name)
        self.__check_field_value(field_name, value)
        self.__check_illegal_character(field_name, value)
        self.__add_condition(ConditionType.EQUAL_TO, field_name, value)
        return self

    def not_equal_to(self, field_name: str, value: Any) -> CloudDBZoneQuery:
        self.__check_field_valid(field_name)
        self.__check_byte_array(field_name)
        self.__check_field_value(field_name, value)
        self.__check_illegal_character(field_name, value)
        self.__add_condition(ConditionType.NOT_EQUAL_TO, field_name, value)
        return self

    def greater_than(self, field_name: str, value: Any) -> CloudDBZoneQuery:
        self.__check_field_valid(field_name)
        self.__check_byte_array_and_boolean(field_name)
        self.__check_field_value(field_name, value)
        self.__check_illegal_character(field_name, value)
        self.__add_condition(ConditionType.GREATER_THAN, field_name, value)
        return self

    def greater_than_equal_to(self, field_name: str, value: Any) -> CloudDBZoneQuery:
        self.__check_field_valid(field_name)
        self.__check_byte_array_and_boolean(field_name)
        self.__check_field_value(field_name, value)
        self.__check_illegal_character(field_name, value)
        self.__add_condition(ConditionType.GREATER_THAN_OR_EQUAL_TO, field_name, value)
        return self

    def less_than(self, field_name: str, value: Any) -> CloudDBZoneQuery:
        self.__check_field_valid(field_name)
        self.__check_byte_array_and_boolean(field_name)
        self.__check_field_value(field_name, value)
        self.__check_illegal_character(field_name, value)
        self.__add_condition(ConditionType.LESS_THAN, field_name, value)
        return self

    def less_than_or_equal_to(self, field_name: str, value: Any) -> CloudDBZoneQuery:
        self.__check_field_valid(field_name)
        self.__check_byte_array_and_boolean(field_name)
        self.__check_field_value(field_name, value)
        self.__check_illegal_character(field_name, value)
        self.__add_condition(ConditionType.LESS_THAN_OR_EQUAL_TO, field_name, value)
        return self

    def inside(self, field_name: str, values: Any) -> CloudDBZoneQuery:
        self.__check_field_valid(field_name)
        self.__check_byte_array_and_boolean(field_name)
        self.__check_field_value(field_name, *values)
        for char in values:
            self.__check_illegal_character(field_name, char)
        self.__add_condition(ConditionType.IN, field_name, values)
        return self

    def ends_with(self, field_name: str, value: Any) -> CloudDBZoneQuery:
        self.__check_field_valid(field_name)
        self.__check_string_and_text(field_name)
        self.__check_field_value(field_name, value)
        self.__check_illegal_character(field_name, value)
        self.__add_condition(ConditionType.ENDS_WITH, field_name, value)
        return self

    def begins_with(self, field_name: str, value: Any) -> CloudDBZoneQuery:
        self.__check_field_valid(field_name)
        self.__check_string_and_text(field_name)
        self.__check_field_value(field_name, value)
        self.__check_illegal_character(field_name, value)
        self.__add_condition(ConditionType.BEGINS_WITH, field_name, value)
        return self

    def contains(self, field_name: str, value: Any) -> CloudDBZoneQuery:
        self.__check_field_valid(field_name)
        self.__check_string_and_text(field_name)
        self.__check_field_value(field_name, value)
        self.__check_illegal_character(field_name, value)
        self.__add_condition(ConditionType.CONTAINS, field_name, value)
        return self

    def is_null(self, field_name: str) -> CloudDBZoneQuery:
        self.__check_field_valid(field_name)
        self.__add_condition(ConditionType.IS_NULL, field_name)
        return self

    def is_not_null(self, field_name: str) -> CloudDBZoneQuery:
        self.__check_field_valid(field_name)
        self.__add_condition(ConditionType.IS_NOT_NULL, field_name)
        return self

    def order_by_asc(self, field_name: str) -> CloudDBZoneQuery:
        self.__check_field_valid(field_name)
        self.__add_order_by_condition(field_name, ConditionType.ASCEND)
        return self

    def order_by_desc(self, field_name: str) -> CloudDBZoneQuery:
        self.__check_field_valid(field_name)
        self.__add_order_by_condition(field_name, ConditionType.DESCEND)
        return self

    def limit(self, count: int, offset: Union[None: int] = None) -> CloudDBZoneQuery:
        condition_1 = ((not count or math.isnan(count)) and count != 0)
        condition_2 = (offset and (math.isnan(offset)))

        if condition_1 or condition_2:
            log.warning(ErrorCodeMap.get(CloudDBErrorCode.QUERY_INPUT_VALUE_IS_NULL))
            raise AGConnectCloudDBException(error_code=CloudDBErrorCode.QUERY_INPUT_VALUE_IS_NULL,
                                            error_message=ErrorCodeMap.get(CloudDBErrorCode.QUERY_INPUT_VALUE_IS_NULL))
        if count < 0 or (offset and offset < 0):
            log.warning(ErrorCodeMap.get(CloudDBErrorCode.INPUT_LIMIT_OR_OFFSET_LESS_THAN_ZERO))
            raise AGConnectCloudDBException(error_code=CloudDBErrorCode.INPUT_LIMIT_OR_OFFSET_LESS_THAN_ZERO,
                                            error_message=ErrorCodeMap.get(
                                                CloudDBErrorCode.INPUT_LIMIT_OR_OFFSET_LESS_THAN_ZERO))
        limit_object = {"number": count}
        if offset:
            limit_object["offset"] = offset
        self.query_conditions = list(
            filter(lambda obj: obj.get("conditionType") != ConditionType.LIMIT, self.query_conditions))
        self.__add_condition(ConditionType.LIMIT, None, limit_object)
        return self

    def start_at(self, query_obj: T) -> CloudDBZoneQuery:
        self.__check_object(query_obj)
        Utils.check_illegal_character(query_obj)
        self.__add_pagination_condition(ConditionType.START_AT, query_obj)
        return self

    def start_after(self, query_obj: T) -> CloudDBZoneQuery:
        self.__check_object(query_obj)
        Utils.check_illegal_character(query_obj)
        self.__add_pagination_condition(ConditionType.START_AFTER, query_obj)
        return self

    def end_at(self, query_obj: T) -> CloudDBZoneQuery:
        self.__check_object(query_obj)
        Utils.check_illegal_character(query_obj)
        self.__add_pagination_condition(ConditionType.END_AT, query_obj)
        return self

    def end_before(self, query_obj: T) -> CloudDBZoneQuery:
        self.__check_object(query_obj)
        Utils.check_illegal_character(query_obj)
        self.__add_pagination_condition(ConditionType.END_BEFORE, query_obj)
        return self

    def by_uid(self, uid: str) -> CloudDBZoneQuery:
        if not uid:
            log.warning(ErrorCodeMap.get(CloudDBErrorCode.QUERY_INPUT_VALUE_IS_NULL))
            raise AGConnectCloudDBException(error_code=CloudDBErrorCode.QUERY_INPUT_VALUE_IS_NULL,
                                            error_message=ErrorCodeMap.get(CloudDBErrorCode.QUERY_INPUT_VALUE_IS_NULL))
        if len(uid) > self.__UID_MAX_SIZE:
            log.warning(ErrorCodeMap.get(CloudDBErrorCode.USERID_IS_INVALID))
            raise AGConnectCloudDBException(error_code=CloudDBErrorCode.USERID_IS_INVALID,
                                            error_message=ErrorCodeMap.get(CloudDBErrorCode.USERID_IS_INVALID))
        condition_object: dict[Any] = {"conditionType": ConditionType.UID, "value": uid}
        self.query_conditions.append(condition_object)
        return self

    def get_clazz(self):
        return self.clazz

    def get_query_conditions(self):
        return self.query_conditions

    def __check_field_valid(self, field_name: str) -> None:
        if not field_name:
            log.warning(ErrorCodeMap.get(CloudDBErrorCode.QUERY_INPUT_FIELD_NAME_IS_NULL))
            raise AGConnectCloudDBException(error_code=CloudDBErrorCode.QUERY_INPUT_FIELD_NAME_IS_NULL,
                                            error_message=ErrorCodeMap.get(
                                                CloudDBErrorCode.QUERY_INPUT_FIELD_NAME_IS_NULL))
        if field_name not in self.field_type_map:
            log.warning(ErrorCodeMap.get(CloudDBErrorCode.QUERY_INPUT_FIELD_NAME_DO_NOT_EXIST))
            raise AGConnectCloudDBException(error_code=CloudDBErrorCode.QUERY_INPUT_FIELD_NAME_DO_NOT_EXIST,
                                            error_message=ErrorCodeMap.get(
                                                CloudDBErrorCode.QUERY_INPUT_FIELD_NAME_DO_NOT_EXIST))
        if field_name in self.encrypted_field_list:
            log.warning(ErrorCodeMap.get(CloudDBErrorCode.ENCRYPTED_FIELD_NOT_SUPPORT_QUERY))
            raise AGConnectCloudDBException(error_code=CloudDBErrorCode.ENCRYPTED_FIELD_NOT_SUPPORT_QUERY,
                                            error_message=ErrorCodeMap.get(
                                                CloudDBErrorCode.ENCRYPTED_FIELD_NOT_SUPPORT_QUERY))

    def __check_field_value(self, field_name: str, *values: [Any]) -> None:
        field_type = self.field_type_map.get(field_name)
        if field_type == FieldType.ByteArray:
            log.warning(ErrorCodeMap.get(CloudDBErrorCode.DO_NOT_SUPPORT_BYTEARRAY))
            raise AGConnectCloudDBException(error_code=CloudDBErrorCode.DO_NOT_SUPPORT_BYTEARRAY,
                                            error_message=ErrorCodeMap.get(CloudDBErrorCode.DO_NOT_SUPPORT_BYTEARRAY))
        for value in values:
            if value is None:
                log.warning(ErrorCodeMap.get(CloudDBErrorCode.QUERY_INPUT_VALUE_IS_NULL))
                raise AGConnectCloudDBException(error_code=CloudDBErrorCode.QUERY_INPUT_VALUE_IS_NULL,
                                                error_message=ErrorCodeMap.get(
                                                    CloudDBErrorCode.QUERY_INPUT_VALUE_IS_NULL))
            if not data_model_helper.DataModelHelper.validate_query_field_value(field_type, value):
                log.warning(ErrorCodeMap.get(CloudDBErrorCode.ERROR_CODE_DATA_INVALID))
                raise AGConnectCloudDBException(error_code=CloudDBErrorCode.ERROR_CODE_DATA_INVALID,
                                                error_message=ErrorCodeMap.get(
                                                    CloudDBErrorCode.ERROR_CODE_DATA_INVALID))

    def __check_object(self, query_object: T) -> None:
        if not query_object:
            log.warning(ErrorCodeMap.get(CloudDBErrorCode.QUERY_INPUT_QUERY_OBJECT_IS_NULL))
            raise AGConnectCloudDBException(error_code=CloudDBErrorCode.QUERY_INPUT_QUERY_OBJECT_IS_NULL,
                                            error_message=ErrorCodeMap.get(
                                                CloudDBErrorCode.QUERY_INPUT_QUERY_OBJECT_IS_NULL))
        if not data_model_helper.DataModelHelper.validate(query_object, True):
            log.warning(ErrorCodeMap.get(CloudDBErrorCode.ERROR_CODE_DATA_INVALID))
            raise AGConnectCloudDBException(error_code=CloudDBErrorCode.ERROR_CODE_DATA_INVALID,
                                            error_message=ErrorCodeMap.get(CloudDBErrorCode.ERROR_CODE_DATA_INVALID))
        if self.__paginationObject:
            log.warning(ErrorCodeMap.get(CloudDBErrorCode.PAGINATE_QUERY_INPUT_IS_MORE_THAN_ONE))
            raise AGConnectCloudDBException(error_code=CloudDBErrorCode.PAGINATE_QUERY_INPUT_IS_MORE_THAN_ONE,
                                            error_message=ErrorCodeMap.get(
                                                CloudDBErrorCode.PAGINATE_QUERY_INPUT_IS_MORE_THAN_ONE))
        self.__paginationObject = query_object

    def __check_byte_array(self, field_name: str) -> None:
        if self.field_type_map.get(field_name) == FieldType.ByteArray:
            log.warning(ErrorCodeMap.get(CloudDBErrorCode.DO_NOT_SUPPORT_BYTEARRAY))
            raise AGConnectCloudDBException(error_code=CloudDBErrorCode.DO_NOT_SUPPORT_BYTEARRAY,
                                            error_message=ErrorCodeMap.get(CloudDBErrorCode.DO_NOT_SUPPORT_BYTEARRAY))

    def __check_byte_array_and_boolean(self, field_name: str) -> None:
        field_type = self.field_type_map.get(field_name)
        if field_type == FieldType.Boolean or field_type == FieldType.ByteArray:
            log.warning(ErrorCodeMap.get(CloudDBErrorCode.DO_NOT_SUPPORT_BYTEARRAY_OR_BOOLEAN))
            raise AGConnectCloudDBException(error_code=CloudDBErrorCode.DO_NOT_SUPPORT_BYTEARRAY_OR_BOOLEAN,
                                            error_message=ErrorCodeMap.get(
                                                CloudDBErrorCode.DO_NOT_SUPPORT_BYTEARRAY_OR_BOOLEAN))

    def __check_string_and_text(self, field_name: str) -> None:
        field_type = self.field_type_map.get(field_name)
        if field_type != FieldType.Text.name and field_type != FieldType.String.name:
            log.warning(ErrorCodeMap.get(CloudDBErrorCode.ONLY_SUPPORT_TEXT_AND_STRING))
            raise AGConnectCloudDBException(error_code=CloudDBErrorCode.ONLY_SUPPORT_TEXT_AND_STRING,
                                            error_message=ErrorCodeMap.get(
                                                CloudDBErrorCode.ONLY_SUPPORT_TEXT_AND_STRING))

    def __check_illegal_character(self, field_name: str, value: any):
        field_type = self.field_type_map.get(field_name)
        if field_type == FieldType.Text.value or field_type == FieldType.String.value:
            if value is None:
                return
            try:
                value.index("\0")
                log.warning(ErrorCodeMap.get(CloudDBErrorCode.INPUT_CONTAIN_ILLEGAL_CHARACTER))
                raise AGConnectCloudDBException(error_code=CloudDBErrorCode.INPUT_CONTAIN_ILLEGAL_CHARACTER,
                                                error_message=ErrorCodeMap.get(
                                                    CloudDBErrorCode.INPUT_CONTAIN_ILLEGAL_CHARACTER))
            except ValueError:
                pass
