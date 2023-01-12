# Copyright (c) Huawei Technologies Co., Ltd. 2022. All rights reserved.

from agconnect.common_server import BaseResponse


class ExportUserListRsp(BaseResponse):
    def __init__(self):
        self.__total_block = None
        self.__uids = None
        super().__init__()

    def get_total_block(self):
        return self.__total_block

    def set_total_block(self, total_block):
        self.__total_block = total_block

    def get_uids(self):
        return self.__uids

    def set_uids(self, uids: int):
        self.__uids = uids

    def construct_response(self, response):
        self.__total_block = None
        if response.get("totalBlock") is not None:
            self.__total_block = response.get("totalBlock")

        if response.get("uids") and isinstance(response.get("uids"), list):
            self.__uids = response.get("uids")
