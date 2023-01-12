# Copyright (c) Huawei Technologies Co., Ltd. 2022. All rights reserved.

class UserImportExportResult:
    def __init__(self, success_list, fail_list):
        self.__success_users = len(success_list)
        self.__error_users = len(fail_list)
        self.__error_user_list = fail_list

    def get_success_count(self):
        return self.__success_users

    def get_error_users(self):
        return self.__error_users

    def get_error_users_list(self):
        return self.__error_user_list
