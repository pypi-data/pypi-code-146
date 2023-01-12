# Copyright (c) Huawei Technologies Co., Ltd. 2022. All rights reserved.

from abc import ABCMeta, abstractmethod

from agconnect.common_server.src.http_client.connect_ret import ConnectRet


class BaseResponse(metaclass=ABCMeta):
    ret: ConnectRet = ConnectRet(0, "")

    def is_success(self) -> bool:
        return self.ret is not None and self.ret.get_code() == 0

    def get_ret(self) -> ConnectRet:
        return self.ret

    def set_ret(self, value: ConnectRet):
        self.ret = value

    @abstractmethod
    def construct_response(self, response) -> None:
        pass
