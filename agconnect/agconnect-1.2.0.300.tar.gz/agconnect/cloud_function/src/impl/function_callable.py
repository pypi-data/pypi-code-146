# Copyright (c) Huawei Technologies Co., Ltd. 2022. All rights reserved.

from typing import Any

from agconnect.cloud_function.src.exception.agc_function_error_code import AGCFunctionErrorCode
from agconnect.cloud_function.src.exception.agc_function_exception import AGCFunctionException
from agconnect.cloud_function.src.server.function_backend import FunctionBackend
from agconnect.cloud_function.src.server.request.function_request import FunctionRequest
from agconnect.cloud_function.src.function_types.base import FunctionResult, FunctionCallable


class FunctionCallableImpl(FunctionCallable):
    __http_trigger_url: str = ''
    timeout: int = 3000
    function_backend: FunctionBackend = FunctionBackend()

    def __init__(self, client, http_trigger_url):
        super().__init__()
        self.__client = client
        self.__http_trigger_url = http_trigger_url

    async def call(self, req_body: Any) -> FunctionResult:
        function_request: FunctionRequest = FunctionRequest(self.__client, self.__http_trigger_url, req_body)
        try:
            res = await self.function_backend.do_request(function_request)
        except Exception as e:
            raise AGCFunctionException(AGCFunctionErrorCode.CALL_CLOUD_FUNCTION_FAIL) from e
        return res

    def clone(self, timeout: int) -> FunctionCallable:
        clone_callable = FunctionCallableImpl(self.__client, self.__http_trigger_url)
        clone_callable.timeout = timeout
        return clone_callable

    def set_timeout(self, timeout: int):
        FunctionBackend.set_timeout(timeout)
