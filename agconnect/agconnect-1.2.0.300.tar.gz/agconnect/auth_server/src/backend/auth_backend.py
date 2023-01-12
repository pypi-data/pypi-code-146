# Copyright (c) Huawei Technologies Co., Ltd. 2022. All rights reserved.

from typing import Callable, Any

from aiohttp import TCPConnector

from agconnect.auth_server import AGCAuthException, AuthErrorCode
from agconnect.common_server.src.config import ConfigService, CloudGwUrlUtils
from agconnect.common_server.src.http_client import HttpClientCfg, CommonHeaders, get_http_client, RequestConstructor, \
    BaseResponse, ConnectRet
from agconnect.common_server.src.http_client.http_client_api import HttpMethod, HttpClientApiImpl
from agconnect.common_server.src.log_config import logger


class AuthBackend:
    __resolver = None
    __connector_cb: Callable[[Any], TCPConnector] = None
    __http_client: HttpClientApiImpl = None
    __NAME = "AuthBackend"
    __DEFAULT_ERROR = AuthErrorCode.AUTH_CLI_REQUEST_FAIL

    @staticmethod
    async def post(request: RequestConstructor, response: BaseResponse, enable_back_url: bool = False):
        AuthBackend.__init_http_client(connector_builder=AuthBackend.__connector_cb)
        header = await request.get_headers()
        try:
            async with AuthBackend.__http_client as cli:
                resp = await cli.request(HttpMethod.POST,
                                         request.get_url(),
                                         data=request.get_body(),
                                         headers=header)

            return await AuthBackend.__handle_response(resp, response)
        except AGCAuthException as e:
            if CloudGwUrlUtils.check_use_back_url(e, enable_back_url):
                logger.info("auth do post request using back url")
                try:
                    async with AuthBackend.__http_client as cli:
                        resp = await cli.request(HttpMethod.POST,
                                                 request.get_url(True),
                                                 data=request.get_body(),
                                                 headers=header)
                        return await AuthBackend.__handle_response(resp, response)
                except AGCAuthException as agc_err:
                    raise AGCAuthException(AuthErrorCode.AUTH_CLI_REQUEST_FAIL, AuthBackend.__NAME) from agc_err
                except Exception as err:
                    raise AGCAuthException(AuthErrorCode.AUTH_CLI_REQUEST_FAIL, AuthBackend.__NAME, str(err)) from err
            else:
                raise AGCAuthException(AuthErrorCode.AUTH_CLI_REQUEST_FAIL, AuthBackend.__NAME) from None

    @staticmethod
    async def get(request: RequestConstructor, response: BaseResponse, enable_back_url: bool = False,
                  ignore_ret: bool = None):
        AuthBackend.__init_http_client(connector_builder=AuthBackend.__connector_cb)
        header = await request.get_headers()
        try:
            async with AuthBackend.__http_client as cli:
                resp = await cli.request(HttpMethod.GET,
                                         request.get_url(),
                                         data=request.get_body(),
                                         headers=header)
                response = await AuthBackend.__handle_response(resp, response, ignore_ret)
                return response
        except AGCAuthException as e:
            if CloudGwUrlUtils.check_use_back_url(e, enable_back_url):
                logger.info("auth do get request using back url")
                try:
                    async with AuthBackend.__http_client as cli:
                        resp = await cli.request(HttpMethod.GET,
                                                 request.get_url(True),
                                                 data=request.get_body(),
                                                 headers=header)
                        response = await AuthBackend.__handle_response(resp, response, ignore_ret)
                        return response
                except AGCAuthException as agc_err:
                    raise AGCAuthException(AuthErrorCode.AUTH_CLI_REQUEST_FAIL, AuthBackend.__NAME) from agc_err
                except Exception as err:
                    raise AGCAuthException(AuthErrorCode.AUTH_CLI_REQUEST_FAIL, AuthBackend.__NAME, str(err)) from err
            else:
                raise AGCAuthException(AuthErrorCode.AUTH_CLI_REQUEST_FAIL, AuthBackend.__NAME) from None

    @staticmethod
    async def __handle_response(resp, response, ignore_ret: bool = False):
        try:
            data = await resp.json()
        except Exception as err:
            raise AGCAuthException(AuthBackend.__DEFAULT_ERROR, AuthBackend.__NAME, "Reason: " + resp.reason) from err
        if ignore_ret:
            response.construct_response(data)
        else:
            if data.get('ret') and data.get('ret').get('code') == 0:
                response.construct_response(data)
            response.set_ret(ConnectRet(data.get('ret').get('code'), data.get('ret').get('msg')))
        return response

    @staticmethod
    def __init_http_client(proxy: dict = None, connector_builder=None, resolver=None):
        if connector_builder is not None:
            AuthBackend.__connector_cb = connector_builder
        if resolver is not None:
            AuthBackend.__resolver = resolver
        if AuthBackend.__connector_cb is not None:
            AuthBackend.__http_client = get_http_client(
                HttpClientCfg(common_headers=AuthBackend.get_auth_common_header(),
                              proxy_map=proxy,
                              connector=AuthBackend.__connector_cb(AuthBackend.__resolver)))
        else:
            AuthBackend.__http_client = get_http_client(
                HttpClientCfg(common_headers=AuthBackend.get_auth_common_header(),
                              proxy_map=proxy,
                              connector=None))

    @staticmethod
    def get_auth_common_header():
        return {
            'serverSdkName':
                CommonHeaders.SDK_PREFIX + ConfigService.get_service("AUTH").get_config_value(
                    CommonHeaders.SDK_NAME),
            'serverSdkVersion':
                ConfigService.get_service("AUTH").get_config_value(CommonHeaders.SDK_VERSION)
        }
