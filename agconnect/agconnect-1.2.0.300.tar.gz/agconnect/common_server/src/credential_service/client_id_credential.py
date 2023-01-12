# Copyright (c) Huawei Technologies Co., Ltd. 2022. All rights reserved.

import json
import time
from datetime import datetime, timezone

import aiohttp

from agconnect.common_server.src.config.cloud_gw_url_utils import CloudGwUrlUtils
from agconnect.common_server.src.config.config_service import ConfigService
from agconnect.common_server.src.credential_service.access_token import AccessToken
from agconnect.common_server.src.credential_service.credential_service import CredentialService
from agconnect.common_server.src.error.error import AGCException
from agconnect.common_server.src.error.error_message import ErrorCodeConstant
from agconnect.common_server.src.http_client.http_client import get_http_client
from agconnect.common_server.src.http_client.http_client_api import HttpMethod
from agconnect.common_server.src.log_config.common_log import logger


class ClientIdCredential(CredentialService):
    __CLIENT_TOK_PATH = 'client_token_path'

    def __init__(self, client_id='', client_sec='', project_id='',
                 developer_id='', region='', project_type='', configuration_version='', tkn=None):
        self.__region = region
        self.__client_id = client_id
        self.__client_secret = client_sec
        self.__developer_id = developer_id
        self.__configuration_version = configuration_version
        self.__project_id = project_id
        self.__project_type = project_type
        self.__access_token: AccessToken = tkn

    def get_region(self) -> str:
        return self.__region

    def get_project_id(self) -> str:
        return self.__project_id

    def get_client_id(self) -> str:
        return self.__client_id

    def get_developer_id(self) -> str:
        return self.__developer_id

    def get_client_secret(self) -> str:
        return self.__client_secret

    def get_configuration_version(self) -> str:
        return self.__configuration_version

    def get_project_type(self) -> str:
        return self.__project_type

    def set_region(self, region):
        self.__region = region

    async def get_access_token(self) -> str:
        if self.__access_token is None or self.__access_token.is_valid() is False:
            token = await self.refresh_access_token()
        else:
            token = self.__access_token.get_token()
        return token

    async def refresh_access_token(self):
        http_cli = get_http_client()
        body = {
            "grant_type": 'client_credentials',
            "client_id": self.__client_id,
            "client_secret": self.__client_secret
        }
        header = {
            "algorithm_type": "1"
        }
        res_json = {}
        try:
            async with http_cli as client:
                resp = await client.request(HttpMethod.POST, self.__get_gw_token_url(), json.dumps(body), params={},
                                            headers=header)
                resp.raise_for_status()
                if resp.status == 200:
                    res_json = await resp.json()
        except aiohttp.ClientConnectorError as e:
            logger.error(f"{str(ErrorCodeConstant.REQUEST_TOK_FAILED)} Client Connection Error.")
            raise AGCException(ErrorCodeConstant.REQUEST_TOK_FAILED, msg=" , Client Connection Error.") from e
        except Exception as e:
            logger.error(ErrorCodeConstant.REQUEST_TOK_FAILED)
            raise AGCException(ErrorCodeConstant.REQUEST_TOK_FAILED) from e
        token = res_json.get('access_token')
        expires_in = res_json.get('expires_in')
        local_time = time.localtime()
        now = datetime(local_time[0], local_time[1], local_time[2], local_time[3], local_time[4], local_time[5])
        self.__access_token = AccessToken(token=token, expiration_time=self.__timestamp(now) + 1000 * expires_in)
        return token

    def __get_gw_token_url(self, use_back_url: bool = None):
        url = CloudGwUrlUtils.get_cloud_gw_url_by_region(self.get_region(), bool(use_back_url))
        path = ConfigService.get_service("COMMON").get_config_value(ClientIdCredential.__CLIENT_TOK_PATH)
        return url + path

    @staticmethod
    def __timestamp(date_time: datetime):
        return date_time.replace(tzinfo=timezone.utc).timestamp() * 1000
