# Copyright (c) Huawei Technologies Co., Ltd. 2022. All rights reserved.

import json
import os
import time
import urllib.parse
from abc import ABC
from typing import Union

import jwt
from Crypto import Random
from Crypto.PublicKey import RSA

from agconnect.auth_server import AGCAuthException, AuthErrorCode
from agconnect.auth_server.src.backend.auth_backend import AuthBackend
from agconnect.auth_server.src.entity.auth_access_token import AuthAccessToken
from agconnect.auth_server.src.entity.user_import_export_result import UserImportExportResult
from agconnect.auth_server.src.jwt.agc_auth_jwt import AGCAuthJwt
from agconnect.auth_server.src.jwt.agc_auth_jwttoken import AGCAuthJwtToken
from agconnect.auth_server.src.jwt.agc_auth_public_key_manager import AGCAuthPublicKeyManager
from agconnect.auth_server.src.jwt.agc_auth_rsa_verifier import AGCAuthRsaVerifier
from agconnect.auth_server.src.jwt.rsa_key_pair import RSAKeyPair
from agconnect.auth_server.src.request.export_user_list_req import ExportUserListReq
from agconnect.auth_server.src.request.export_user_req import ExportUserReq
from agconnect.auth_server.src.request.import_export_user_info import ImportExportUserInfo, UserInfoList
from agconnect.auth_server.src.request.import_user_req import ImportUserReq
from agconnect.auth_server.src.request.revoke_token_req import RevokeTokenReq
from agconnect.auth_server.src.request.verify_token_req import VerifyTokenReq
from agconnect.auth_server.src.response.auth_operate_rsp import AuthOperateRsp
from agconnect.auth_server.src.response.export_user_list_rsp import ExportUserListRsp
from agconnect.auth_server.src.response.export_user_rsp import ExportUserRsp
from agconnect.auth_server.src.response.import_success_user import ImportSuccessUser
from agconnect.auth_server.src.response.import_user_rsp import ImportUserRsp
from agconnect.auth_server.src.response.verify_token import VerifyTokenRsp
from agconnect.auth_server.src.service.agc_auth import AGCAuth
from agconnect.auth_server.src.service.impl.agc_auth_service import AGCAuthService
from agconnect.auth_server.src.utils.auth_service_api_util import AuthServiceApiUtil
from agconnect.auth_server.src.utils.key_header_util import KeyHeaderUtil
from agconnect.common_server import logger, ConfigService
from agconnect.common_server.src.agc_client.agc_client import AGCClient
from agconnect.common_server.src.service.agc_service import AGCService

SERVICE_NAME = 'AUTH'


class AGCAuthServiceImpl(AGCAuthService, AGCService, ABC):
    RSA_KEY_SIZE = 3072
    ONE_HOUR_SECOND = 3600
    IMPORT_USER_LIMIT_SIZE = 10
    HTTP_STATUS_UNAUTHORIZED = 401
    THIRD_ACCESS_TOKEN_AUTH_FAILED = 205524994
    INVALID_ACCESS_TOKEN = 203817985
    EXPIRED_TOKEN = 203818357
    REVOKE_TOKEN = 203818359
    client: Union[AGCClient, None]

    def sign(self, uid: str, display_name: str = None, photo_url: str = "", private_key: str = ""):
        logger.info("do sign")
        AuthServiceApiUtil.check_credential(self.client)
        if not uid:
            raise AGCAuthException(AuthErrorCode.UID_IS_INVALID, self.client.get_name())
        if not private_key:
            raise AGCAuthException(AuthErrorCode.SIGN_PRIVATE_KEY_IS_INVALID, self.client.get_name())
        exp_time = round(time.time()) + AGCAuthServiceImpl.ONE_HOUR_SECOND * ConfigService.get_service(
            "AUTH").get_config_value("jwt_expires_time")
        try:
            decode_photo_url = urllib.parse.unquote(photo_url)
        except Exception as e:
            raise AGCAuthException(AuthErrorCode.PHOTO_URL_INVALID, self.client.get_name(), e) from e

        payload = {
            "uid": uid,
            "photoUrl": decode_photo_url,
            "exp": exp_time,
            "displayName": display_name
        }
        header = {
            "alg": "PS256",
            "typ": "JWT"
        }
        try:
            jwt_token = jwt.encode(payload, private_key,
                                   algorithm="PS256", headers=header)
            return AGCAuthJwtToken(jwt_token, exp_time)
        except Exception as e:
            raise AGCAuthException(AuthErrorCode.FAILED_TO_SIGN_JWT,
                                   self.client.get_name(), e) from e

    def generate_keys(self):
        logger.info("generating key")
        AuthServiceApiUtil.check_credential(self.client)
        try:
            random_generator = Random.new().read
            key = RSA.generate(AGCAuthServiceImpl.RSA_KEY_SIZE, random_generator)
            private_key, public_key = key, key.publickey()

            public_key_res = public_key.export_key().decode("utf-8")
            private_key_res = private_key.export_key(pkcs=8).decode("utf-8")

            return RSAKeyPair(public_key_res, private_key_res)
        except Exception as e:
            raise AGCAuthException(AuthErrorCode.FAILED_TO_GENERATE_RSA_KEY_PAIR, self.client.get_name(), e) from e

    def generate_raw_keys(self):
        logger.info("generating key")
        AuthServiceApiUtil.check_credential(self.client)
        try:
            random_generator = Random.new().read
            key = RSA.generate(AGCAuthServiceImpl.RSA_KEY_SIZE, random_generator)
            private_key, public_key = key, key.publickey()
            public_key_res = KeyHeaderUtil.remove_wrap(
                KeyHeaderUtil.remove_public_key_header_and_end(public_key.export_key().decode("utf-8")), True)
            private_key_res = KeyHeaderUtil.remove_wrap(
                KeyHeaderUtil.remove_private_key_header_and_end(private_key.export_key().decode("utf-8")), True)

            return RSAKeyPair(public_key_res, private_key_res)
        except Exception as e:
            raise AGCAuthException(AuthErrorCode.FAILED_TO_GENERATE_RSA_KEY_PAIR, self.client.get_name(), e) from e

    async def import_user_data(self, file_path: str) -> UserImportExportResult:
        logger.info("do userdata import")
        AuthServiceApiUtil.check_credential(self.client)
        AuthServiceApiUtil.check_read_file_path(file_path, self.client)
        total_list = self.__read_import_users(file_path)
        if total_list is None or len(total_list) == 0:
            raise AGCAuthException(AuthErrorCode.INVALID_IMPORT_USER_DATA, self.client.get_name())
        if len(total_list) > ConfigService.get_service("AUTH").get_config_value("import_user_limit_size"):
            raise AGCAuthException(AuthErrorCode.IMPORT_USER_DATA_OVER_LIMIT_SIZE, self.client.get_name())
        partition_list = []
        success_user_list: [ImportSuccessUser] = []
        for i in range(0, len(total_list), AGCAuthServiceImpl.IMPORT_USER_LIMIT_SIZE):
            partition_list.append(total_list[i:i + AGCAuthServiceImpl.IMPORT_USER_LIMIT_SIZE])
        for partition in partition_list:
            req: ImportUserReq = ImportUserReq(partition, self.client)
            response: ImportUserRsp = ImportUserRsp()
            try:
                response = await AuthBackend.post(req, response, True)
            except AGCAuthException as e:
                raise AGCAuthException(AuthErrorCode.IMPORT_USER_FAILED,
                                       self.client.get_name(),
                                       e) from None

            if response.get_ret().get_code() == 0:
                if len(response.get_imported_users()) > 0:
                    success_user_list.extend(response.get_imported_users())
            else:
                raise AGCAuthException(AuthErrorCode.IMPORT_USER_FAILED,
                                       self.client.get_name(), extra=response.get_ret().get_msg())
        res = self.__get_export_success_fail_list(total_list, success_user_list)
        logger.info("importUserData end")
        return UserImportExportResult(res[0], res[1])

    async def export_user_data(self, file_path: str) -> UserImportExportResult:
        logger.info("do userdata export")
        AuthServiceApiUtil.check_credential(self.client)
        AuthServiceApiUtil.check_write_file_path(file_path, self.client)
        block_rap = await self.__send_request_get_block_user_list(0)
        total_block = block_rap.get_total_block()
        uid_list = block_rap.get_uids()
        if uid_list is None or len(uid_list) == 0:
            return UserImportExportResult([], [])
        success_list = []
        export_user_info_list = []
        if total_block > 0:
            for i in range(1, total_block):
                iter_block_rsp = await self.__send_request_get_block_user_list(i)
                iter_uid_list = iter_block_rsp.get_uids()
                if len(iter_uid_list) != 0:
                    uid_list.append(*iter_uid_list)

        for uid in uid_list:
            export_user_rsp = await self.__send_request_get_export_user(uid)
            if export_user_rsp.get_user() is not None:
                if export_user_rsp.get_user() is not None:
                    export_user_info_list.append(export_user_rsp.get_user())
                if export_user_rsp.get_user().get_uid() is not None:
                    success_list.append(export_user_rsp.get_user().get_uid())
            else:
                logger.error(f"get export user info failed, uid {str(uid)}")
        self.__write_object_to_file(export_user_info_list, file_path)
        res = self.__get_import_success_fail_list(uid_list, success_list)
        logger.info("exportUserData end")
        return UserImportExportResult(res[0], res[1])

    async def revoke_refresh_tokens(self, uid: str):
        logger.info("revoke issued token")
        AuthServiceApiUtil.check_credential(self.client)
        if not uid:
            raise AGCAuthException(AuthErrorCode.REVOKE_REFRESH_UID_IS_NULL, self.client.get_name())
        else:
            req = RevokeTokenReq(uid, self.client)
            resp = AuthOperateRsp()
            try:
                await AuthBackend.post(req, resp, True)
            except AGCAuthException as e:
                raise AGCAuthException(AuthErrorCode.REVOKE_REFRESH_FAILED, self.client.get_name(),
                                       e.get_message()) from e

            logger.info("revoke token end")
        return

    async def verify_access_token(self, access_token: str, check_revoked: bool) -> AuthAccessToken:
        logger.info(f"verifyAccessToken begin, checkRevoked {str(check_revoked)}")
        AuthServiceApiUtil.check_credential(self.client)
        AuthServiceApiUtil.check_access_token(access_token, self.client)
        parsed_jwt = AGCAuthJwt.parse(access_token)
        alg = parsed_jwt.parse_alg()
        if alg is None:
            raise AGCAuthException(AuthErrorCode.ACCESS_ALG_IS_INVALID, self.client.get_name())
        elif 'HS512' in alg:
            verify_token_rsp = await self.do_token_verify_request(access_token)
            return self.__build_auth_access_token(verify_token_rsp)
        else:
            kid = parsed_jwt.parse_kid()
            if kid is None:
                raise AGCAuthException(AuthErrorCode.ACCESS_KID_IS_INVALID, self.client.get_name())

            public_key = await AGCAuthPublicKeyManager.get_public_key(kid, self.client)
            verify_res = AGCAuthRsaVerifier.verify(public_key, access_token, parsed_jwt.parse_alg(), self.client)
            if parsed_jwt.expire():
                raise AGCAuthException(AuthErrorCode.JWT_EXPIRE, self.client.get_name())
            if check_revoked:
                await self.do_token_verify_request(access_token)
            auth_access_token: AuthAccessToken = AuthAccessToken(verify_res)
            logger.info("verifyAccessToken end")
            return auth_access_token

    def initialize(self, client: AGCClient):
        self.client = client

    def get_service_name(self) -> str:
        return AGCAuth.SERVICE_NAME + "#" + self.client.get_name()

    @staticmethod
    def __read_import_users(file_path: str) -> [ImportExportUserInfo]:
        try:
            with open(file_path) as file:
                obj = json.load(file)
                res: [ImportExportUserInfo] = []
                if obj and obj.get('users') and isinstance(obj.get('users'), list):
                    for user in obj.get('users'):
                        info = ImportExportUserInfo()
                        info.construct_import_user_info(user)
                        res.append(info)
                    return res
        except AGCAuthException as e:
            logger.info("read import_users fail", e)
            return []
        return []

    @staticmethod
    def __get_export_success_fail_list(total_list: [ImportExportUserInfo],
                                       success_user_list: [ImportSuccessUser]) -> Union[list, list]:
        success_list: list = []
        fail_list: list = []
        for count, _ in enumerate(total_list):
            fail_list.append(total_list[count].get_uid())
        for count, _ in enumerate(success_user_list):
            success_list.append(success_user_list[count].get_import_uid())
            index = fail_list.index(success_user_list[count].get_import_uid())
            if index > -1:
                fail_list.pop(index)
        res: Union[list, list] = [[], []]
        res[0] = success_list
        res[1] = fail_list
        return res

    @staticmethod
    def __get_import_success_fail_list(total_list: [ImportExportUserInfo],
                                       success_user_list: [ImportSuccessUser]) -> Union[list, list]:
        success_list: list = []
        fail_list: list = []
        for user in total_list:
            fail_list.append(user)
        for i, _ in enumerate(success_user_list):
            success_list.append(success_user_list[i])
            if success_user_list[i] in fail_list:
                fail_list.pop(fail_list.index(success_user_list[i]))
        res: Union[list, list] = [[], []]
        res[0] = success_list
        res[1] = fail_list
        return res

    async def do_token_verify_request(self, access_token: str) -> VerifyTokenRsp:
        req: VerifyTokenReq = VerifyTokenReq(access_token, self.client)
        response: VerifyTokenRsp = VerifyTokenRsp()
        try:
            await AuthBackend.get(req, response, True)
        except AGCAuthException as e:
            if e.get_code() == AGCAuthServiceImpl.HTTP_STATUS_UNAUTHORIZED:
                raise AGCAuthException(AuthErrorCode.JWT_REVOKED,
                                       self.client.get_name(),
                                       e) from e
            raise AGCAuthException(AuthErrorCode.JWT_VERIFY_FAILED,
                                   self.client.get_name(),
                                   e) from e

        if response.get_ret().get_code() != 0:
            if response.get_ret().get_code() == AGCAuthServiceImpl.INVALID_ACCESS_TOKEN:
                raise AGCAuthException(AuthErrorCode.JWT_VERIFY_FAILED, self.client.get_name())
            if response.get_ret().get_code() == AGCAuthServiceImpl.EXPIRED_TOKEN:
                raise AGCAuthException(AuthErrorCode.JWT_EXPIRE,
                                       self.client.get_name())
            if response.get_ret().get_code() == AGCAuthServiceImpl.REVOKE_TOKEN:
                raise AGCAuthException(AuthErrorCode.JWT_REVOKED,
                                       self.client.get_name())
            if response.get_ret().get_code() == AGCAuthServiceImpl.THIRD_ACCESS_TOKEN_AUTH_FAILED:
                raise AGCAuthException(AuthErrorCode.JWT_REVOKED,
                                       self.client.get_name(), extra=response.get_ret().get_msg())

            raise AGCAuthException(AuthErrorCode.INVOKE_INTERFACE_FAIL,
                                   self.client.get_name(), extra=response.get_ret().get_msg())

        return response

    @staticmethod
    def __build_auth_access_token(rsp: VerifyTokenRsp):
        token = AuthAccessToken()
        token.set_sub(rsp.get_uid())
        token.set_aud(rsp.get_product_id())
        create_time = int(round(time.time()))
        if rsp.get_access_token() and rsp.get_access_token().get_valid_period() is not None:
            token.set_exp(create_time + rsp.get_access_token().get_valid_period())
        token.set_iat(create_time)
        if rsp.get_product_id():
            token.set_iss("https://agc.developer.huawei.com/" + rsp.get_product_id())
        return token

    def __write_object_to_file(self, export_user_info_list: [ImportExportUserInfo], file_path: str):
        if export_user_info_list and len(export_user_info_list) > 0:
            output_json = UserInfoList(export_user_info_list).to_json()
            try:
                file = os.open(file_path, os.O_RDWR | os.O_CREAT, 0o755)
                os.truncate(file, 0)
                os.write(file, json.dumps(output_json).encode())
                os.close(file)

            except AGCAuthException as e:
                raise AGCAuthException(AuthErrorCode.EXPORT_USER_TO_FILE_FAILED,
                                       self.client.get_name(), e) from e

    async def __send_request_get_block_user_list(self, block: int) -> ExportUserListRsp:
        req = ExportUserListReq(block, self.client)
        response = ExportUserListRsp()
        try:
            await AuthBackend.get(req, response, True)
        except AGCAuthException as e:
            raise AGCAuthException(AuthErrorCode.GET_BLOCK_USER_LIST_FAILED,
                                   self.client.get_name(),
                                   e) from e
        if response.get_ret().get_code() != 0:
            raise AGCAuthException(AuthErrorCode.GET_BLOCK_USER_LIST_FAILED,
                                   self.client.get_name(), extra=json.dumps(response.get_ret().get_msg()))
        return response

    async def __send_request_get_export_user(self, uid: str) -> ExportUserRsp:
        req: ExportUserReq = ExportUserReq(uid, self.client)
        response: ExportUserRsp = ExportUserRsp()
        try:
            await AuthBackend.get(req, response, True)
        except AGCAuthException as e:
            raise AGCAuthException(AuthErrorCode.GET_EXPORT_USER_FAILED,
                                   self.client.get_name(),
                                   e) from e
        if response.get_ret().get_code() != 0:
            raise AGCAuthException(AuthErrorCode.GET_EXPORT_USER_FAILED,
                                   self.client.get_name(), extra=json.dumps(response.get_ret().get_msg()))
        return response
