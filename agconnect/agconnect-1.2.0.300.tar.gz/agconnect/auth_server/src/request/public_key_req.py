# Copyright (c) Huawei Technologies Co., Ltd. 2022. All rights reserved.

from agconnect.common_server import RequestConstructor, ConfigService


class PublicKeyReq(RequestConstructor):

    def get_url(self, use_back_url: bool = False) -> str:
        return ConfigService.get_service("AUTH").get_config_value("publickey_url")

    @staticmethod
    async def get_headers():
        return None

    @staticmethod
    def get_body():
        return None
