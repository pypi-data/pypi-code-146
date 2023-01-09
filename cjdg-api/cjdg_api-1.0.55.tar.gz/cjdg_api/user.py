import requests
from .base import base


class user(base):

    def __init__(self, token, app_secret=None):
        super().__init__(token, app_secret)

# 查询用户
    def list(self,data):
        api_name = "shopguiderefshowref.jhtml?refIdParam=1"
        return self.request(api_name,data)

# 离职用户
    def delete(self,data):
        api_name = "userleaveOffice.jhtml"
        return self.request(api_name,data)
# 初始密码
    def userinitPassword(self,data):
        api_name = "userinitPassword.jhtml"
        # userId: 318384529
        return self.request(api_name,data)

    def get(self):
        api_name = "game/getUser"
        return self.request(api_name)

    def getGold(self):
        return self.get().get("gold")

    def signIn(self):
        api_name = "game/addNewUserSignin"
        return self.request(api_name)

    def signInOld(self):
        api_name = "game/addUserSignin"
        return self.request(api_name)

    def activate(self, cdkey):
        # 激活
        api_name = "game/activateEnterpriseAcc"
        data = {}
        data["cdkey"] = cdkey
        return self.request(api_name)

    def updatePassword(self, oldPassword, newPassword):
        # 激活
        api_name = "auth/updateUserPassword"
        data = {}
        data["oldPassword"] = oldPassword
        data["newPassword"] = newPassword
        return self.request(api_name)
