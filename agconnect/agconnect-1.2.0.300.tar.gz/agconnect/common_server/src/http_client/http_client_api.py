# Copyright (c) Huawei Technologies Co., Ltd. 2022. All rights reserved.

import abc
import ssl
from enum import Enum
from types import TracebackType
from typing import Optional, Type

import aiohttp.connector
from aiohttp import ClientSession, ClientTimeout

from agconnect.common_server.src.error.error import AGCException
from agconnect.common_server.src.error.error_message import ErrorCodeConstant
from agconnect.common_server.src.http_client.common_headers import CommonHeaders
from agconnect.common_server.src.log_config.common_log import logger
from agconnect.common_server.src.utils.utils import url_validate


class HttpClientCfg:
    DEFAULT_TIMEOUT = 1 * 55
    DEFAULT_RESPONSE_TYPE = "json"
    DEFAULT_CONTENT_TYPE = 'application/json'

    def __init__(self, timeout: ClientTimeout = ClientTimeout(DEFAULT_TIMEOUT),
                 response_type: str = DEFAULT_RESPONSE_TYPE,
                 max_body_length: int = None,
                 max_content_length: int = None,
                 is_enable_ssl_cert: bool = True,
                 ssl_ctx: ssl.SSLContext = None,
                 common_headers: dict = None,
                 dictionary: dict = None, connector=None, proxy_map: dict = None):
        self.timeout = timeout
        self.response_type = response_type
        self.max_content_length = max_content_length
        self.max_body_length = max_body_length
        self.is_enable_ssl_cert = is_enable_ssl_cert
        self.common_headers = common_headers
        self.connector = connector
        self.ssl_ctx = ssl_ctx
        self.proxy_map = proxy_map
        if dictionary is not None:
            self.__dict__.update(dictionary)


class HttpMethod(Enum):
    """HTTP Method"""
    GET = "GET"
    HEAD = "HEAD"
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
    DELETE = "DELETE"
    OPTIONS = "OPTION"
    TRACE = "TRACE"


class HttpClientAPI(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def request(self, method_type: HttpMethod,
                url: str,
                data=None,
                **options):
        pass


class HttpClientApiImpl(HttpClientAPI):
    __cli_sess: ClientSession

    async def close(self) -> None:
        return await self.__cli_sess.close()

    async def __aenter__(self) -> "HttpClientApiImpl":
        return self

    async def __aexit__(
            self,
            exc_type: Optional[Type[BaseException]],
            exc_val: Optional[BaseException],
            exc_tb: Optional[TracebackType],
    ) -> Optional[bool]:
        await self.close()
        return None

    def __init__(self, cfg: HttpClientCfg):
        self.__timeout = ClientTimeout(HttpClientCfg.DEFAULT_TIMEOUT)
        self.__trust_env = False
        self.__resp_headers = {'User-Agent': CommonHeaders.get_user_agent(),
                               'serverSdkName': CommonHeaders.get_sdk_name(),
                               'serverSdkVersion': CommonHeaders.get_sdk_version(),
                               'X-Request-Id': CommonHeaders.generate_request_id(),
                               'Content-Type': HttpClientCfg.DEFAULT_CONTENT_TYPE}
        self.__is_enable_ssl_cert = True
        self.__response_type = HttpClientCfg.DEFAULT_RESPONSE_TYPE
        self.__sslcontext = ssl.create_default_context(purpose=ssl.Purpose.CLIENT_AUTH)
        self.__connector = None
        self.__proxy_map = {}
        if cfg is not None:
            if cfg.timeout is not None:
                self.__timeout = cfg.timeout
            if cfg.response_type is not None:
                self.__response_type = self.__get_response_type(cfg.response_type)
            if cfg.max_body_length is not None:
                # Set Max Body Length -- Defaults to Content-Length See RFC 7230
                pass
            if cfg.max_content_length is not None:
                self.__resp_headers['Content-Length'] = cfg.max_content_length

            if cfg.common_headers is not None and len(cfg.common_headers) > 0:
                for k, v in cfg.common_headers.items():
                    self.__resp_headers[k] = v
            if not cfg.is_enable_ssl_cert:
                self.__is_enable_ssl_cert = False
            if isinstance(cfg.connector, aiohttp.connector.TCPConnector):
                self.__connector = cfg.connector
            if cfg.proxy_map is not None:
                self.__proxy_map = cfg.proxy_map

        if self.__is_enable_ssl_cert:
            if cfg is not None:
                if cfg.ssl_ctx is not None:
                    self.__sslcontext = cfg.ssl_ctx
        else:
            self.__trust_env = True
            pass
        self.__init_http_cli()
        logger.info('Instantiating HttpClientApiImpl')

    def __init_http_cli(self) -> None:
        self.__cli_sess = ClientSession(timeout=self.__timeout,
                                        headers=self.__resp_headers,
                                        connector=self.__connector)

    def get_cli_sess(self):
        return self.__cli_sess

    def request(self,
                method_type: HttpMethod,
                url: str,
                data=None,
                **options):
        if not url_validate(url):
            raise AGCException(ErrorCodeConstant.URL_VALIDATE_FAIL)
        headers = options.get("headers")
        if headers is None:
            headers = {}
        headers.update(self.__resp_headers)
        params = options.get("params")
        if params is None:
            params = {}
        proxy = options.get("proxy")
        proxy_auth = options.get("proxy_auth")
        if proxy is None:
            if self.__proxy_map.get("proxy_host"):
                proxy = self.__proxy_map.get("proxy_host")
            if self.__proxy_map.get("proxy_auth"):
                proxy_auth = self.__proxy_map.get("proxy_auth")
        return self.__cli_sess.request(str(method_type.value),
                                       url,
                                       data=data,
                                       headers=headers,
                                       params=params,
                                       proxy=proxy,
                                       proxy_auth=proxy_auth,
                                       ssl=self.__sslcontext)

    @staticmethod
    def __get_response_type(response_type: str):
        response_types = ('arraybuffer', 'blob', 'document', 'json', 'text', 'stream')
        if response_type is None:
            return "json"
        elif response_type in response_types:
            return response_type
        else:
            logger.error('not supported http response type')
            raise AGCException(ErrorCodeConstant.CREATE_HTTP_CLIENT_RESPONSE_TYPE)
