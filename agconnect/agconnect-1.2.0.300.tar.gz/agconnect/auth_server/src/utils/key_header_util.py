# Copyright (c) Huawei Technologies Co., Ltd. 2022. All rights reserved.

import re


class KeyHeaderUtil:
    PUBLIC_KEY_BEGIN = "-----BEGIN PUBLIC KEY-----"
    PUBLIC_KEY_END = "-----END PUBLIC KEY-----"

    PRIVATE_KEY_BEGIN = "-----BEGIN PRIVATE KEY-----"
    PRIVATE_KEY_END = "-----END PRIVATE KEY-----"

    PRIVATE_RSA_KEY_BEGIN = "-----BEGIN RSA PRIVATE KEY-----"
    PRIVATE_RSA_KEY_END = "-----END RSA PRIVATE KEY-----"

    CERTIFICATE_BEGIN = "-----BEGIN CERTIFICATE-----"
    CERTIFICATE_END = "-----END CERTIFICATE-----"

    WRAP = "\n"
    WRAP_EXP = '/\n/g'

    @staticmethod
    def add_public_key_header_and_end(public_key: str):
        if public_key:
            res = public_key
            if not res.startswith(KeyHeaderUtil.PUBLIC_KEY_BEGIN):
                res = KeyHeaderUtil.PUBLIC_KEY_BEGIN + KeyHeaderUtil.WRAP + res
            if not res.endswith(KeyHeaderUtil.PUBLIC_KEY_END):
                res = res + KeyHeaderUtil.WRAP + KeyHeaderUtil.PUBLIC_KEY_END
            return res
        return public_key

    @staticmethod
    def add_private_key_header_and_end(private_key: str):
        if private_key:
            res = private_key
            if not res.startswith(KeyHeaderUtil.PRIVATE_KEY_BEGIN):
                res = KeyHeaderUtil.PRIVATE_KEY_BEGIN + KeyHeaderUtil.WRAP + res
            if not res.endswith(KeyHeaderUtil.PRIVATE_KEY_END):
                res = res + KeyHeaderUtil.WRAP + KeyHeaderUtil.PRIVATE_KEY_END
            return res
        return private_key

    @staticmethod
    def remove_public_key_header_and_end(public_key: str):
        if public_key:
            res = public_key
            res = res.replace(KeyHeaderUtil.PUBLIC_KEY_BEGIN, "")
            res = res.replace(KeyHeaderUtil.PUBLIC_KEY_END, "")
            return res
        return public_key

    @staticmethod
    def remove_private_key_header_and_end(private_key: str):
        if private_key:
            res = private_key
            res = res.replace(KeyHeaderUtil.PRIVATE_KEY_BEGIN, "")
            res = res.replace(KeyHeaderUtil.PRIVATE_KEY_END, "")
            res = res.replace(KeyHeaderUtil.PRIVATE_RSA_KEY_BEGIN, "")
            res = res.replace(KeyHeaderUtil.PRIVATE_RSA_KEY_END, "")
            return res
        return private_key

    @staticmethod
    def decode_public_key(public_key):
        if public_key:
            new_public_key = public_key.replace(KeyHeaderUtil.CERTIFICATE_BEGIN, KeyHeaderUtil.PUBLIC_KEY_BEGIN)
            new_public_key = new_public_key.replace(KeyHeaderUtil.CERTIFICATE_END, KeyHeaderUtil.PUBLIC_KEY_END)
            return new_public_key
        return public_key

    @staticmethod
    def remove_wrap(str_param: str, default=False):
        if default:
            return re.sub(KeyHeaderUtil.WRAP, "", str_param)
        if len(str_param) > 0:
            return re.sub(KeyHeaderUtil.WRAP_EXP, "", str_param)
        else:
            return str_param
