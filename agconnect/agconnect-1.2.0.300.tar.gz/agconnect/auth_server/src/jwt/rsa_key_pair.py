# Copyright (c) Huawei Technologies Co., Ltd. 2022. All rights reserved.

class RSAKeyPair:
    def __init__(self, public_key: str, private_key: str):
        self.__public_key = public_key
        self.__private_key = private_key

    def get_public_key(self) -> str:
        return self.__public_key

    def get_private_key(self) -> str:
        return self.__private_key

    def get_keys(self):
        return self.__private_key, self.__public_key
