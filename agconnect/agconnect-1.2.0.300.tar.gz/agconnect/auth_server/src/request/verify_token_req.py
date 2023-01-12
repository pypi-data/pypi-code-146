# Copyright (c) Huawei Technologies Co., Ltd. 2022. All rights reserved.

import json

from agconnect.common_server import RequestConstructor, CloudGwUrlUtils, AGCClient


class VerifyTokenReq(RequestConstructor):

    def __init__(self, access_token, client: AGCClient):
        self.__client = client
        self.__access_token = access_token

    @property
    def __url(self):
        return "api/oauth2/third/v1/verify-token?productId="

    def get_url(self, use_back_url: bool = False) -> str:
        return CloudGwUrlUtils.get_cloud_gw_url_by_region(self.__client.get_credential().get_region(),
                                                          use_back_url) + self.__url \
               + self.__client.get_credential().get_project_id()

    async def get_headers(self):
        token = await self.__client.get_credential().get_access_token()
        return {"accessToken": self.__access_token, "client_id": self.__client.get_credential().get_client_id(),
                "Authorization": "Bearer " + token}

    @staticmethod
    def get_body():
        return None
