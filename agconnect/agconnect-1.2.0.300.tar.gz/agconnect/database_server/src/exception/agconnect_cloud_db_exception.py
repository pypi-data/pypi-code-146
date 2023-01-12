# Copyright (c) Huawei Technologies Co. Ltd. 2022. All rights reserved.

from agconnect.common_server import AGCException
from agconnect.database_server.src.exception.error_code_message import get_error_message


class AGConnectCloudDBException(AGCException):
    def __init__(self, error_code: str, error_message=''):
        my_error_code = {"code": error_code,
                         "message": error_message if error_message else get_error_message(error_code)}
        super().__init__(my_error_code, "database_server")
