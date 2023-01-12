# Copyright (c) Huawei Technologies Co., Ltd. 2022. All rights reserved.

from agconnect.common_server import RequestConstructor, CloudGwUrlUtils, AGCClient


class RevokeTokenReq(RequestConstructor):

    def __init__(self, uid, client: AGCClient):
        self.__client = client
        self.__uid = uid

    @property
    def __url(self):
        return "api/oauth2/third/v1/revoke-token?productId="

    def get_url(self, use_back_url: bool = False) -> str:
        url = CloudGwUrlUtils.get_cloud_gw_url_by_region(self.__client.get_credential().get_region(),
                                                         use_back_url)
        return url + self.__url + self.__client.get_credential().get_project_id()

    async def get_headers(self):
        token = await self.__client.get_credential().get_access_token()
        return {"uid": self.__uid, "client_id": self.__client.get_credential().get_client_id(),
                "Authorization": "Bearer " + token}

    @staticmethod
    def get_body():
        return None
