# Copyright (c) Huawei Technologies Co., Ltd. 2022. All rights reserved.

import re

from agconnect.common_server.src.log_config import logger
from agconnect.database_server.src.exception.agconnect_cloud_db_exception import AGConnectCloudDBException
from agconnect.database_server.src.exception.cloud_db_error_code import CloudDBErrorCode
from agconnect.database_server.src.exception.error_code_message import ErrorCodeMap


class CloudDBZoneConfig:
    __CLOUD_DB_ZONE_NAME_MAX_LENGTH = 20
    __NATURAL_STORE_NAME_REG_EXP = r'^[a-zA-Z][0-9a-zA-Z]{0,19}$'
    __CLOUD_DB_ZONE_NAME: str

    def __init__(self, zone_name: str):
        self.check_cloud_db_zone_name(zone_name)
        self.__cloud_db_zone_name = zone_name

    def get_cloud_db_zone_name(self) -> str:
        return self.__cloud_db_zone_name

    def check_cloud_db_zone_name(self, zone_name: str):
        if not zone_name or (len(zone_name) > self.__CLOUD_DB_ZONE_NAME_MAX_LENGTH) or not bool(re.match(
                self.__NATURAL_STORE_NAME_REG_EXP, zone_name)):
            logger.warning(ErrorCodeMap.get(CloudDBErrorCode.DATABASE_NAME_INVALID))
            raise AGConnectCloudDBException(error_code=CloudDBErrorCode.DATABASE_NAME_INVALID,
                                            error_message=ErrorCodeMap.get(
                                                CloudDBErrorCode.DATABASE_NAME_INVALID))
