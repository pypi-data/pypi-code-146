import requests
from .base import base


class cjdgAuth(base):

    def __init__(self, token, app_secret):
        super().__init__(token, app_secret)

    def getData(self, org_type: int, page: int = 1, rows: int = 10):
        data = {
            "type": org_type,
            "page": page,
            "rows": rows,
        }
        api_name = "org/getOrgWithinAuth"
        return self.request(api_name, data)

    def getCompanyData(self, org_type=2, page: int = 1, rows: int = 10):
        api_name = "org/getOrgWithinAuth"
        return self.getData(org_type, page, rows)

    def getDepData(self, org_type=3, page: int = 1, rows: int = 10):
        api_name = "org/getOrgWithinAuth"
        return self.getData(org_type, page, rows)

    def getAreaData(self, org_type=4, page: int = 1, rows: int = 10):
        api_name = "org/getOrgWithinAuth"
        return self.getData(org_type, page, rows)

    def getShopData(self, org_type=5, page: int = 1, rows: int = 10):
        api_name = "org/getOrgWithinAuth"
        return self.getData(org_type, page, rows)

    def getAgentData(self, org_type=6, page: int = 1, rows: int = 10):
        api_name = "org/getOrgWithinAuth"
        return self.getData(org_type, page, rows)

    def modifiRoleDetail(roleName: str, operation: str, accounts: str = None):
        data = {
            "roleName": roleName,
            # operation=add/del/delall
            "operation": operation,
        }
        if accounts:
            data["accounts"] = accounts
        api_name = "auth/modifiRoleDetail"
        return self.request(url, data)

    def clearRoleDetail(roleName: str):
        data = {
            "roleName": roleName,
            "operation": "delall",
        }
        return self.modifiRoleDetail(**data)

    def removeRoleDetail(roleName: str, login_name: str):
        data = {
            "roleName": roleName,
            "operation": "del",
            "accounts": login_name,
        }
        return self.modifiRoleDetail(**data)

    def addRoleDetail(roleName: str, login_name: str):
        data = {
            "roleName": roleName,
            "operation": "add",
            "accounts": login_name,
        }
        return self.modifiRoleDetail(**data)
