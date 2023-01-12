# Copyright (c) Huawei Technologies Co., Ltd. 2022. All rights reserved.

class TokenInfo:
    def __init__(self):
        self.__token = None
        self.__valid_period = None

    def get_token(self):
        return self.__token

    def set_token(self, token: str):
        self.__token = token

    def get_valid_period(self):
        return self.__valid_period

    def set_valid_period(self, valid_period: str):
        self.__valid_period = valid_period
