# Copyright (c) Huawei Technologies Co., Ltd. 2022. All rights reserved.

import json
from typing import Union

from agconnect.auth_server.src.entity.provider import Provider
from agconnect.auth_server.src.entity.token_provider_info import TokenProviderInfo


class AuthAccessToken:
    def __init__(self, obj=None, jsn: str = None):
        if jsn is not None:
            obj = json.loads(jsn)
        if obj:
            self.__name = obj.get("displayName")
            self.__picture = obj.get("photoUrl")
            self.__iss = obj.get("iss")
            self.__aud = obj.get("aud")
            self.__auth_time = obj.get("auth_time")
            self.__sub = str(obj.get("sub"))
            self.__iat = obj.get("iat")
            self.__exp = obj.get("exp")
            self.__email = obj.get("email")
            self.__phone = obj.get("phone")
            self.__email_verified = obj.get("email_verified")
            if obj.get("agc"):
                self.__provider_info = TokenProviderInfo()
                self.__provider_info.set_sign_in_provider(obj.get("agc").get("sign_in_provider"))
                if obj.get("agc").get("providers") and isinstance(obj.get("agc").get("providers"), list):
                    providers = []
                    for i in range(len(obj.get("agc").get("providers"))):
                        provider = Provider()
                        provider.set_provider(obj.get("agc").get("providers")[i].get("provider"))
                        provider.set_provider_uid(obj.get("agc").get("providers")[i].get("provider_uid"))
                        providers.append(provider)
                    self.__provider_info.set_providers(providers)

    def get_name(self) -> Union[str, None]:
        return self.__name

    def get_picture(self) -> Union[str, None]:
        return self.__picture

    def get_iss(self) -> Union[str, None]:
        return self.__iss

    def get_aud(self) -> Union[str, None]:
        return self.__aud

    def get_sub(self) -> Union[str, None]:
        return self.__sub

    def get_iat(self) -> Union[int, None]:
        return self.__iat

    def get_exp(self) -> Union[int, None]:
        return self.__iat

    def is_mail_verified(self) -> Union[bool, None]:
        return self.__email_verified

    def get_phone(self) -> Union[str, None]:
        return self.__phone

    def get_email(self) -> Union[str, None]:
        return self.__email

    def get_provider_info(self) -> Union[TokenProviderInfo, None]:
        return self.__provider_info

    def get_exp(self) -> Union[int, None]:
        return self.__exp

    def get_auth_time(self):
        return self.__auth_time

    def set_auth_time(self, auth_time):
        self.__auth_time = auth_time

    def set_name(self, name):
        self.__name = name

    def set_picture(self, picture):
        self.__picture = picture

    def set_iss(self, iss):
        self.__iss = iss

    def set_aud(self, aud):
        self.__aud = aud

    def set_exp(self, exp: int):
        self.__exp = exp

    def set_sub(self, sub):
        self.__sub = str(sub)

    def set_iat(self, iat):
        self.__iat = iat

    def set_email(self, email_param):
        self.__email = email_param

    def set_phone(self, phone):
        self.__phone = phone

    def set_provider_info(self, provider_info):
        self.__provider_info = provider_info

    def is_mail_verified(self, email_verified):
        self.__email_verified = email_verified
