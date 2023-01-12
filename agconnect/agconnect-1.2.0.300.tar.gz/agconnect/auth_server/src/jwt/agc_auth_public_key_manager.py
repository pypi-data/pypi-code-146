# Copyright (c) Huawei Technologies Co., Ltd. 2022. All rights reserved.

import json

from agconnect.auth_server.src.backend.auth_backend import AuthBackend
from agconnect.auth_server.src.error.agc_auth_exception import AGCAuthException
from agconnect.auth_server.src.error.agc_auth_error_message import AuthErrorCode
from agconnect.auth_server.src.request.public_key_req import PublicKeyReq
from agconnect.auth_server.src.response.publickey_rsp import PublickeyRsp
from agconnect.common_server.src.agc_client.agc_client import AGCClient


class AGCAuthPublicKeyManager:
    @staticmethod
    async def get_public_key(kid: str, client: AGCClient) -> str:
        public_key_req = PublicKeyReq()
        public_key_rsp = PublickeyRsp()
        try:
            await AuthBackend.get(public_key_req, public_key_rsp, False, True)
        except Exception as e:
            raise AGCAuthException(AuthErrorCode.GET_PUBLIC_KEY_FAILED, client.get_name(),
                                   e) from e

        if public_key_rsp.get_ret().get_code() != 0:
            raise AGCAuthException(AuthErrorCode.GET_PUBLIC_KEY_FAILED, client.get_name(),
                                   extra=json.loads(public_key_rsp.get_ret()))
        keys = public_key_rsp.get_public_key()
        if keys.get(kid):
            return keys.get(kid)
        else:
            raise AGCAuthException(AuthErrorCode.GET_PUBLIC_KEY_FAILED, client.get_name(),
                                   extra="public key for kid not exist.")
