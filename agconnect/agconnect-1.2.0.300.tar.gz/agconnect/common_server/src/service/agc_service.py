# Copyright (c) Huawei Technologies Co., Ltd. 2022. All rights reserved.

from abc import abstractmethod
from agconnect.common_server.src.agc_client.agc_client import AGCClient


class AGCService:

    @abstractmethod
    def initialize(self, client: AGCClient):
        pass

    @abstractmethod
    def get_service_name(self) -> str:
        pass
    