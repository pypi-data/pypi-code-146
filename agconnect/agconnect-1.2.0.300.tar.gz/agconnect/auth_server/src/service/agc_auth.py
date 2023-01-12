# Copyright (c) Huawei Technologies Co., Ltd. 2022. All rights reserved.

import os

from agconnect.auth_server.src.service.impl.agc_auth_service import AGCAuthService
from agconnect.common_server.src.agc_client.agc_client import AGCClient
from agconnect.common_server.src.service import ServiceFactory


class AGCAuth:
    SERVICE_NAME = 'AUTH'

    @staticmethod
    def factory():
        from agconnect.auth_server.src.service.impl.agc_auth_service_impl import AGCAuthServiceImpl
        return AGCAuthServiceImpl()

    @staticmethod
    def get_instance(name: str = None) -> AGCAuthService:
        path = os.path.normpath(os.path.join(os.path.dirname(__file__), './../../agconnect_auth.json'))
        return ServiceFactory.initialize_service(client=AGCClient.get_instance(name), service_name=AGCAuth.SERVICE_NAME,
                                                 fact=AGCAuth.factory, config_path=path)
