# Copyright (c) Huawei Technologies Co., Ltd. 2022. All rights reserved.

from __future__ import annotations

from typing import Dict

from agconnect.common_server.src.log_config import logger
from agconnect.database_server.src.exception.agconnect_cloud_db_exception import AGConnectCloudDBException
from agconnect.database_server.src.exception.cloud_db_error_code import CloudDBErrorCode
from agconnect.database_server.src.exception.error_code_message import ErrorCodeMap
from agconnect.database_server.src.query.cloud_db_zone_config import CloudDBZoneConfig
from agconnect.common_server.src.agc_client import AGCClient
from agconnect.database_server.src.services.cloud_db_service import CloudDBService
from agconnect.database_server.src.services import cloud_db_zone


class AGConnectCloudDB(CloudDBService):
    __AG_CONNECT_MULTI_ClOUD_DB: Dict[str, AGConnectCloudDB] = {}
    __USER_KEY = "v3/userKey"
    __UID_MAX_SIZE = 100
    __RETENTION_PERIOD_URL = 'v1/retentionPeriod'

    def __init__(self, agc_client: AGCClient):
        super().__init__(agc_client)

    @classmethod
    def initialize(cls, agc_client: AGCClient):
        if not agc_client:
            logger.warning(ErrorCodeMap.get(CloudDBErrorCode.VALUE_IS_NULL))
            raise AGConnectCloudDBException(error_code=CloudDBErrorCode.VALUE_IS_NULL,
                                            error_message=ErrorCodeMap.get(
                                                CloudDBErrorCode.VALUE_IS_NULL))
        region = agc_client.get_credential().get_region()
        if not cls.__AG_CONNECT_MULTI_ClOUD_DB.get(region):
            cls.__AG_CONNECT_MULTI_ClOUD_DB[region] = AGConnectCloudDB(agc_client)

    @staticmethod
    def get_instance(agc_client: AGCClient) -> AGConnectCloudDB:
        if len(AGConnectCloudDB.__AG_CONNECT_MULTI_ClOUD_DB) == 0:
            logger.warning(ErrorCodeMap.get(CloudDBErrorCode.AGCONNECT_CLOUDDB_NOT_INITIALIZE))
            raise AGConnectCloudDBException(error_code=CloudDBErrorCode.AGCONNECT_CLOUDDB_NOT_INITIALIZE,
                                            error_message=ErrorCodeMap.get(
                                                CloudDBErrorCode.AGCONNECT_CLOUDDB_NOT_INITIALIZE))
        agconnect_cloud_db = AGConnectCloudDB.__AG_CONNECT_MULTI_ClOUD_DB.get(
            agc_client.get_credential().get_region()
        )
        if not agconnect_cloud_db:
            logger.warning(ErrorCodeMap.get(CloudDBErrorCode.AGCONNECT_CLOUDDB_NOT_INITIALIZE))
            raise AGConnectCloudDBException(error_code=CloudDBErrorCode.AGCONNECT_CLOUDDB_NOT_INITIALIZE,
                                            error_message=ErrorCodeMap.get(
                                                CloudDBErrorCode.AGCONNECT_CLOUDDB_NOT_INITIALIZE))
        return agconnect_cloud_db

    def open_cloud_db_zone(self, zone_config: CloudDBZoneConfig) -> cloud_db_zone.CloudDBZone:
        if not zone_config:
            logger.warning(ErrorCodeMap.get(CloudDBErrorCode.VALUE_IS_NULL))
            raise AGConnectCloudDBException(error_code=CloudDBErrorCode.VALUE_IS_NULL,
                                            error_message=ErrorCodeMap.get(
                                                CloudDBErrorCode.VALUE_IS_NULL))
        return cloud_db_zone.CloudDBZone(self._agc_client, zone_config)

    async def execute_delete_user_key(self, uid: str):
        if not uid:
            logger.warning(ErrorCodeMap.get(CloudDBErrorCode.VALUE_IS_NULL))
            raise AGConnectCloudDBException(error_code=CloudDBErrorCode.VALUE_IS_NULL,
                                            error_message=ErrorCodeMap.get(
                                                CloudDBErrorCode.VALUE_IS_NULL))
        if len(uid) > AGConnectCloudDB.__UID_MAX_SIZE:
            logger.warning(ErrorCodeMap.get(CloudDBErrorCode.USERID_IS_INVALID))
            raise AGConnectCloudDBException(error_code=CloudDBErrorCode.USERID_IS_INVALID,
                                            error_message=ErrorCodeMap.get(
                                                CloudDBErrorCode.USERID_IS_INVALID))
        request_url = AGConnectCloudDB._URL_PREFIX + AGConnectCloudDB.__USER_KEY
        data = {
            "user_id": uid
        }
        return await self._object_delete_response(request_url, data)

    def query_deleted_data_retention_period(self):
        request_url = AGConnectCloudDB._URL_PREFIX + AGConnectCloudDB.__RETENTION_PERIOD_URL
        return self._object_get_response(request_url, None)

    def update_deleted_data_retention_period(self, days: int):
        if days < 0 or days > self._MAX_RETENTION_DAYS:
            raise AGConnectCloudDBException(error_code=CloudDBErrorCode.INPUT_PARAMETER_INVALID,
                                            error_message=ErrorCodeMap.get(
                                                CloudDBErrorCode.INPUT_PARAMETER_INVALID))
        request_url = AGConnectCloudDB._URL_PREFIX + AGConnectCloudDB.__RETENTION_PERIOD_URL
        data = {
            "retention_days": days
        }
        return self._object_delete_response(request_url, data)
