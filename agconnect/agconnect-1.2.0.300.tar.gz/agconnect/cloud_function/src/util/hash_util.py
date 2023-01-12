# Copyright (c) Huawei Technologies Co., Ltd. 2022. All rights reserved.

import hashlib


class HashUtil:
    __BASE_62 = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    __DIVISOR = 62
    __BIT_MAX = 61

    @staticmethod
    def hash(team_id: str, product_id: str) -> str:
        format_str: str = "agc:" + team_id + "@" + product_id
        hex_res = hashlib.md5(format_str.encode()).hexdigest()
        hex_res = '0x' + hex_res
        res = HashUtil.__encode_func(int(hex_res, 16))
        return res

    @classmethod
    def __encode_func(cls, num) -> str:
        res: str = ''
        while num > cls.__BIT_MAX:
            remainder = num % cls.__DIVISOR
            res = cls.__BASE_62[remainder] + str(res)
            num = num // cls.__DIVISOR
        res = cls.__BASE_62[num] + str(res)
        return res
