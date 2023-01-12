# Copyright (c) Huawei Technologies Co., Ltd. 2022. All rights reserved.

class AGCBaseException(Exception):
    _COLON = ': '
    _COMMA = ', '
    _DASH = '-'
    __default_name = 'AGCException'

    def __init__(self, msg, name=None, suffix=None):

        super().__init__()

        self.message = msg
        if name:
            self.name = name
        else:
            self.name = self.__default_name
        if suffix:
            self.name = self.name + AGCBaseException._DASH + suffix

    def set_name(self, name):
        self.name = name

    def get_name(self) -> str:
        return self.name


class AGCException(AGCBaseException):
    __error_code = {'code': None, 'message': None}

    def __init__(self, error_code, name=None, msg=None, suffix=None):
        error_msg = str(error_code['code']) + AGCException._COLON + error_code['message']
        if msg:
            error_msg = error_msg + AGCException._COMMA + msg

        super().__init__(error_msg, name, suffix)

        self.__error_code = error_code
        if msg:
            self.__error_code['message'] = self.__error_code['message'] + \
                                           AGCException._COMMA + msg

    def get_code(self) -> str:
        return self.__error_code['code']

    def get_message(self) -> str:
        return self.__error_code['message']
