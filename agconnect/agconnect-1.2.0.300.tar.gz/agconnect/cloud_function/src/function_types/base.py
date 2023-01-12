# Copyright (c) Huawei Technologies Co., Ltd. 2022. All rights reserved.

import abc
import os
from typing import Any

from agconnect.common_server.src.agc_client import AGCClient
from agconnect.common_server.src.service import AGCService, ServiceFactory


class FunctionResult(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def get_value(self) -> Any:
        pass


class FunctionCallable(metaclass=abc.ABCMeta):
    def __init__(self):
        self.timeout = None

    @abc.abstractmethod
    async def call(self, req_body: Any) -> FunctionResult:
        pass

    @abc.abstractmethod
    def clone(self, timeout: int):
        pass

    @abc.abstractmethod
    def set_timeout(self, timeout: int):
        pass


class AGConnectFunctionService(AGCService, metaclass=abc.ABCMeta):

    def __init__(self):
        self.client = None

    @abc.abstractmethod
    def wrap(self, http_trigger_url: str) -> FunctionCallable:
        pass


class AGConnectFunction:
    SERVICE_NAME = 'CLOUD FUNCTION'

    @staticmethod
    def factory():
        from agconnect.cloud_function.src.impl.agconnect_function_impl import AGConnectFunctionImpl
        return AGConnectFunctionImpl()

    @staticmethod
    def get_instance(name: str = None) -> AGConnectFunctionService:
        path = os.path.join(os.path.dirname(__file__), "../../../auth_server/agconnect_auth.json")
        return ServiceFactory.initialize_service(client=AGCClient.get_instance(name),
                                                 service_name=AGConnectFunction.SERVICE_NAME,
                                                 fact=AGConnectFunction.factory, config_path=path)
