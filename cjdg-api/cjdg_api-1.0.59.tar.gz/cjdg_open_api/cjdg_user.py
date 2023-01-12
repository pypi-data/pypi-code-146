'''
@author: renqiukai
@Date: 2020-05-29 10:30:41
@Description: 
@LastEditTime: 2020-06-10 18:33:01
'''
import requests
from .base import base


class cjdgUser(base):

    def __init__(self, token, app_secret):
        super().__init__(token, app_secret)

    def create(self, data):
        api_name = "user/create"
        return self.request(api_name, data)

    def createBatch(self, data):
        data["api_name"] = "user/batchcreate"
        return self.request(**data)

    def list(self, data):
        api_name = "user/query"
        return self.request(api_name, data)

    def read(self, account):
        api_name = "user/query"
        data = {
            "accounts": account,
        }

        return self.request(api_name, data)

    def read_by_tel(self, tel):
        # 为啥同步不过去
        api_name = "user/query"
        data = {
            "tel": tel,
        }
        return self.request(api_name, data)

    def getUserIds(self, accounts):
        api_name = "user/query/byaccounts"
        data = {
            "accounts": accounts,
        }
        return self.request(api_name, data=data, method="POST")

    def update(self, data):
        api_name = "user/modifi"
        return self.request(api_name, data)

    def updateBatch(self, data):
        api_name = "user/batchmodifi"
        return self.request(api_name=api_name, json=data)

    def delete(self, data):
        api_name = "user/destroy"
        return self.request(api_name, data, safe=True, domain=True)

    def enabled(self, data):
        api_name = "user/enabled"
        return self.request(api_name, data)


