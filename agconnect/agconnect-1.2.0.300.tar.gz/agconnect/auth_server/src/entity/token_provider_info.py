# Copyright (c) Huawei Technologies Co., Ltd. 2022. All rights reserved.

from typing import List

from agconnect.auth_server.src.entity.provider import Provider


class TokenProviderInfo:
    def __init__(self):
        self.__sign_in_provider = None
        self.__providers: list = []

    def get_sign_in_provider(self):
        return self.__sign_in_provider

    def set_sign_in_provider(self, sign_in_provider):
        self.__sign_in_provider = sign_in_provider

    def get_providers(self):
        return self.__providers

    def set_providers(self, providers: List[Provider]):
        self.__providers = providers
