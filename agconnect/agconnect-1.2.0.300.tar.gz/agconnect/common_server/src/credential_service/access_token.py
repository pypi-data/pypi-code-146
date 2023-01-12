# Copyright (c) Huawei Technologies Co., Ltd. 2022. All rights reserved.

import time


class AccessToken:
    TWO_MINUTES_EARLY = 60 * 2 * 1000

    def __init__(self, token, expiration_time):
        self.__token = token
        self.__expiration_time = expiration_time

    def get_token(self) -> str:
        return self.__token

    def is_valid(self) -> bool:
        current_time = int(round(time.time() * 1000))
        valid_time = self.__expiration_time - AccessToken.TWO_MINUTES_EARLY
        return True if self.__token is not None and current_time <= valid_time else False
