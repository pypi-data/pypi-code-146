# Copyright (c) Huawei Technologies Co., Ltd. 2022. All rights reserved.
import abc


class RequestConstructor(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def get_url(self, use_back_url: bool = False) -> str:
        pass

    @abc.abstractmethod
    async def get_headers(self):
        pass

    @staticmethod
    def get_body():
        pass
