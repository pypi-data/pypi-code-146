#!/usr/bin/env python3
# coding = utf8
"""
@ Author : ZeroSeeker
@ e-mail : zeroseeker@foxmail.com
@ GitHub : https://github.com/ZeroSeeker
@ Gitee : https://gitee.com/ZeroSeeker
"""
from lazysdk import lazyrequests
from lazysdk import lazyrandom
from lazysdk import lazytime
from lazysdk import lazymd5
"""
迈步书城（中文在线）开放接口SDK
"""


def make_sign(
        channel_id,
        sign_key
):
    """
    签名生成规则：字符串依次拼接：渠道号、随机字符串、时间戳、密钥,最后将将结果大写MD5
    :param channel_id: 渠道号
    :param sign_key: 密钥
    :return:
    """
    random_str = lazyrandom.random_str(str_length=20)
    time_stamp = lazytime.get_timestamp()
    sign = lazymd5.md5_str(f"{channel_id}{random_str}{time_stamp}{sign_key}").upper()
    return {'sign': sign, 'random_str': random_str, 'time_stamp': time_stamp}


def op_account(
        channel_id,
        sign_key,
        page_no: int = 1,
        page_size: int = 10,
        appids: list = None,
        start_time: str = None,
        end_time: str = None
):
    """
    经销商归属账号查询
    :param channel_id: 渠道id,参数示例：258
    :param sign_key:
    :param page_no: 页号,参数示例：100
    :param page_size: 每页条数,参数示例：100
    :param appids: appid,参数示例：["wx7be6602ae378fa74","wx1bcc9386cd0a4a24"]
    :param start_time: 开始时间,参数示例：2021-05-10 08:34:01
    :param end_time: 结束时间,参数示例：2021-05-11 07:51:11
    :return:
    """
    # ---------------- 相对固定设置 ----------------
    sign_res = make_sign(
        channel_id=channel_id,  # 渠道id
        sign_key=sign_key
    )
    body = dict()
    body['channelId'] = channel_id  # 渠道id
    body['signaure'] = sign_res['sign']  # 签名，生成规则见make_sign方法
    body['nonce'] = sign_res['random_str']  # 随机字符串
    body['timestamp'] = sign_res['time_stamp']  # 时间戳
    # ---------------- 相对固定设置 ----------------

    url = 'https://data.mbookcn.com/v1/open/api/account'
    body['pageNo'] = page_no
    body['pageSize'] = page_size
    if appids is not None:
        body['appids'] = appids
    if start_time is not None:
        body['startTime'] = start_time
    if end_time is not None:
        body['endTime'] = end_time
    return lazyrequests.lazy_requests(
        method='POST',
        url=url,
        json=body,
        return_json=True
    )


def op_wx_info(
        channel_id,
        sign_key,
        page_no: int = 1,
        page_size: int = 10,
        appids: list = None,
        start_time: str = None,
        end_time: str = None,
        account_id: int = None
):
    """
    公众号信息（获取公众号列表）
    :param channel_id: 渠道id,参数示例：258
    :param sign_key:
    :param page_no: 页号,参数示例：100
    :param page_size: 每页条数,参数示例：100
    :param appids: appid,参数示例：["wx7be6602ae378fa74","wx1bcc9386cd0a4a24"]
    :param start_time: 开始时间,参数示例：2021-05-10 08:34:01
    :param end_time: 结束时间,参数示例：2021-05-11 07:51:11
    :param account_id: 账号id,参数示例：301
    :return:
    """
    # ---------------- 相对固定设置 ----------------
    sign_res = make_sign(
        channel_id=channel_id,  # 渠道id
        sign_key=sign_key
    )
    body = dict()
    body['channelId'] = channel_id  # 渠道id
    body['signaure'] = sign_res['sign']  # 签名，生成规则见make_sign方法
    body['nonce'] = sign_res['random_str']  # 随机字符串
    body['timestamp'] = sign_res['time_stamp']  # 时间戳
    # ---------------- 相对固定设置 ----------------

    url = 'https://data.mbookcn.com/v1/open/api/wx-info'
    body['pageNo'] = page_no
    body['pageSize'] = page_size
    if appids is not None:
        body['appids'] = appids
    if start_time is not None:
        body['startTime'] = start_time
    if end_time is not None:
        body['endTime'] = end_time
    if account_id is not None:
        body['accountId'] = account_id
    return lazyrequests.lazy_requests(
        method='POST',
        url=url,
        json=body,
        return_json=True
    )


def op_user_info(
        channel_id,
        sign_key,
        page_no: int = 1,
        page_size: int = 10,
        appids: list = None,
        start_time: str = None,
        end_time: str = None
):
    """
    用户信息（获取用户列表）
    :param channel_id: 渠道id,参数示例：258
    :param sign_key:
    :param page_no: 页号,参数示例：100
    :param page_size: 每页条数,参数示例：100
    :param appids: appid,参数示例：["wx7be6602ae378fa74","wx1bcc9386cd0a4a24"]
    :param start_time: 开始时间,参数示例：2021-05-10 08:34:01
    :param end_time: 结束时间,参数示例：2021-05-11 07:51:11
    :return:
    """
    # ---------------- 相对固定设置 ----------------
    sign_res = make_sign(
        channel_id=channel_id,  # 渠道id
        sign_key=sign_key
    )
    body = dict()
    body['channelId'] = channel_id  # 渠道id
    body['signaure'] = sign_res['sign']  # 签名，生成规则见make_sign方法
    body['nonce'] = sign_res['random_str']  # 随机字符串
    body['timestamp'] = sign_res['time_stamp']  # 时间戳
    # ---------------- 相对固定设置 ----------------

    url = 'https://data.mbookcn.com/v1/open/api/user-info'
    body['pageNo'] = page_no
    body['pageSize'] = page_size
    if appids is not None:
        body['appids'] = appids
    if start_time is not None:
        body['startTime'] = start_time
    if end_time is not None:
        body['endTime'] = end_time
    return lazyrequests.lazy_requests(
        method='POST',
        url=url,
        json=body,
        return_json=True
    )


def op_recharge_info(
        channel_id,
        sign_key,
        page_no: int = 1,
        page_size: int = 10,
        appids: list = None,
        start_time: str = None,
        end_time: str = None,
        pay_status: int = 1,
        fetch_start_time: str = None,
        fetch_end_time: str = None
):
    """
    充值信息（获取充值列表）
    :param channel_id: 渠道id,参数示例：258
    :param sign_key:
    :param page_no: 页号,参数示例：100
    :param page_size: 每页条数,参数示例：100
    :param appids: appid,参数示例：["wx7be6602ae378fa74","wx1bcc9386cd0a4a24"]
    :param start_time: 开始时间,参数示例：2021-05-10 08:34:01
    :param end_time: 结束时间,参数示例：2021-05-11 07:51:11
    :param pay_status: 支付状态 0：未支付 1：已支付,参数示例：0
    :param fetch_start_time: 付款到账开始时间 传此值 开始时间可不传
    :param fetch_end_time: 付款到账结束时间 传此值 结束时间可不传
    :return:
    """
    # ---------------- 相对固定设置 ----------------
    sign_res = make_sign(
        channel_id=channel_id,  # 渠道id
        sign_key=sign_key
    )
    body = dict()
    body['channelId'] = channel_id  # 渠道id
    body['signaure'] = sign_res['sign']  # 签名，生成规则见make_sign方法
    body['nonce'] = sign_res['random_str']  # 随机字符串
    body['timestamp'] = sign_res['time_stamp']  # 时间戳
    # ---------------- 相对固定设置 ----------------

    url = 'https://data.mbookcn.com/v1/open/api/recharge-info'
    body['pageNo'] = page_no
    body['pageSize'] = page_size
    if appids is not None:
        body['appids'] = appids
    if start_time is not None:
        body['startTime'] = start_time
    if end_time is not None:
        body['endTime'] = end_time
    if pay_status is not None:
        body['payStatus'] = pay_status
    if fetch_start_time is not None:
        body['fetchStartTime'] = fetch_start_time
    if fetch_end_time is not None:
        body['fetchEndTime'] = fetch_end_time
    return lazyrequests.lazy_requests(
        method='POST',
        url=url,
        json=body,
        return_json=True
    )


def op_sub_chapter(
        channel_id,
        sign_key,
        page_no: int = 1,
        page_size: int = 10,
        appids: list = None,
        start_time: str = None,
        end_time: str = None
):
    """
    章节阅读记录（获取章节阅读记录列表）
    :param channel_id: 渠道id,参数示例：258
    :param sign_key:
    :param page_no: 页号,参数示例：100
    :param page_size: 每页条数,参数示例：100
    :param appids: appid,参数示例：["wx7be6602ae378fa74","wx1bcc9386cd0a4a24"]
    :param start_time: 开始时间,参数示例：2021-05-10 08:34:01
    :param end_time: 结束时间,参数示例：2021-05-11 07:51:11
    :return:
    """
    # ---------------- 相对固定设置 ----------------
    sign_res = make_sign(
        channel_id=channel_id,  # 渠道id
        sign_key=sign_key
    )
    body = dict()
    body['channelId'] = channel_id  # 渠道id
    body['signaure'] = sign_res['sign']  # 签名，生成规则见make_sign方法
    body['nonce'] = sign_res['random_str']  # 随机字符串
    body['timestamp'] = sign_res['time_stamp']  # 时间戳
    # ---------------- 相对固定设置 ----------------

    url = 'https://data.mbookcn.com/v1/open/api/sub-chapter'
    body['pageNo'] = page_no
    body['pageSize'] = page_size
    if appids is not None:
        body['appids'] = appids
    if start_time is not None:
        body['startTime'] = start_time
    if end_time is not None:
        body['endTime'] = end_time
    return lazyrequests.lazy_requests(
        method='POST',
        url=url,
        json=body,
        return_json=True
    )
