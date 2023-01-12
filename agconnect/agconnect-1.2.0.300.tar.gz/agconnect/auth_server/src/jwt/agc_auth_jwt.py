# Copyright (c) Huawei Technologies Co., Ltd. 2022. All rights reserved.

import base64
import json
import time
from typing import Union


class DefaultAGCAuthJwt(object):
    def __new__(cls, *args, **kwarg):
        if not hasattr(cls, 'instance'):
            cls.instance = super(DefaultAGCAuthJwt, cls).__new__(cls, *args, **kwarg)
        return cls.instance


class AGCAuthJwt(object):
    obj = DefaultAGCAuthJwt()
    __SEP = "."
    __HEAD = 0
    __PAYLOAD = 1
    __SIGNATURE = 2

    def __init__(self):
        self.__header: Union[None, str] = None
        self.__payload: Union[None, str] = None
        self.__signature: Union[None, str] = None

    @staticmethod
    def parse(jwt_token: str) -> obj:
        fields = jwt_token.split(AGCAuthJwt.__SEP)
        jwt = AGCAuthJwt()
        jwt.__header = fields[AGCAuthJwt.__HEAD]
        jwt.__payload = fields[AGCAuthJwt.__PAYLOAD]
        jwt.__signature = fields[AGCAuthJwt.__SIGNATURE]
        return jwt

    def parse_alg(self):
        header_json = None
        if self.__header is not None:
            header_json = json.loads(base64.b64decode(self.__header + '=='))
        if header_json is not None and header_json.get('alg'):
            return header_json.get('alg')
        return None

    def parse_kid(self):
        header_json = None
        if self.__header is not None:
            header_json = json.loads(base64.b64decode(self.__header + '=='))
        if header_json is not None and header_json.get("kid"):
            return header_json.get("kid")
        return None

    def parse_payload(self):
        return json.loads(base64.b64encode(self.__payload.encode('ascii')))

    def expire(self):
        payload_json = json.loads(base64.b64decode(self.__payload.encode('ascii') + b'=='))
        return 0 < payload_json.get("exp") < int(round(time.time()))
