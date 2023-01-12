# Copyright (c) Huawei Technologies Co., Ltd. 2022. All rights reserved.

from abc import ABCMeta, abstractmethod

from agconnect.auth_server.src.entity import UserImportExportResult
from agconnect.auth_server.src.jwt.agc_auth_jwttoken import AGCAuthJwtToken
from agconnect.auth_server.src.jwt.rsa_key_pair import RSAKeyPair
from agconnect.common_server.src.service import AGCService


class AGCAuthService(AGCService, metaclass=ABCMeta):
    """
    according payload and privatekey generate self account JWT
    """

    @abstractmethod
    def sign(self, uid: str, display_name: str, photo_url: str,
             private_key: str) -> AGCAuthJwtToken:
        pass

    """generate rsa pair key"""

    @abstractmethod
    def generate_keys(self) -> RSAKeyPair:
        pass

    @abstractmethod
    def generate_raw_keys(self) -> RSAKeyPair:
        pass

    """import user from firebase or agc"""

    @abstractmethod
    async def import_user_data(self, file_path: str) -> UserImportExportResult:
        pass

    """export users of agc project"""

    @abstractmethod
    async def export_user_data(self, file_path: str) -> UserImportExportResult:
        pass

    """This method to verify that the token is valid,ensure that the token is correctly signed"""

    @abstractmethod
    async def verify_access_token(self, access_token: str, check_revoked: bool):
        pass

    """If {@code checkRevoked} is set to true, this method will check the access token
     * has been revoke"""

    @abstractmethod
    async def revoke_refresh_tokens(self, uid: str):
        pass
