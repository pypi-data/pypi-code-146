# Copyright (c) Huawei Technologies Co., Ltd. 2022. All rights reserved.

from agconnect.common_server import AGCException, ConnectRet


class AGCFunctionException(AGCException):
    @staticmethod
    def construct_excp_from_ret(ret: ConnectRet):
        return AGCFunctionException({'code': ret.get_code(), 'message': ret.get_msg()})

    def __init__(self, error_code: dict, error_msg: str = ""):
        super().__init__(error_code, error_msg)
