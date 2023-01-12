# Copyright (c) Huawei Technologies Co., Ltd. 2022. All rights reserved.

from agconnect.common_server import BaseResponse


class PublickeyRsp(BaseResponse):
    def __init__(self):
        self.public_key = {}

    def get_public_key(self):
        return self.public_key

    def construct_response(self, response):
        self.public_key = response
