# Copyright (c) Huawei Technologies Co., Ltd. 2022. All rights reserved.

import json

from agconnect.auth_server.src.request.import_export_user_info import ImportExportUserInfo, UserInfoList
from agconnect.common_server import RequestConstructor, CloudGwUrlUtils, AGCClient


class ImportUserReq(RequestConstructor):
    def __init__(self, import_user_info_list: [ImportExportUserInfo], client: AGCClient):
        self.__client = client
        self.__import_user_info_list = import_user_info_list

    @property
    def __url(self):
        return "api/oauth2/third/v1/import/user?productId="

    def get_url(self, use_back_url: bool = False) -> str:
        url = CloudGwUrlUtils.get_cloud_gw_url_by_region(self.__client.get_credential().get_region(),
                                                         use_back_url)
        return url + self.__url + self.__client.get_credential().get_project_id()

    async def get_headers(self):
        token = await self.__client.get_credential().get_access_token()
        return {"client_id": self.__client.get_credential().get_client_id(), "Authorization": "Bearer " + token}

    def get_body(self):
        users_json = UserInfoList(self.__import_user_info_list).to_json()
        users_json.update({"algorithm": None, "algorithmKey": None, "algorithmParam": None})
        return json.dumps(users_json, default=lambda o: o.to_json)
