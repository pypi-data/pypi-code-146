import requests
from .base import base


class user(base):

    def __init__(self, token, app_secret=None):
        super().__init__(token, app_secret)


# 查询激活码
    def list(self,data):
        api_name = "cdkey/getCdkeyList"
        return self.request(api_name,data)


    def delete(self,data):
        api_name = "cdkey/delCdkey"
        return self.request(api_name,data)



