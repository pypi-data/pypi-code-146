# Copyright (c) Huawei Technologies Co., Ltd. 2022. All rights reserved.

import base64
import copy
import math
from datetime import datetime
from typing import Any, Union, Dict, Type
import re
import uuid as uuid

from agconnect.common_server.src.log_config import logger
from agconnect.database_server.src.exception.agconnect_cloud_db_exception import AGConnectCloudDBException
from agconnect.database_server.src.exception.cloud_db_error_code import CloudDBErrorCode
from agconnect.database_server.src.exception.error_code_message import ErrorCodeMap
from agconnect.database_server.src.utils.aggregare_type import AggregateType
from agconnect.database_server.src.utils.condition_type import ConditionType
from agconnect.database_server.src.utils import data_model_helper
from agconnect.database_server.src.utils.field_type import FieldType


class Utils:
    __DATE_REG_EXP = r"^[1-9]\d{3}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}\s\d{3}"
    __NUMBER_REG_EXP = r"^(-)?(0|[1-9][0-9]*)$"
    __MAX_OBJECT_CAPACITY = 2 * 1024 * 1024
    __KEY_DELETE_TIME = "delete#time"

    @staticmethod
    def is_array(value: Any) -> bool:
        if isinstance(value, list) and not value:
            return isinstance(value, list)
        else:
            return isinstance(value, list)

    @staticmethod
    def is_null_object(value: Any) -> bool:
        if value is None:
            return True
        else:
            return False

    @staticmethod
    def is_not_null_object(value: Any) -> bool:
        return value

    @staticmethod
    def serialize_objects(objects: [Any]) -> [Any]:
        formatted_data: [Any] = []
        for element in objects:
            obj = Utils.serialize_object(element)
            formatted_data.append(obj)
        return formatted_data

    @staticmethod
    def to_timestamp(dt):
        return round(dt.timestamp() * 1000)

    @staticmethod
    def __serialize_date(date_time: datetime) -> Union[int, datetime]:
        if type(date_time) is not datetime:
            return date_time
        return Utils.to_timestamp(date_time)

    @staticmethod
    def deserialize_objects(objects: [Any], field_type_map: Dict[str, str],
                            target_class: Any) -> [Any]:
        formatted_data: Any = []
        for element in objects:
            const_object = target_class()
            for key in field_type_map.keys():
                if element.get(key) is None or key in const_object.get_encrypted_field_list():
                    setattr(const_object, key, None)
                    continue
                if element.get(key) is None:
                    setattr(const_object, key, None)
                    continue
                field_type = field_type_map.get(key)
                if field_type is FieldType.Date.value:
                    setattr(const_object, key, Utils.deserialize_date(element.get(key)))
                    continue
                if Utils.is_field_type_number(field_type):
                    setattr(const_object, key, Utils.deserialize_number(element.get(key)))
                    continue
                if type(field_type) is FieldType.ByteArray:
                    setattr(const_object, key, Utils.base64_to_array_buffer(element.get(key)))
                    continue
                setattr(const_object, key, element.get(key))
            formatted_data.append(const_object)
        return formatted_data

    @staticmethod
    def array_buffer_to_base64(array_buffer: Any) -> Any:
        base64_encoded_str = base64.b64encode(array_buffer).decode('utf-8')
        return base64_encoded_str

    @staticmethod
    def base64_to_array_buffer(my_str_encoded: str):
        my_str_decoded = base64.b64decode(my_str_encoded).decode('utf-8')
        buffer = copy.deepcopy(my_str_decoded)
        return buffer

    @staticmethod
    def is_field_type_number(field_type: Any) -> bool:
        if not field_type:
            raise AGConnectCloudDBException(error_code=CloudDBErrorCode.PARAMETER_INVALID,
                                            error_message=ErrorCodeMap.get(CloudDBErrorCode.PARAMETER_INVALID))
        if (
                field_type == FieldType.Byte.name
                or field_type == FieldType.Double.name
                or field_type == FieldType.Integer.name
        ):
            return True
        elif field_type == FieldType.IntAutoIncrement.name or field_type == FieldType.Float.name \
                or field_type == FieldType.Short.name:
            return True
        else:
            return False

    @staticmethod
    def deserialize_number(data: Any):
        if type(data) is str:
            try:
                data = int(data)
            except ValueError:
                return float(data)
            return data
        else:
            return data

    @staticmethod
    def deserialize_date(data: str) -> datetime:
        if not re.search(Utils.__DATE_REG_EXP, data):
            logger.warning(f'The date string from cloud is invalid: {data}')
            raise AGConnectCloudDBException(error_code=CloudDBErrorCode.DATE_STRING_INVALID,
                                            error_message=ErrorCodeMap.get(CloudDBErrorCode.DATE_STRING_INVALID))
        utc_date_string: str = data.replace(' ', 'T', 1).replace(' ', '.', 1) + 'Z'
        return datetime.strptime(utc_date_string, "%Y-%m-%dT%H:%M:%S.%fZ")

    @staticmethod
    def add_condition(condition_type: ConditionType, field_name: Union[str, None], field_type: Union[Any, None],
                      value: Any = None) -> Any:
        condition_object: Type[Dict[Any]] = Dict[Any]
        condition_object[field_name] = field_name
        condition_object[field_type] = field_type
        condition_object[condition_type] = condition_type
        condition_object[value] = value
        return condition_object

    @staticmethod
    def serialize_query_conditions(query_conditions: [Any], field_type_map: Dict[str, str],
                                   begin: datetime = None, end: datetime = None) -> [Any]:
        formatted_condition: [Any] = []
        condition_copy: Dict[Any]
        for query_condition in query_conditions:
            query_condition["conditionType"] = query_condition.get("conditionType")
            condition_copy = query_condition.copy()
            if Utils.is_pagination_type(query_condition.get('conditionType')):
                if not Utils.is_object_valid(query_condition.get('value')):
                    logger.warning(ErrorCodeMap.get(CloudDBErrorCode.OBJECT_IS_INVALID))
                    raise AGConnectCloudDBException(error_code=CloudDBErrorCode.OBJECT_IS_INVALID,
                                                    error_message=ErrorCodeMap.get(CloudDBErrorCode.OBJECT_IS_INVALID))
                condition_copy['value'] = Utils.serialize_object(query_condition.get('value'))
                formatted_condition.append(condition_copy)
                continue
            if field_type_map.get(query_condition.get('fieldName')) is FieldType.Date.value and \
                    query_condition.get('conditionType') is ConditionType.IN.value:
                for i in range(0, len(query_condition)):
                    condition_copy['value'][i] = Utils.__serialize_date(query_condition.get('value')[i])
            else:
                condition_copy["value"] = Utils.__serialize_date(query_condition.get('value'))
            formatted_condition.append(condition_copy)
        if begin and end:
            begin_time_range_condition: Any = Utils.add_condition(
                ConditionType.GREATER_THAN_OR_EQUAL_TO, Utils.__KEY_DELETE_TIME,
                FieldType.Long, Utils.__serialize_date(begin))
            formatted_condition.append(begin_time_range_condition)
            end_time_range_condition: Any = Utils.add_condition(ConditionType.LESS_THAN_OR_EQUAL_TO,
                                                                Utils.__KEY_DELETE_TIME, FieldType.Long,
                                                                Utils.__serialize_date(end))
            formatted_condition.append(end_time_range_condition)
        return formatted_condition

    @staticmethod
    def is_numeric_field(field_type: str) -> bool:
        if field_type is str(FieldType.Byte.name) or field_type is str(FieldType.Double.name) or \
                field_type is str(FieldType.Integer.name):
            return True
        elif field_type is str(FieldType.IntAutoIncrement.name) or field_type is str(FieldType.Float.name):
            return True
        elif field_type is str(FieldType.Short.name) or field_type is str(FieldType.Long.name):
            return True
        elif field_type is str(FieldType.LongAutoIncrement.name):
            return True
        else:
            return False

    @staticmethod
    def clazz_check(clazz: Any):
        obj = clazz()
        if not Utils.is_object_valid(obj):
            raise AGConnectCloudDBException(error_code=CloudDBErrorCode.CLASS_INVALID,
                                            error_message=ErrorCodeMap.get(CloudDBErrorCode.CLASS_INVALID))

    @staticmethod
    def is_object_valid(obj: Any) -> bool:
        condition_1 = hasattr(obj, "get_field_type_map") and hasattr(obj, "get_class_name")
        condition_2 = hasattr(obj, "get_encrypted_field_list") and hasattr(obj, "get_primary_key_list")
        condition_3 = hasattr(obj, "get_index_list")
        if condition_1 and condition_2 and condition_3:
            return True
        else:
            return False

    @staticmethod
    def serialize_object(element: Any) -> Any:
        obj = {}
        field_type_map = element.get_field_type_map()
        encrypted_field_list = element.get_encrypted_field_list()
        for key in element.__dict__.keys():
            if element.__dict__.get(key) is None or key in encrypted_field_list:
                continue
            if element.__dict__.get(key) is None:
                obj[key] = None
                continue
            field_type = field_type_map.get(key)
            if Utils.is_numeric_field(field_type) and not math.isfinite(int(element.__dict__.get(key))):
                raise AGConnectCloudDBException(error_code=CloudDBErrorCode.NUMBER_IS_INVALID,
                                                error_message=ErrorCodeMap.get(CloudDBErrorCode.NUMBER_IS_INVALID))

            if field_type_map.get(key) is FieldType.Date.name:
                obj[key] = Utils.__serialize_date(element.__dict__.get(key))
                continue
            if field_type is FieldType.ByteArray.name:
                if type(element.__dict__.get(key)) == str:
                    byte_array_element_key = bytearray(element.__dict__.get(key), 'UTF-8')
                    obj[key] = Utils.array_buffer_to_base64(byte_array_element_key)
                    continue
                obj[key] = Utils.array_buffer_to_base64(element.__dict__.get(key))
                continue
            obj[key] = element.__dict__.get(key)
        return obj

    @staticmethod
    def is_aggregate_type(condition_type: str) -> bool:
        array = [AggregateType.AVG, AggregateType.COUNT, AggregateType.MAX,
                 AggregateType.MIN, AggregateType.SUM]
        return True if condition_type in array else False

    @staticmethod
    def is_pagination_type(condition_type: str) -> bool:
        array = [ConditionType.START_AT, ConditionType.START_AFTER, ConditionType.END_AT,
                 ConditionType.END_BEFORE]
        return True if condition_type in array else False

    @staticmethod
    def check_schema_data_size(object_list: [Any]):
        class_name: str = ""
        for element in object_list:
            if not Utils.is_object_valid(element):
                logger.warning(ErrorCodeMap.get(CloudDBErrorCode.OBJECT_IS_INVALID))
                raise AGConnectCloudDBException(error_code=CloudDBErrorCode.OBJECT_IS_INVALID,
                                                error_message=ErrorCodeMap.get(CloudDBErrorCode.OBJECT_IS_INVALID))
            if not data_model_helper.DataModelHelper.validate(element):
                logger.warning(ErrorCodeMap.get(CloudDBErrorCode.ERROR_CODE_DATA_INVALID))
                raise AGConnectCloudDBException(error_code=CloudDBErrorCode.ERROR_CODE_DATA_INVALID,
                                                error_message=ErrorCodeMap.get(CloudDBErrorCode.
                                                                               ERROR_CODE_DATA_INVALID))
            if class_name == "":
                class_name = element.get_class_name()
            if class_name is not element.get_class_name():
                logger.warning(ErrorCodeMap.get(CloudDBErrorCode.ONLY_SUPPORT_ONE_SCHEMA))
                raise AGConnectCloudDBException(error_code=CloudDBErrorCode.ONLY_SUPPORT_ONE_SCHEMA,
                                                error_message=ErrorCodeMap.get(CloudDBErrorCode.
                                                                               ONLY_SUPPORT_ONE_SCHEMA))
            object_list_size = data_model_helper.DataModelHelper.calculate_object(element)
            if object_list_size > Utils.__MAX_OBJECT_CAPACITY:
                logger.warning(ErrorCodeMap.get(CloudDBErrorCode.DATA_SIZE_IS_OVERFLOW))
                raise AGConnectCloudDBException(error_code=CloudDBErrorCode.DATA_SIZE_IS_OVERFLOW,
                                                error_message=ErrorCodeMap.get(CloudDBErrorCode.
                                                                               DATA_SIZE_IS_OVERFLOW))

    @staticmethod
    def check_illegal_character(obj: Any):
        field_type_map = obj.get_field_type_map()
        for key in field_type_map.keys():
            if field_type_map.get(key) == "String" or field_type_map.get(key) == 'Text':
                value: str = obj.__dict__.get(key)
                if value is None:
                    continue
                if r"\0" in value:
                    logger.warning(ErrorCodeMap.get(CloudDBErrorCode.INPUT_CONTAIN_ILLEGAL_CHARACTER))
                    raise AGConnectCloudDBException(error_code=CloudDBErrorCode.INPUT_CONTAIN_ILLEGAL_CHARACTER,
                                                    error_message=ErrorCodeMap.get(
                                                        CloudDBErrorCode.INPUT_CONTAIN_ILLEGAL_CHARACTER))

    @staticmethod
    def get_request_id() -> str:
        uuid_params = str(uuid.uuid4())
        const_re = r"/-/gi"
        return uuid_params.replace(const_re, "")

    @staticmethod
    def primary_key_compare_to(obj_1: Any, obj_2: Any, field_type: str):
        if field_type == FieldType.Byte or field_type == FieldType.Short:
            res = int(obj_1) - int(obj_2)
            return res
        if field_type == FieldType.Integer or \
                field_type == FieldType.IntAutoIncrement:
            res = int(obj_1) - int(obj_2)
            return res
        elif field_type == FieldType.String:
            if int(obj_1) > int(obj_2):
                return 1
            elif int(obj_1) < int(obj_2):
                return -1
            else:
                return 0
        elif field_type == FieldType.Float or field_type == FieldType.LongAutoIncrement:
            result = Utils.long_compare_to(obj_1, obj_2)
            return result
        return None

    @staticmethod
    def long_compare_to(obj_1: str or int, obj_2: str):
        if isinstance(obj_1, int):
            obj_1 = str(obj_1)
        if not re.search(Utils.__NUMBER_REG_EXP, obj_1) or not re.search(Utils.__NUMBER_REG_EXP, obj_2):
            raise AGConnectCloudDBException(error_code=CloudDBErrorCode.ERROR_CODE_DATA_INVALID,
                                            error_message=ErrorCodeMap.get(
                                                CloudDBErrorCode.ERROR_CODE_DATA_INVALID))
        if obj_1[0] == '-' and obj_2[0] != '-':
            return -1
        if obj_1[0] != '-' and obj_2[0] == '-':
            return 1
        default_value = -1 if obj_1[0] == '-' else 1
        if len(obj_1) > len(obj_2):
            return default_value
        if len(obj_1) < len(obj_2):
            return -default_value

        for i, value in enumerate(obj_1):
            res = 1
            if value == obj_2[i]:
                res = 0
            if value < obj_2[i]:
                res = -1
            if res != 0:
                return default_value * res
        return 0

    @staticmethod
    def serialize_map_object(obj: Any, maps: Dict[str, Any]):
        new_obj = copy.deepcopy(obj)
        if new_obj.get_id():
            new_obj.set_id(None)
        for key, value in maps.items():
            setattr(new_obj, key, value)
        Utils.check_schema_data_size([new_obj])
        return Utils.serialize_object(new_obj)

    @staticmethod
    def deep_copy(object_list: [Any]):
        const_list = []
        for item in object_list:
            if type(item) is object_list:
                const_list.append(item)
                continue
            if isinstance(item.get("value"), datetime):
                const_list.append(item)
                continue
            if item.get("copy"):
                const_list.append(copy.deepcopy(item))
                continue
            new_obj = {}
            for const_key in item:
                if const_key in item:
                    val = item.get(const_key)
                    new_obj[const_key] = val

            const_list.append(new_obj)
        return const_list
