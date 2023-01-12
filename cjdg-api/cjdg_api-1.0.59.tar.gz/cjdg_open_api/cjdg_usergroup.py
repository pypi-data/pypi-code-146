import requests
from .base import base


class cjdgUserGroup(base):

    def __init__(self, token, app_secret):
        super().__init__(token, app_secret)

    def operation(self, operationType, groupName, accounts=None):
        data = {
            "operationType": operationType,
            "groupName": groupName,
        }
        if accounts:
            data["accounts"] = accounts
        api_name = "user/operationGroupUser"
        return self.request(api_name, data)

    def add(self, group_name, login_name):
        data = {
            "operationType": "add",
            "groupName": group_name,
            "accounts": login_name,
        }
        return self.operation(**data)

    def delete(self, group_name, login_name):
        data = {
            "operationType": "del",
            "groupName": group_name,
            "accounts": login_name,
        }
        return self.operation(**data)

    def deleteAll(self, group_name):
        data = {
            "operationType": "delAll",
            "groupName": group_name,
        }
        return self.operation(**data)
