# Copyright (c) Huawei Technologies Co., Ltd. 2022. All rights reserved.

import json
from typing import Any, Dict

from aiohttp import ClientTimeout
from agconnect.common_server.src.agc_client import AGCClient
from agconnect.common_server.src.http_client import get_http_client
from agconnect.common_server.src.http_client.http_client_api import HttpClientAPI, HttpClientCfg, HttpMethod
from agconnect.common_server.src.log_config import logger
from agconnect.database_server.src.communicator.request_header import RequestHeader
from agconnect.database_server.src.exception.agconnect_cloud_db_exception import AGConnectCloudDBException
from agconnect.database_server.src.exception.cloud_db_error_code import CloudDBErrorCode
from agconnect.database_server.src.exception.error_code_message import ErrorCodeMap
from agconnect.database_server.src.utils.cloud_db_sdk_utils import CloudDBSdkUtils


class RequestTemplate:
    def __init__(self, url: str, backup_url: str, headers: RequestHeader, params: Dict[str, Any]):
        self.url = url
        self.backup_url = backup_url
        self.headers = headers
        self.params = params


class HttpsCommunicator:
    __MAX_BODY_LENGTH = 30 * 1024 * 1024
    __MAX_CONTENT_LENGTH = str(30 * 1024 * 1024)
    __timeout = 0
    __request_template: RequestTemplate = None
    __agc_client: AGCClient = None
    __http_client: HttpClientAPI = None
    __request_port = ':443/'

    def __init__(self, agc_client: AGCClient):
        self.__agc_client = agc_client
        credential = self.__agc_client.get_credential()
        if not credential:
            logger.warning(ErrorCodeMap.get(CloudDBErrorCode.FAIL_TO_GET_CREDENTIAL))
            raise AGConnectCloudDBException(
                error_code=CloudDBErrorCode.FAIL_TO_GET_CREDENTIAL,
                error_message=ErrorCodeMap.get(CloudDBErrorCode.FAIL_TO_GET_CREDENTIAL),
            )
        url_without_port = CloudDBSdkUtils.get_cloud_gw_url(credential.get_region())
        backup_url_without_port = CloudDBSdkUtils.get_cloud_gw_url(
            credential.get_region(), True
        )
        headers = RequestHeader(credential.get_client_id(), credential.get_project_id())

        self.__request_template = RequestTemplate(
            url=url_without_port[0: len(url_without_port) - 1] + self.__request_port,
            backup_url=backup_url_without_port[0: len(
                backup_url_without_port) - 1] + self.__request_port,
            headers=headers,
            params={},
        )

    def __init_http_client(self):
        http_client_config: HttpClientCfg = HttpClientCfg(
            max_body_length=self.__MAX_BODY_LENGTH, timeout=ClientTimeout(self.__timeout)
        )
        HttpsCommunicator.__http_client = get_http_client(http_client_config)

    async def send_get_request(self, request_url: str, request_id: str, data: Any, use_backup: bool or None = None):
        try:
            return await self.__send_request(method=HttpMethod.GET, request_id=request_id, use_backup=use_backup,
                                             request_url=request_url, data=data)
        except Exception as err:
            raise err from err

    async def send_post_request(self, request_url: str, request_id: str, data: Any, use_backup=True):
        try:
            return await self.__send_request(method=HttpMethod.POST, request_id=request_id, use_backup=use_backup,
                                             request_url=request_url, data=json.dumps(data))
        except Exception as err:
            raise err from err

    async def send_delete_request(self, request_url: str, request_id: str, data: Any, use_backup=True):
        try:
            return await self.__send_request(method=HttpMethod.DELETE, request_id=request_id, use_backup=use_backup,
                                             request_url=request_url, data=json.dumps(data))
        except Exception as err:
            raise err from err

    async def send_put_request(self, request_url: str, request_id: str, data: Any, use_backup=True):
        try:
            return await self.__send_request(method=HttpMethod.PUT, request_id=request_id, use_backup=use_backup,
                                             request_url=request_url, data=json.dumps(data))
        except Exception as err:
            raise err from err

    async def __send_request(self, request_id: str, request_url: str, data: Any, **options):
        token = await self.__generate_auth()
        self.__request_template.headers.set_authorization("Bearer " + token)
        self.__request_template.headers.set_request_id(request_id)
        real_request_url = self.__request_template.backup_url + request_url \
            if options.get("use_backup") else self.__request_template.url + request_url

        self.__init_http_client()
        async with HttpsCommunicator.__http_client as cli:
            if options.get("method") == HttpMethod.GET:
                return await cli.request(HttpMethod.GET, real_request_url,
                                         headers=self.__request_template.headers.get_headers())
            elif options.get("method") == HttpMethod.POST:
                return await cli.request(HttpMethod.POST, real_request_url, data=data,
                                         headers=self.__request_template.headers.get_headers())
            elif options.get("method") == HttpMethod.DELETE:
                return await cli.request(HttpMethod.DELETE, real_request_url, data=data,
                                         headers=self.__request_template.headers.get_headers())
            elif options.get("method") == HttpMethod.PUT:
                return await cli.request(HttpMethod.PUT, real_request_url, data=data,
                                         headers=self.__request_template.headers.get_headers())
            else:
                raise TypeError("Not support the type of request.")

    async def __generate_auth(self):
        try:
            return await self.__agc_client.get_credential().get_access_token()
        except Exception as err:
            raise err from err
