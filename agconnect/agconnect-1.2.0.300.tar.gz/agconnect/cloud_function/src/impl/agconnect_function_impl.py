# Copyright (c) Huawei Technologies Co., Ltd. 2022. All rights reserved.

from typing import Union

from agconnect.auth_server.src.utils.auth_service_api_util import AuthServiceApiUtil
from agconnect.cloud_function.src.impl.function_callable import FunctionCallableImpl
from agconnect.common_server.src.agc_client import AGCClient
from agconnect.cloud_function.src.function_types.base import AGConnectFunction, FunctionCallable


class AGConnectFunctionImpl(AGConnectFunction):
    client: Union[AGCClient, None]

    def initialize(self, client: AGCClient):
        self.client = client

    def get_service_name(self) -> str:
        return AGConnectFunction.SERVICE_NAME + "#" + self.client.get_name()

    def wrap(self, function_name: str, version: str = None) -> FunctionCallable:
        http_trigger_url = function_name + "-$latest"
        if version:
            http_trigger_url = function_name + "-" + version
        AuthServiceApiUtil.check_credential(self.client)
        return FunctionCallableImpl(self.client, http_trigger_url)
