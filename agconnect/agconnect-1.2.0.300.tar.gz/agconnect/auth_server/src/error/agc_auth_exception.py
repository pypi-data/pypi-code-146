# Copyright (c) Huawei Technologies Co., Ltd. 2022. All rights reserved.

from typing import Any

from agconnect.common_server import AGCException


class AGCAuthException(AGCException):
    def __init__(self, error_code: dict, name: str, extra: Any = None):
        if extra and str(extra):
            super().__init__(error_code, name=name, suffix='AUTH', msg=str(extra))
        else:
            super().__init__(error_code, name=name, suffix='AUTH')
