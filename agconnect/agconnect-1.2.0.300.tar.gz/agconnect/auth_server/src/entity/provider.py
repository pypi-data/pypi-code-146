# Copyright (c) Huawei Technologies Co., Ltd. 2022. All rights reserved.

from typing import Union


class Provider:
    def __init__(self):
        self.__provider: Union[str, None] = None
        self.__provider_uid: Union[str, None] = None

    def get_provider(self):
        return self.__provider

    def set_provider(self, provider):
        self.__provider = provider

    def get_provider_uid(self):
        return self.__provider_uid

    def set_provider_uid(self, provider_uid: str):
        self.__provider_uid = provider_uid
