# Copyright (c) Huawei Technologies Co., Ltd. 2022. All rights reserved.

from typing import Callable, Any
from aiohttp import TCPConnector

from agconnect.cloud_function.src.exception.agc_function_error_code import AGCFunctionErrorCode
from agconnect.cloud_function.src.exception.agc_function_exception import AGCFunctionException
from agconnect.cloud_function.src.impl.function_result_impl import FunctionResultImpl
from agconnect.cloud_function.src.server.request.function_request import FunctionRequest
from agconnect.common_server.src.config import ConfigService
from agconnect.common_server.src.http_client import get_http_client, CommonHeaders
from agconnect.common_server.src.http_client.http_client_api import HttpClientApiImpl, HttpMethod, HttpClientCfg


class FunctionHttpClientCfg(HttpClientCfg):
    maxBodyLength = 30 * 1024 * 1024
    maxContentLength = 30 * 1024 * 1024
    timeout = 55000

    @classmethod
    def set_timeout(cls, timeout: int):
        if timeout <= 0 or timeout > 55000:
            raise AGCFunctionException(AGCFunctionErrorCode.TIMEOUT_OUT_OF_RANGE)

        cls.timeout = timeout


class FunctionBackend:
    __resolver = None
    __connector_cb: Callable[[Any], TCPConnector] = None
    __http_client: HttpClientApiImpl = None
    __NAME = "FunctionBackend"
    timeout = 55000

    @staticmethod
    def get_auth_common_header():
        return {
            'serverSdkName':
                CommonHeaders.SDK_PREFIX + ConfigService.get_service("AUTH").get_config_value(
                    CommonHeaders.SDK_NAME),
            'serverSdkVersion':
                ConfigService.get_service("AUTH").get_config_value(CommonHeaders.SDK_VERSION)
        }

    @classmethod
    def __init_http_client(cls, proxy: dict = None, connector_builder=None, resolver=None):
        if connector_builder is not None:
            FunctionBackend.__connector_cb = connector_builder
        if resolver is not None:
            FunctionBackend.__resolver = resolver
        if FunctionBackend.__connector_cb is not None:
            cfg = FunctionHttpClientCfg(common_headers=FunctionBackend.get_auth_common_header(),
                                        proxy_map=proxy,
                                        connector=FunctionBackend.__connector_cb(FunctionBackend.__resolver))
        else:
            cfg = FunctionHttpClientCfg(common_headers=FunctionBackend.get_auth_common_header(),
                                        proxy_map=proxy,
                                        connector=None)
        cfg.set_timeout(cls.timeout)
        FunctionBackend.__http_client = get_http_client(cfg)

    @classmethod
    async def do_request(cls, function_request: FunctionRequest):
        header = await function_request.get_headers()
        FunctionBackend.__init_http_client()
        async with FunctionBackend.__http_client as cli:
            request_resp = await cli.request(HttpMethod.POST,
                                             function_request.get_url(),
                                             data=function_request.get_body(),
                                             headers=header)
        return await FunctionBackend.__handle_response(request_resp)

    @staticmethod
    async def __handle_response(request_resp):
        try:
            data = await request_resp.json()
            response = FunctionResultImpl()
            response.construct_response(data)
        except Exception as err:
            raise AGCFunctionException(AGCFunctionErrorCode.CALL_CLOUD_FUNCTION_FAIL) from err
        return response

    @classmethod
    def set_timeout(cls, timeout):
        cls.timeout = timeout
