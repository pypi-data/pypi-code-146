# Copyright (c) Huawei Technologies Co., Ltd. 2022. All rights reserved.

from typing import Union

from agconnect.common_server import BaseResponse
from agconnect.auth_server.src.response.token_info import TokenInfo


class VerifyTokenRsp(BaseResponse):
    def __init__(self):
        self.__product_id = None
        self.__access_token = None
        self.__uid: Union[str:None] = None

    def get_uid(self):
        return self.__uid

    def get_access_token(self):
        return self.__access_token

    def get_product_id(self):
        return self.__product_id

    def construct_response(self, response):
        self.__product_id = response.get("productId")
        self.__access_token = TokenInfo()
        if response.get("accessToken"):
            self.__access_token.set_token(response.get("accessToken").get("token"))
            self.__access_token.set_valid_period(response.get("accessToken").get("valid_period"))
        self.__uid = response.get("uid")
