# Copyright (c) Huawei Technologies Co., Ltd. 2022. All rights reserved.

from agconnect.cloud_function.src.exception.agc_function_error_code import AGCFunctionErrorCode
from agconnect.cloud_function.src.exception.agc_function_exception import AGCFunctionException
from agconnect.cloud_function.src.util.hash_util import HashUtil
from agconnect.common_server.src.config import CloudGwUrlUtils
from agconnect.common_server.src.http_client.request_constructor import RequestConstructor


class FunctionRequest(RequestConstructor):
    SERVER_URL = "api/wisefunction/functions"
    use_back_url = False
    __body = None
    __http_trigger_url = ""

    def __init__(self, client, http_trigger_url="", body=None):
        super(FunctionRequest, self).__init__()
        self.__client = client
        self.__body = body
        self.__http_trigger_url = http_trigger_url

    def get_url(self, use_back_url=False):
        team_id = self.__client.get_credential().get_developer_id()
        product_id = self.__client.get_credential().get_project_id()
        app_id = HashUtil.hash(team_id=team_id, product_id=product_id)
        if self.__http_trigger_url and len(self.__http_trigger_url) > 0 and self.__http_trigger_url[0] != '/':
            self.__http_trigger_url = '/' + self.__http_trigger_url

        agc_gw_url = CloudGwUrlUtils.get_cloud_gw_url_by_region(self.__client.get_credential().get_region(),
                                                                use_back_url)
        if agc_gw_url:
            return agc_gw_url + FunctionRequest.SERVER_URL + '/' + app_id + self.__http_trigger_url
        raise AGCFunctionException(AGCFunctionErrorCode.GET_GW_URL_FAIL)

    async def get_headers(self):
        token = await self.__client.get_credential().get_access_token()
        return {"clientId": self.__client.get_credential().get_client_id(),
                "productId": self.__client.get_credential().get_project_id(),
                "Authorization": "Bearer " + token}

    def get_body(self):
        return self.__body
