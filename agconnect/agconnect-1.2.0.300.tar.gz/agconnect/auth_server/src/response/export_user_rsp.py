# Copyright (c) Huawei Technologies Co., Ltd. 2022. All rights reserved.

from agconnect.auth_server.src.request.import_export_user_info import ImportExportUserInfo
from agconnect.auth_server.src.request.provider_info import ProviderInfo
from agconnect.common_server import BaseResponse


class ExportUserRsp(BaseResponse):
    def __init__(self):
        self.__block_no = None
        self.__user = None

    def get_block_no(self):
        return self.__block_no

    def set_block_no(self, block_no):
        self.__block_no = block_no

    def get_user(self):
        return self.__user

    def set_user(self, user: ImportExportUserInfo):
        self.__user = user

    def construct_response(self, response):
        self.__block_no = response.get("blockNo")
        if response.get("user"):
            self.__user = ImportExportUserInfo()
            self.__user.set_uid(response.get("user").get("uid"))
            self.__user.set_display_name(response.get("user").get("displayName"))
            self.__user.set_photo_url(response.get("user").get("photoUrl"))
            self.__user.set_email(response.get("user").get("email"))
            self.__user.set_email_verified(response.get("user").get("emailVerified"))
            self.__user.set_phone_number(response.get("user").get("phoneNumber"))
            self.__user.set_created_at(response.get("user").get("createdAt"))
            self.__user.set_last_signed_in_at(response.get("user").get("lastSignedAt"))
            self.__user.set_password_hash(response.get("user").get("passwordHash"))
            self.__user.set_salt(response.get("user").get("salt"))

            if response.get("user").get("providers") and isinstance(response.get("user").get("providers"), list):
                providers = []
                for user in response.get("user").get("providers"):
                    provider_info = ProviderInfo()
                    provider_info.set_provider_id(user.get("providerId"))
                    provider_info.set_raw_id(user.get("rawId"))
                    provider_info.set_photo_url(response.get(user.get("photoUrl")))
                    provider_info.set_display_name(user.get("displayName"))
                    provider_info.set_open_id(user.get("openId"))
                    providers.append(provider_info)
                self.__user.set_providers(providers)
