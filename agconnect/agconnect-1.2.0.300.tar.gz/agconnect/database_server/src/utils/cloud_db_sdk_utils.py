# Copyright (c) Huawei Technologies Co., Ltd. 2022. All rights reserved.

import os
from typing import Any

from agconnect.common_server.src.config.cloud_gw_url_utils import CloudGwUrlUtils, ConfigService

CONFIG_PATH = os.path.normpath(os.path.join(os.path.dirname(__file__), '../../agconnect-database.json'))


class CloudDBSdkUtils:
    __SERVICE_NAME = "CloudDB"

    @staticmethod
    def get_cloud_gw_url(region: str = None, use_back_up=False):
        return CloudGwUrlUtils.get_cloud_gw_url_by_region(region, use_back_up)

    @classmethod
    def __get_service(cls) -> ConfigService:
        ConfigService.initial_load_service_config(cls.__SERVICE_NAME,
                                                  CONFIG_PATH)
        return ConfigService.get_service(cls.__SERVICE_NAME)

    @classmethod
    def get_cloud_sdk_name(cls) -> str:
        sdk_name: str = cls.__get_service().get_config_value("sdk_name")
        return sdk_name

    @classmethod
    def get_cloud_sdk_version(cls) -> str:
        sdk_version: Any = cls.__get_service().get_config_value("sdk_version")
        return sdk_version
