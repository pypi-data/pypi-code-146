#!/usr/bin/env python3
# coding = utf8
"""
@ Author : ZeroSeeker
@ e-mail : zeroseeker@foxmail.com
@ GitHub : https://github.com/ZeroSeeker
@ Gitee : https://gitee.com/ZeroSeeker
"""
from lazysdk import lazyrandom
from lazysdk import lazytime
import hashlib


def make_sign(
    token,
    client_id
):
    """
    生成签名
    :param token: （只参与签名）系统随机生成，由书城方提供
    :param client_id: 系统分配的客户端ID，由书城方提供
    :return:
    """
    timestamp = lazytime.get_timestamp()
    nonce = lazyrandom.random_str()
    sign = hashlib.sha1(f"{token}{timestamp}{client_id}{nonce}".encode('UTF-8')).hexdigest()
    sign_params = {
        'client_id': client_id,
        'timestamp': timestamp,
        'nonce': nonce,
        'signaure': sign
    }
    return sign_params
