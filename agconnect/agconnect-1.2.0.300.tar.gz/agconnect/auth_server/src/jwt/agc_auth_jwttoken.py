# Copyright (c) Huawei Technologies Co., Ltd. 2022. All rights reserved.
from typing import Union


class AGCAuthJwtToken:
    __token = Union[str, None]
    __expiration_time = Union[int, None]

    def __init__(self, token: str, expiration_time: int):
        self.__token = token
        self.__expiration_time = expiration_time

    def get_token(self) -> Union[str, None]:
        return self.__token

    def get_expiration_time(self) -> Union[int, None]:
        return self.__expiration_time
