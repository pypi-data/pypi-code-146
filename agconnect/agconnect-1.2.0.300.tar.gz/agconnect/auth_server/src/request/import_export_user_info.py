# Copyright (c) Huawei Technologies Co., Ltd. 2022. All rights reserved.
import json

from agconnect.auth_server.src.request.provider_info import ProviderInfo


class ImportExportUserInfo:
    def __init__(self):
        self.uid = None
        self.display_name = None
        self.photo_url = None
        self.email = None
        self.email_verified = None
        self.phone_number = None
        self.created_at = None
        self.last_signed_in_at = None
        self.password_hash = None
        self.salt = None
        self.providers: [ProviderInfo] = []

    def construct_import_user_info(self, obj):
        if not obj or (not obj.get("localID") and not obj.get("uid")):
            return False

        if obj.get("localID"):
            self.uid = obj.get("localID")

        if obj.get("uid"):
            self.uid = obj.get("uid")

        self.display_name = obj.get("displayName")
        self.photo_url = obj.get("photoUrl")
        self.email = obj.get("email")
        self.email_verified = obj.get("emailVerified")
        self.phone_number = obj.get("phoneNumber")
        self.created_at = obj.get("createdAt")
        self.last_signed_in_at = obj.get("lastSignedInAt")
        self.password_hash = obj.get("passwordHash")
        self.salt = obj.get("salt")
        self.providers = []
        provider_user_info = obj.get("providerUserInfo")
        if isinstance(provider_user_info, list) and len(provider_user_info) > 0:
            provider_user_infos: [ProviderInfo] = []
            for user_info in provider_user_info:
                provider_info = ProviderInfo()
                provider_info.set_provider_id(user_info.get("providerIdd"))
                provider_info.set_raw_id(user_info.get("rawId"))
                provider_info.set_photo_url(user_info.get("photoUrl"))
                provider_info.set_display_name(user_info.get("displayName"))
                provider_info.set_open_id(user_info.get("openId"))
                provider_user_infos.append(provider_info)
            self.providers = provider_user_infos

        providers = obj.get("providers")
        if isinstance(providers, list) and len(providers) > 0:
            provider_user_info: [ProviderInfo] = []
            for provider in providers:
                provider_info = ProviderInfo()
                provider_info.set_provider_id(provider.get("providerId"))
                provider_info.set_raw_id(provider.get("rawId"))
                provider_info.set_photo_url(provider.get("photoUrl"))
                provider_info.set_display_name(provider.get("displayName"))
                provider_info.set_open_id(provider.get("openId"))
                provider_user_info.append(provider_info)
            self.providers = provider_user_info

        return True

    def get_uid(self):
        return self.uid

    def set_uid(self, uid: str):
        self.uid = uid

    def get_display_name(self):
        return self.display_name

    def set_display_name(self, display_name: str):
        self.display_name = display_name

    def get_photo_url(self):
        return self.photo_url

    def set_photo_url(self, photo_url: str):
        self.photo_url = photo_url

    def get_email(self):
        return self.email

    def set_email(self, email: str):
        self.email = email

    def get_email_verified(self):
        return self.email_verified

    def set_email_verified(self, email_verified: str):
        self.email_verified = email_verified

    def get_phone_number(self):
        return self.phone_number

    def set_phone_number(self, phone_number: str):
        self.phone_number = phone_number

    def get_created_at(self):
        return self.created_at

    def set_created_at(self, created_at: str):
        self.created_at = created_at

    def get_last_signed_in_at(self):
        return self.last_signed_in_at

    def set_last_signed_in_at(self, last_signed_in_at: str):
        self.last_signed_in_at = last_signed_in_at

    def get_password_hash(self):
        return self.password_hash

    def set_password_hash(self, password_hash: str):
        self.password_hash = password_hash

    def get_salt(self):
        return self.salt

    def set_salt(self, salt: str):
        self.salt = salt

    def get_providers(self):
        return self.providers

    def set_providers(self, providers: [ProviderInfo]):
        self.providers = providers

    def __iter__(self):
        yield from {
            "uid": self.uid,
            "displayName": self.display_name,
            "photoUrl": self.photo_url,
            "email": self.email,
            "emailVerified": self.email_verified,
            "phoneNumber": self.phone_number,
            "createdAt": self.created_at,
            "lastSignedInAt": self.last_signed_in_at,
            "passwordHash": self.password_hash,
            "salt": self.salt,
            "providers": self.providers
        }.items()

    def __str__(self):
        return json.dumps(self.to_json())

    def __repr__(self):
        return self.__str__()

    def to_json(self):
        json_str = {
            "uid": self.uid,
            "displayName": self.display_name,
            "photoUrl": self.photo_url,
            "email": self.email,
            "emailVerified": self.email_verified,
            "phoneNumber": self.phone_number,
            "createdAt": self.created_at,
            "lastSignedInAt": self.last_signed_in_at,
            "passwordHash": self.password_hash,
            "salt": self.salt,
        }
        prov_list = []
        for provider in self.providers:
            prov_list = [provider.to_json()]
        json_str["providers"] = prov_list
        return json_str

    @staticmethod
    def from_json(json_dct):
        return ImportExportUserInfo.construct_import_user_info(json_dct)


class UserInfoList:
    def __init__(self, infos: [ImportExportUserInfo]):
        self.__KEY = "users"
        self.infos = infos

    def __iter__(self):
        yield from {
            "users": self.infos,
        }.items()

    def __str__(self):
        return json.dumps(self.to_json())

    def __repr__(self):
        return self.__str__()

    def to_json(self):
        result = {}
        info_json = []
        for info in self.infos:
            if info is not None:
                info_json.append(info.to_json())
        result[self.__KEY] = info_json
        return result
