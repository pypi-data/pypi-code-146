# Copyright (c) Huawei Technologies Co., Ltd. 2022. All rights reserved.

import re
from typing import Any, Union

import jwt

from agconnect.auth_server.src.error.agc_auth_exception import AGCAuthException
from agconnect.auth_server.src.error.agc_auth_error_message import AuthErrorCode
from agconnect.common_server.src.agc_client.agc_client import AGCClient
from agconnect.auth_server.src.utils.key_header_util import KeyHeaderUtil


class AGCAuthRsaVerifier:
    @staticmethod
    def verify(public_key: str, token: str, alg: str, client: AGCClient) -> Any:
        new_public_key = KeyHeaderUtil.decode_public_key(public_key)
        try:
            if alg == "PS256":
                decode = jwt.decode(
                    token,
                    new_public_key,
                    algorithms=[alg, "RS256"],
                    options={"verify_exp": False, "verify_aud": False},
                )
            else:
                decode = jwt.decode(
                    token,
                    new_public_key,
                    algorithms=[alg],
                    options={"verify_exp": False, "verify_aud": False},
                )
            return decode
        except Exception as e:
            raise AGCAuthException(AuthErrorCode.ACCESS_VERIFY_FAILED,
                                   client.get_name(), e) from e

    @staticmethod
    def get_sub(payload: str) -> Union[str, None]:
        if payload:
            payload_array = payload.split(".")
            for _, ele in enumerate(payload_array):
                if [re.match(r"\"sub\":", ele)]:
                    sub = ele.replace(r"\"sub\":", "")
                    return sub
        return None

    @staticmethod
    def to_base64(base64_url: str):
        res = base64_url
        base64_pad_len = 4 - len(res) % 4
        if base64_pad_len != 4:
            for _i in range(base64_pad_len):
                res += '='
        return res.replace("\\-/g", "+").replace("/_/g", "/")
