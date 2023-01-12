# Copyright (c) Huawei Technologies Co., Ltd. 2022. All rights reserved.

from __future__ import annotations

import json
from enum import Enum
from typing import Any, Type, TypeVar

from agconnect.common_server.src.log_config import logger
from agconnect.database_server.src.exception.agconnect_cloud_db_exception import AGConnectCloudDBException
from agconnect.database_server.src.exception.cloud_db_error_code import CloudDBErrorCode
from agconnect.database_server.src.exception.error_code_message import ErrorCodeMap
from agconnect.database_server.src.query import cloud_db_zone_query
from agconnect.database_server.src.services import cloud_db_zone
from agconnect.database_server.src.utils.utils import Utils

T = TypeVar('T')

MAX_QUERY_OBJECT_NUM = 1000
MAX_QUERY_OBJECT_LIST_CAPACITY = 20 * 1024 * 1024
KEY_NATURAL_BASE_VERSION = 'naturalbase_version'


class TransactionFunction:
    async def apply(self, transaction: Transaction = None) -> bool:
        pass


class OperationType(str, Enum):
    UPSERT = 'Upsert',
    DELETE = 'Delete'


operation = {
    'operationType': OperationType,
    "objectTypeName": str,
    "objects": [Any]
}

verify_object = {
    'objectTypeName': str,
    "objects": [Any]
}

verify_map_object = {
    'operationType': str,
    "objectTypeName": Any,
    "objects": [Any]
}


class Transaction:
    need_verify_objects_list: [Any] = []
    transaction_list: [operation] = []
    __cloud_db_zone: cloud_db_zone.CloudDBZone
    __need_verify_object_map: [str, verify_map_object] = {}
    __need_verify_data_num = 0
    __query_data_length = 0

    def __init__(self, cloud_db_zone_obj: cloud_db_zone.CloudDBZone):
        self.__cloud_db_zone = cloud_db_zone_obj

    async def execute_query(self, cloud_db_zone_query_obj: cloud_db_zone_query.CloudDBZoneQuery) -> T:
        if not cloud_db_zone_query_obj or type(cloud_db_zone_query_obj) == float:
            logger.warning(ErrorCodeMap.get(CloudDBErrorCode.VALUE_IS_NULL))
            raise AGConnectCloudDBException(error_code=CloudDBErrorCode.VALUE_IS_NULL,
                                            error_message=ErrorCodeMap.get(CloudDBErrorCode.VALUE_IS_NULL))
        if len(self.transaction_list) > 0:
            logger.warning(ErrorCodeMap.get(CloudDBErrorCode.ERROR_CODE_TRANSACTION_SEQUENCE_INCORRECT))
            raise AGConnectCloudDBException(error_code=CloudDBErrorCode.ERROR_CODE_TRANSACTION_SEQUENCE_INCORRECT,
                                            error_message=ErrorCodeMap.get(
                                                CloudDBErrorCode.ERROR_CODE_TRANSACTION_SEQUENCE_INCORRECT))
        object_data = await self.__cloud_db_zone.execute_transaction_query(cloud_db_zone_query_obj, False)
        self.check_query_data(object_data)
        clazz = cloud_db_zone_query_obj.get_clazz()
        my_obj = clazz()
        verify_objects = Transaction.get_version_data(object_data, my_obj.get_primary_key_list())
        if my_obj.get_class_name() in self.__need_verify_object_map:
            concat_arr = self.__need_verify_object_map.get(my_obj.get_class_name()).get("objects") + verify_objects
            self.__need_verify_object_map.get(my_obj.get_class_name())["objects"] = concat_arr
        else:
            need_verify_object: verify_map_object = {
                "ObjectTypeName": my_obj.get_class_name(),
                "clazz": my_obj,
                "objects": verify_objects
            }
            res = my_obj.get_class_name()
            self.__need_verify_object_map[res] = need_verify_object
        field_type_map = my_obj.get_field_type_map()
        deserialize_objects = Utils.deserialize_objects(object_data, field_type_map, clazz)
        for obj in deserialize_objects:
            try:
                if isinstance(obj.ByteArrayT, str):
                    obj.ByteArrayT = bytearray(obj.ByteArrayT, 'UTF-8')
            except Exception:
                logger.info('str type ByteArrayT variable conversion failed')
        return deserialize_objects

    def execute_upsert(self, object_list: [Type[T]]) -> Transaction:
        Transaction.check_input_data(object_list)
        if len(object_list) == 0:
            return self
        Utils.check_schema_data_size(object_list)
        self.transaction_list.append(self.form_transaction_data(object_list, OperationType.UPSERT))
        return self

    def execute_delete(self, object_list: [Type[T]]) -> Transaction:
        Transaction.check_input_data(object_list)
        if len(object_list) == 0:
            return self
        Utils.check_schema_data_size(object_list)
        self.transaction_list.append(self.form_transaction_data(object_list, OperationType.DELETE))
        return self

    @staticmethod
    def check_input_data(object_list: [Type[T]]):
        if not object_list or isinstance(object_list, float):
            logger.warning(ErrorCodeMap.get(CloudDBErrorCode.VALUE_IS_NULL))
            raise AGConnectCloudDBException(error_code=CloudDBErrorCode.VALUE_IS_NULL,
                                            error_message=ErrorCodeMap.get(
                                                CloudDBErrorCode.VALUE_IS_NULL))
        if not Utils.is_array(object_list):
            logger.warning(ErrorCodeMap.get(CloudDBErrorCode.PARAMETER_INVALID))
            raise AGConnectCloudDBException(error_code=CloudDBErrorCode.PARAMETER_INVALID,
                                            error_message=ErrorCodeMap.get(
                                                CloudDBErrorCode.PARAMETER_INVALID))
        for i, _ in enumerate(object_list):
            if object_list[i] is None:
                logger.warning(ErrorCodeMap.get(CloudDBErrorCode.VALUE_IS_NULL))
                raise AGConnectCloudDBException(error_code=CloudDBErrorCode.VALUE_IS_NULL,
                                                error_message=ErrorCodeMap.get(
                                                    CloudDBErrorCode.VALUE_IS_NULL))

    @staticmethod
    def form_transaction_data(object_list: [Any], operation_type: OperationType) -> operation:
        return {
            "operationType": operation_type.value,
            "objectTypeName": object_list[0].get_class_name(),
            "objects": Utils.serialize_objects(object_list)
        }

    def release(self):
        self.need_verify_objects_list: []
        self.transaction_list = []
        __need_verify_object_map: [str, verify_map_object] = {}
        self.__need_verify_data_num = 0
        self.__query_data_length = 0

    def is_transaction_empty(self) -> bool:
        is_empty = True
        for ob in self.transaction_list:
            if len(ob['objects']) > 0:
                is_empty = False
                break
        return is_empty

    def sort_verify_object_list(self):
        converted_list: [verify_object] = list(self.__need_verify_object_map.values())
        for i in converted_list:
            for element in i['objects']:
                pr_key = list(element.keys())[0]
            i['objects'] = sorted(i['objects'], key=lambda d: d[pr_key])
        for value in converted_list:
            self.need_verify_objects_list.append({
                "objectTypeName": value.get("ObjectTypeName"),
                "objects": value.get("objects")
            })

    @staticmethod
    def get_version_data(object_data: Any, primary_key_list: [Any]) -> [Any]:
        array_data: [Any] = []
        for data in object_data:
            obj: Any = {}
            for primary_key in primary_key_list:
                value = data.get(primary_key)
                if value is None:
                    logger.warning("the primaryKey data is null")
                    raise AGConnectCloudDBException(error_code=CloudDBErrorCode.PARAMETER_INVALID,
                                                    error_message=ErrorCodeMap.get(
                                                        CloudDBErrorCode.PARAMETER_INVALID))
                obj[primary_key] = value
            version = data[KEY_NATURAL_BASE_VERSION]
            if not version:
                logger.warning('the version data is null')
                raise AGConnectCloudDBException(error_code=CloudDBErrorCode.PARAMETER_INVALID,
                                                error_message=ErrorCodeMap.get(
                                                    CloudDBErrorCode.PARAMETER_INVALID))
            obj[KEY_NATURAL_BASE_VERSION] = version
            array_data.append(obj)
        return array_data

    def check_query_data(self, object_data: Any):
        if not object_data:
            logger.warning(ErrorCodeMap.get(CloudDBErrorCode.FAIL_TO_PARSE_QUERY_DATA))
            raise AGConnectCloudDBException(error_code=CloudDBErrorCode.FAIL_TO_PARSE_QUERY_DATA,
                                            error_message=ErrorCodeMap.get(
                                                CloudDBErrorCode.FAIL_TO_PARSE_QUERY_DATA))
        if len(object_data) > MAX_QUERY_OBJECT_NUM:
            logger.warning(ErrorCodeMap.get(CloudDBErrorCode.ERROR_QUERY_DATA_COUNT_TOO_LARGE))
            raise AGConnectCloudDBException(error_code=CloudDBErrorCode.ERROR_QUERY_DATA_COUNT_TOO_LARGE,
                                            error_message=ErrorCodeMap.get(
                                                CloudDBErrorCode.ERROR_QUERY_DATA_COUNT_TOO_LARGE))
        self.__need_verify_data_num += len(object_data)
        if self.__need_verify_data_num > MAX_QUERY_OBJECT_NUM:
            logger.warning(ErrorCodeMap.get(CloudDBErrorCode.ERROR_QUERY_DATA_COUNT_TOO_LARGE))
            raise AGConnectCloudDBException(error_code=CloudDBErrorCode.ERROR_QUERY_DATA_COUNT_TOO_LARGE,
                                            error_message=ErrorCodeMap.get(
                                                CloudDBErrorCode.ERROR_QUERY_DATA_COUNT_TOO_LARGE))
        self.__query_data_length += len(json.dumps(object_data, separators=(',', ':')))
        if self.__query_data_length > MAX_QUERY_OBJECT_LIST_CAPACITY:
            logger.warning(ErrorCodeMap.get(CloudDBErrorCode.ERROR_QUERY_DATA_SIZE_TOO_LARGE))
            raise AGConnectCloudDBException(error_code=CloudDBErrorCode.ERROR_QUERY_DATA_SIZE_TOO_LARGE,
                                            error_message=ErrorCodeMap.get(
                                                CloudDBErrorCode.ERROR_QUERY_DATA_SIZE_TOO_LARGE))
