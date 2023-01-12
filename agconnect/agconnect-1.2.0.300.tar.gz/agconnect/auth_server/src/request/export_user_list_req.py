# Copyright (c) Huawei Technologies Co., Ltd. 2022. All rights reserved.


from agconnect.common_server import RequestConstructor, CloudGwUrlUtils, AGCClient


class ExportUserListReq(RequestConstructor):

    def __init__(self, block, client: AGCClient):
        self.__client = client
        self.__block = block

    @property
    def __url(self):
        return "api/oauth2/third/v1/export/user/list?productId="

    def get_url(self, use_back_url: bool = False) -> str:
        return CloudGwUrlUtils.get_cloud_gw_url_by_region(self.__client.get_credential().get_region(),
                                                          use_back_url) + self.__url + \
               self.__client.get_credential().get_project_id() + \
               "&block=" + str(self.__block)

    async def get_headers(self):
        token = await self.__client.get_credential().get_access_token()
        return {"client_id": self.__client.get_credential().get_client_id(), "Authorization": "Bearer " + token}

    @staticmethod
    def get_body():
        return None
