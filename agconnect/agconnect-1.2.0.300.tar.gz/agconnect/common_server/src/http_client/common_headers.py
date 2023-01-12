# Copyright (c) Huawei Technologies Co., Ltd. 2022. All rights reserved.

import uuid

from agconnect.common_server.src.config.config_service import ConfigService


class CommonHeaders:
    DEFAULT_CONFIG = 'agconnect-common'
    KEY_REQUEST_ID = 'X-Request-Id'
    KEY_USER_AGENT = 'User-Agent'
    SDK_NAME = 'sdk_name'
    SDK_VERSION = 'sdk_version'
    ALGORITHM_TYPE_NEW_JWT_TOK = '1'
    SDK_PREFIX = 'python/'

    USER_AGENT_PREFIX = 'AGCServerSDK/'
    KEY_AUTHORIZATION = 'Authorization'
    VALUE_BEARER = 'Bearer '
    KEY_HOST = 'Host'

    @staticmethod
    def generate_request_id() -> str:
        request_uuid = str(uuid.uuid1()).replace('/-/g', '')
        return request_uuid

    @staticmethod
    def get_user_agent() -> str:
        return CommonHeaders.USER_AGENT_PREFIX + str(ConfigService.get_service('COMMON').get_config_value(
            CommonHeaders.SDK_VERSION))

    @staticmethod
    def get_sdk_name(service_name=None) -> str:
        if service_name is not None:
            return CommonHeaders.SDK_PREFIX + service_name
        sdk_service = ConfigService.get_service('COMMON').get_config_value(CommonHeaders.SDK_NAME)
        if sdk_service is not None:
            return CommonHeaders.SDK_PREFIX + sdk_service
        return CommonHeaders.SDK_PREFIX + CommonHeaders.SDK_NAME

    @staticmethod
    def get_sdk_version() -> str:
        sdk_version = ConfigService.get_service('COMMON').get_config_value(CommonHeaders.SDK_VERSION)
        if sdk_version is not None:
            return sdk_version
        return 'unknown'
