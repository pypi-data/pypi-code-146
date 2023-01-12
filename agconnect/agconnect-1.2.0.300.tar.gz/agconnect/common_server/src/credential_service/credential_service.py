# Copyright (c) Huawei Technologies Co., Ltd. 2022. All rights reserved.

import abc


class CredentialService(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def get_project_id(self) -> str:
        pass

    @abc.abstractmethod
    def get_region(self) -> str:
        pass

    @abc.abstractmethod
    def get_client_id(self) -> str:
        pass

    @abc.abstractmethod
    def get_developer_id(self) -> str:
        pass

    @abc.abstractmethod
    def get_client_secret(self) -> str:
        pass

    @abc.abstractmethod
    async def get_access_token(self):
        pass
