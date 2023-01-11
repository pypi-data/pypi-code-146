#!/usr/bin/env python3
# coding = utf8
"""
@ Author : ZeroSeeker
@ e-mail : zeroseeker@foxmail.com
@ GitHub : https://github.com/ZeroSeeker
@ Gitee : https://gitee.com/ZeroSeeker
"""
from lazysdk import lazyrequests
import requests


def login(
        username: str,
        password: str
):
    """
    使用账号密码登录系统
    :param username: 账号
    :param password: 密码
    :return:
    登录成功返回：{'code': 200, 'data': {'isFinance': 0}}
    登录失败返回：{'code': 500, 'message': '密码校验失败'}
    """
    url = 'https://bi.reading.163.com/login'
    method = 'POST'
    json_data = {
        'userName': username,
        'password': password
    }
    response = requests.request(
        method=method,
        url=url,
        json=json_data
    )
    return {'response': response.json(), 'cookie': response.headers.get('Set-Cookie')}


def get_apps(
        cookie: str,
        page: int = 1
):
    """
    获取子账号信息
    :param cookie: cookie字符串
    :param page: 页码
    :return:
    """
    url = 'https://bi.reading.163.com/open/query'
    method = 'GET'
    params = {
        'page': page
    }
    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Connection": "keep-alive",
        "Cookie": cookie,
        "Host": "bi.reading.163.com",
        "Referer": "https://bi.reading.163.com/spa/open",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:106.0) Gecko/20100101 Firefox/106.0",
        "X-Requested-With": "XMLHttpRequest"
    }
    return lazyrequests.lazy_requests(
        method=method,
        url=url,
        params=params,
        headers=headers,
        return_json=True
    )
