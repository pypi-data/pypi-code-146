# Copyright (c) Huawei Technologies Co., Ltd. 2022. All rights reserved.

from agconnect.auth_server.src.response.import_success_user import ImportSuccessUser
from agconnect.common_server import BaseResponse


class ImportUserRsp(BaseResponse):
    def __init__(self):
        self.__imported_users: ImportSuccessUser = []

    def get_imported_users(self):
        return self.__imported_users

    def set_imported_users(self, imported_users: ImportSuccessUser):
        self.__imported_users = imported_users

    def construct_response(self, response):
        self.__imported_users = []
        if response.get("importedUsers") and isinstance(response.get("importedUsers"), list):
            for user in response.get("importedUsers"):
                if user and user.get("uid") and user.get("importUid"):
                    user_info = ImportSuccessUser()
                    user_info.set_uid(user.get("uid"))
                    user_info.set_import_uid(user.get("importUid"))
                    self.__imported_users.append(user_info)
