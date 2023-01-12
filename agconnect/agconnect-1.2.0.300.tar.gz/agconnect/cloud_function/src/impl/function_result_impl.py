# Copyright (c) Huawei Technologies Co., Ltd. 2022. All rights reserved.

from typing import Any

from agconnect.common_server import BaseResponse
from agconnect.cloud_function.src.function_types.base import FunctionResult


class FunctionResultImpl(BaseResponse, FunctionResult):
    __response_body: Any = None

    def construct_response(self, response: Any):
        self.__response_body = response

    def get_value(self) -> Any:
        if self.__response_body:
            return self.__response_body
        return None
