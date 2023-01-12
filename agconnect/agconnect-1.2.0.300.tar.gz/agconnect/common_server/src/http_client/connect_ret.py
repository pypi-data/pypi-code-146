# Copyright (c) Huawei Technologies Co., Ltd. 2022. All rights reserved.

class ConnectRet:
    __code: int
    __msg: str

    def __init__(self, code: int, msg: str):
        self.__code = code
        self.__msg = msg

    def get_code(self):
        return self.__code

    def get_msg(self):
        return self.__msg

    def set_msg(self, msg: str):
        self.__msg = msg
