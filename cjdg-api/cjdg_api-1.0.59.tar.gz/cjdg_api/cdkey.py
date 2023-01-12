import requests
# from .base import base
from cjdg_open_api.base import base


class user(base):

    def __init__(self, token, app_secret=None):
        super().__init__(token, app_secret)

# 新增激活码
    def saveCdkey(self,data):
        api_name = "cdkey/saveCdkey"
        return self.request(api_name,data)
# 查询激活码
    def list(self,data):
        api_name = "cdkey/getCdkeyList"
        return self.request(api_name,data)

# 删除激活码
    def delete(self,data):
        api_name = "cdkey/delCdkey"
        return self.request(api_name,data)
# 新增激活码
    def numCdkey(self,data):
        api_name = "cdkey/numCdkey"
        return self.request(api_name,data)








