# Copyright (c) Huawei Technologies Co., Ltd. 2022. All rights reserved.

from typing import Any, Dict

from agconnect.common_server.src.agc_client import AGCClient
from agconnect.common_server.src.log_config import logger
from agconnect.database_server.src.communicator.https_communicator import HttpsCommunicator
from agconnect.database_server.src.exception.agconnect_cloud_db_exception import AGConnectCloudDBException
from agconnect.database_server.src.exception.cloud_db_error_code import CloudDBErrorCode
from agconnect.database_server.src.exception.error_code_message import ErrorCodeMap, get_error_message
from agconnect.database_server.src.utils.utils import Utils


class CloudDBService:
    _agc_client: AGCClient
    _URL_PREFIX = 'api/clouddb/clouddbservice/'
    _request_sender: HttpsCommunicator
    _MAX_RETENTION_DAYS = 60
    _KEY_RETENTION_DAYS = 'retentionDays'

    def __init__(self, agc_client: AGCClient):
        if not agc_client:
            logger.warning(ErrorCodeMap.get(CloudDBErrorCode.VALUE_IS_NULL))
            raise AGConnectCloudDBException(error_code=CloudDBErrorCode.VALUE_IS_NULL,
                                            error_message=ErrorCodeMap.get(CloudDBErrorCode.VALUE_IS_NULL))

        self._agc_client = agc_client
        self._request_sender = HttpsCommunicator(self._agc_client)

    def _object_get_response(self, request_url: str, data: Any = None) -> int:
        request_id = Utils.get_request_id()
        try:
            resp = self._request_sender.send_get_request(request_url, request_id, data)
            self._check_response_body(resp)
            return resp["data"][CloudDBService._KEY_RETENTION_DAYS]
        except AGConnectCloudDBException:
            return self.__resend_get_request(request_url, request_id, data)

    def _object_put_response(self, request_url: str, data: Any = None) -> int:
        request_id = Utils.get_request_id()
        try:
            resp = self._request_sender.send_put_request(request_url, request_id, data)
            self._check_response_body(resp)
            return resp["data"][CloudDBService._KEY_RETENTION_DAYS]
        except AGConnectCloudDBException:
            return self.__resend_put_request(request_url, request_id, data)

    def __resend_get_request(self, request_url, request_id, data):
        try:
            resp = self._request_sender.send_get_request(request_url, request_url, data, True)
            self._check_response_body(resp)
            return resp[data][CloudDBService._KEY_RETENTION_DAYS]
        except AGConnectCloudDBException as err:
            logger.warning("Get catch error, requestId:", request_id)
            if CloudDBService._is_err_response_not_valid(err):
                return None
            raise AGConnectCloudDBException(str(err)) from err

    def __resend_put_request(self, request_url, request_id, data):
        try:
            resp = self._request_sender.send_put_request(request_url, request_url, data, True)
            self._check_response_body(resp)
            return resp["data"][CloudDBService._KEY_RETENTION_DAYS]
        except AGConnectCloudDBException as err:
            logger.warning("Put catch error, requestId:", request_id)
            if CloudDBService._is_err_response_not_valid(err):
                return None
            raise AGConnectCloudDBException(str(err)) from err

    async def _object_delete_response(self, request_url: str, data: Any):
        request_id = Utils.get_request_id()
        try:
            resp = await self._request_sender.send_delete_request(request_url, request_id, data, True)
            await CloudDBService._check_response_body(resp)
            data = await resp.json()
            return data.get("delNumber")
        except AGConnectCloudDBException:
            return await self.__resend_delete_request(request_url, request_id, data)

    async def __resend_delete_request(self, request_url: str, request_id, data: Any):
        try:
            resp = await self._request_sender.send_delete_request(request_url, request_id, data, True)
            await CloudDBService._check_response_body(resp)
            data = await resp.json()
            return data.get("delNumber")
        except AGConnectCloudDBException as err:
            logger.warning("Delete catch error, requestId:", request_id)
            if CloudDBService._is_err_response_not_valid(err):
                return None
            raise AGConnectCloudDBException(str(err)) from err

    @staticmethod
    async def _check_response_body(resp: Any):
        data = await resp.json()
        if resp.status == 200 and not data:
            logger.warning(ErrorCodeMap.get(CloudDBErrorCode.RESPONSE_IS_INVALID))
            raise AGConnectCloudDBException(error_code=CloudDBErrorCode.RESPONSE_IS_INVALID,
                                            error_message=ErrorCodeMap.get(
                                                CloudDBErrorCode.RESPONSE_IS_INVALID))

    @staticmethod
    def _is_err_response_not_valid(err: Any, response_json: Dict = None) -> bool:
        expression_1 = response_json is None or response_json.get("data") is None
        expression_2 = response_json.get("errorCodeV2") is None or not \
            get_error_message(response_json.get("errorCodeV2"))
        if expression_1 or expression_2:
            return True
        logger.warning('Get cloud error code', str(err))
        return False
