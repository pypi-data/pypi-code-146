# Copyright (c) Huawei Technologies Co., Ltd. 2022. All rights reserved.

import os
import stat

from agconnect.auth_server.src.error.agc_auth_exception import AGCAuthException
from agconnect.auth_server.src.error.agc_auth_error_message import AuthErrorCode
from agconnect.common_server import AGCClient


class AuthServiceApiUtil:
    JWT_FIELD_SIZE = 3

    @staticmethod
    def check_credential(client: AGCClient):
        if not client or not client.get_credential() or not client.get_credential().get_project_id():
            raise AGCAuthException(AuthErrorCode.CLIENT_INITIALIZE_FAILED, '')
        if not client.get_credential().get_region():
            raise AGCAuthException(AuthErrorCode.PROJECT_DO_NOT_SET_REGION, client.get_name())
        return True

    @staticmethod
    def check_read_file_path(file_path: str, client: AGCClient):
        if not file_path:
            raise AGCAuthException(AuthErrorCode.INVALID_IMPORT_USER_FILE, client.get_name())
        if not os.path.exists(file_path):
            raise AGCAuthException(AuthErrorCode.INVALID_IMPORT_USER_FILE, client.get_name())
        l_stat_result = os.stat(file_path)
        if not stat.S_ISREG(l_stat_result.st_mode):
            raise AGCAuthException(AuthErrorCode.INVALID_IMPORT_USER_FILE, client.get_name())
        try:
            os.access(file_path, os.R_OK)
        except Exception as e:
            raise AGCAuthException(AuthErrorCode.INVALID_ACCESS_IMPORT_USER_FILE) from e

    @staticmethod
    def check_write_file_path(file_path: str, client: AGCClient):
        if not file_path:
            raise AGCAuthException(AuthErrorCode.EXPORT_USER_DATA_FILEPATH_IS_INVALID, client.get_name())
        if os.path.exists(file_path):
            l_stat_result = os.stat(file_path)
            if not stat.S_ISREG(l_stat_result.st_mode):
                raise AGCAuthException(AuthErrorCode.EXPORT_USER_DATA_FILEPATH_IS_INVALID, client.get_name())
            try:
                os.access(file_path, os.W_OK)
            except Exception as e:
                raise AGCAuthException(AuthErrorCode.INVALID_ACCESS_EXPORT_USER_FILE, client.get_name()) from e
        else:
            dir_path = os.path.join(file_path, '..')
            if not os.path.exists(dir_path):
                raise AGCAuthException(AuthErrorCode.EXPORT_USER_FILE_DIR_NOT_EXIST, client.get_name())
        return True

    @staticmethod
    def check_access_token(access_token: str, client: AGCClient):
        if not access_token:
            raise AGCAuthException(AuthErrorCode.VERIFY_ACCESS_IS_NULL, client.get_name())
        if AuthServiceApiUtil.JWT_FIELD_SIZE != len(access_token.split(".")):
            raise AGCAuthException(AuthErrorCode.ACCESS_INVALID_FORMAT, client.get_name())
