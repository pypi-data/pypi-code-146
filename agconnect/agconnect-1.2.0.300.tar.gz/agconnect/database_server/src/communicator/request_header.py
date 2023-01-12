# Copyright (c) Huawei Technologies Co., Ltd. 2022. All rights reserved.

from agconnect.database_server.src.utils.cloud_db_sdk_utils import CloudDBSdkUtils


class RequestHeader:
    __authorization: str
    __product_id: str
    __client_id: str
    __request_id: str
    __server_sdk_name: str
    __server_sdk_version: str

    def __init__(self, client_id: str, product_id: str):
        self.__authorization = ""
        self.__client_Id = client_id
        self.__product_id = product_id
        self.__request_id = ""
        self.__server_sdk_name = CloudDBSdkUtils.get_cloud_sdk_name()
        self.__server_sdk_version = CloudDBSdkUtils.get_cloud_sdk_version()

    def get_headers(self):
        return {
            "Accept": 'application/json, text/plain, */*',
            "Authorization": self.__authorization,
            "client_Id": self.__client_Id,
            "productId": self.__product_id,
            "requestId": self.__request_id,
            "serverSdkName": self.__server_sdk_name,
            "serverSdkVersion": self.__server_sdk_version,
        }

    def set_authorization(self, authorization: str) -> None:
        self.__authorization = authorization

    def set_request_id(self, request_id: str) -> None:
        self.__request_id = request_id
