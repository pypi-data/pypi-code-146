# Copyright (c) Huawei Technologies Co., Ltd. 2022. All rights reserved.

from __future__ import annotations
from typing import Any, Dict

from agconnect.common_server.src.log_config import logger
from agconnect.database_server.src.exception.agconnect_cloud_db_exception import AGConnectCloudDBException
from agconnect.database_server.src.exception.cloud_db_error_code import CloudDBErrorCode
from agconnect.database_server.src.exception.error_code_message import ErrorCodeMap
from agconnect.database_server.src.utils import data_model_helper
from agconnect.database_server.src.utils.utils import Utils


class CloudDBZoneObjectOperator:

    def __init__(self, obj: Any):
        self.__obj = obj
        self.__increment_map: Dict[str: Any] = {}
        self.__update_map: Dict[str: Any] = {}

    @staticmethod
    def build(obj: Any) -> CloudDBZoneObjectOperator:
        type_of_object = Utils.is_object_valid(obj)
        if not obj or not type_of_object:
            logger.warning(ErrorCodeMap.get(CloudDBErrorCode.OBJECT_IS_INVALID))
            raise AGConnectCloudDBException(error_code=CloudDBErrorCode.OBJECT_IS_INVALID,
                                            error_message=ErrorCodeMap.get(
                                                CloudDBErrorCode.OBJECT_IS_INVALID))
        data_model_helper.DataModelHelper.check_primary_keys(obj)
        return CloudDBZoneObjectOperator(obj)

    def increment(self, field_name: str, delta: Any) -> CloudDBZoneObjectOperator:
        if self.__increment_map.get(field_name) or self.__update_map.get(field_name):
            logger.warning(ErrorCodeMap.get(CloudDBErrorCode.DUPLICATE_FIELD))
            raise AGConnectCloudDBException(error_code=CloudDBErrorCode.DUPLICATE_FIELD,
                                            error_message=ErrorCodeMap.get(
                                                CloudDBErrorCode.DUPLICATE_FIELD))
        data_model_helper.DataModelHelper.check_operator_field(field_name, delta, self.__obj, True)
        self.__increment_map[field_name] = delta
        return self

    def update(self, field_name: str, value: Any) -> CloudDBZoneObjectOperator:
        if self.__increment_map.get(field_name) or self.__update_map.get(field_name):
            raise AGConnectCloudDBException(error_code=CloudDBErrorCode.DUPLICATE_FIELD,
                                            error_message=ErrorCodeMap.get(
                                                CloudDBErrorCode.DUPLICATE_FIELD))
        data_model_helper.DataModelHelper.check_operator_field(field_name, value, self.__obj)
        self.__update_map[field_name] = value
        return self

    def get_object(self) -> Any:
        return self.__obj

    def get_increment_map(self) -> Dict[str, int]:
        return self.__increment_map

    def get_update_map(self) -> Dict[str, Any]:
        return self.__update_map
