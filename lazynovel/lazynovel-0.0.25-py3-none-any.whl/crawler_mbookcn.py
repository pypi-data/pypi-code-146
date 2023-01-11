#!/usr/bin/env python3
# coding = utf8
"""
@ Author : ZeroSeeker
@ e-mail : zeroseeker@foxmail.com
@ GitHub : https://github.com/ZeroSeeker
@ Gitee : https://gitee.com/ZeroSeeker
"""
from lazysdk import lazyrequests
host = 'admin.bookphone.cn'


def get_user_role_list(
        token
):
    """
    获取子账号列表
    :param token:
    :return:
    """
    url = f'https://{host}/prod-api/v3/open/mng/role/getUserRoleList'
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Authorization": f"Bearer {token}",
        "Connection": "keep-alive",
        "Cookie": f"sidebarStatus=0; Admin-Token={token}",
        "Host": host,
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:104.0) Gecko/20100101 Firefox/104.0"
    }
    return lazyrequests.lazy_requests(
        method='GET',
        url=url,
        headers=headers,
        return_json=True
    )


def update_user_role_list(
        token,
        app_id
):
    """
    更新当前的子账号为目标账号
    :param token:
    :param app_id:
    :return:
    """
    url = f'https://{host}/prod-api/v3/open/mng/role/updateUserRoleList'
    params = {
        'appId': app_id
    }
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Authorization": f"Bearer {token}",
        "Connection": "keep-alive",
        "Cookie": f"sidebarStatus=0; Admin-Token={token}",
        "Host": host,
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:104.0) Gecko/20100101 Firefox/104.0"
    }
    return lazyrequests.lazy_requests(
        method='GET',
        url=url,
        headers=headers,
        params=params,
        return_json=True
    )


def make_scheduled_msg(
        token,
        msg_name: str,
        msg_type: int,
        send_time: int,
        text_content: str = None,
        picture_url: str = None,
        graphic_title: str = None,
        graphic_text: str = None,
        description: str = None,

        openid: str = ""
):
    """
    新建客服消息
    :param token:

    :param msg_name: 【必填】名称（标题）
    :param msg_type: 【必填】消息类型，0：文字消息，1：单条图文
    :param text_content: 【文字消息必填】消息正文（文字消息）
    :param send_time: 预约发送 时间，13位时间戳，默认时间戳*1000
    :param openid: 测试openid
    :param picture_url: 图片（地址）
    :param graphic_title: 【图文消息必填】标题（图文消息）
    :param graphic_text: 【图文消息必填】消息正文（图文消息）
    :param description: 【非必填】消息描述（图文消息）

    :return:
    """
    url = f'https://{host}/prod-api/v3/open/mng/scheduled-msg'
    data = {
        "msgType": msg_type,  # 消息类型，0：文字消息
        "msgName": str(msg_name),  # 名称（标题）
        "sendTime": send_time,  # 预约发送时间，13位时间戳，默认时间戳*1000
        "openid": openid,  # 测试openid
        "rule": {
            "sex": -1,
            "op": -1,
            "recharge": -1,
            "coinType": -1,
            "subStart": -1,
            "subEnd": -1,
            "prefer": -1,
            "coinAmount": -1,
            "isVip": -1,
            "times": []
        },  # 设置标签
        "sendCount": 0,
        "status": 0
    }
    if msg_type == 0:
        data['title'] = text_content  # 消息正文
    elif msg_type == 1:
        data['pictureUrl'] = picture_url
        data['title'] = graphic_title  # 标题
        data['url'] = graphic_text
        if description:
            data['description'] = description

    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Authorization": f"Bearer {token}",
        "Connection": "keep-alive",
        "Content-Type": "application/json;charset=utf-8",
        "Cookie": f"sidebarStatus=0; Admin-Token={token}",
        "Host": host,
        "Origin": f"https://{host}",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:104.0) Gecko/20100101 Firefox/104.0"
    }
    return lazyrequests.lazy_requests(
        method='POST',
        url=url,
        headers=headers,
        json=data,
        return_json=True
    )


def get_scheduled_msg(
        token,
        current_page: int = 1,
        page_size: int = 10,
        page_type: int = 1

):
    """
    获取客服消息列表
    :param token:
    :param current_page:  # 当前页码
    :param page_size:  # 每页条数
    :param page_type:

    :return:
    """
    url = f'https://{host}/prod-api/v3/open/mng/scheduled-msg/_mget'
    params = {
        "currentPage": current_page,
        "pageSize": page_size,
        "type": page_type
    }
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Authorization": f"Bearer {token}",
        "Connection": "keep-alive",
        "Cookie": f"sidebarStatus=0; Admin-Token={token}",
        "Host": host,
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:104.0) Gecko/20100101 Firefox/104.0"
    }
    return lazyrequests.lazy_requests(
        method='GET',
        url=url,
        headers=headers,
        params=params,
        return_json=True
    )


def get_page_template(
        token
):
    """
    获取【插入页面】的列表元素信息
    :param token:

    :return:
    """
    url = f'https://{host}/prod-api/v3/open/mng/page-template'
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Authorization": f"Bearer {token}",
        "Connection": "keep-alive",
        "Cookie": f"sidebarStatus=0; Admin-Token={token}",
        "Host": host,
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:104.0) Gecko/20100101 Firefox/104.0"
    }
    return lazyrequests.lazy_requests(
        method='GET',
        url=url,
        headers=headers,
        return_json=True
    )


def get_short_link(
        token,
        link_id
):
    """
    获取插入消息正文的短链接
    :param token:
    :param link_id:

    :return:
    """
    url = f'https://{host}/prod-api/v3/open/mng/short-link?id={link_id}'
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Authorization": f"Bearer {token}",
        "Connection": "keep-alive",
        "Cookie": f"sidebarStatus=0; Admin-Token={token}",
        "Host": host,
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:104.0) Gecko/20100101 Firefox/104.0"
    }
    return lazyrequests.lazy_requests(
        method='GET',
        url=url,
        headers=headers,
        return_json=True
    )


def get_novel_info_list(
        token,
        current_page: int = 1,
        page_size: int = 10,
        title: str = None,
        classify_name: str = None
):
    """
    获取小说信息列表
    :param token:
    :param current_page: 当前页码
    :param page_size: 每页数据量
    :param title: 书名
    :param classify_name: 分类

    :return:
    """
    url = f'https://{host}/prod-api/v3/open/mng/novel/getNovelInfoList'
    params = {
        'currentPage': current_page,
        'pageSize': page_size,
        'title': title,
        'classIfyName': classify_name
    }
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Authorization": f"Bearer {token}",
        "Connection": "keep-alive",
        "Cookie": f"sidebarStatus=0; Admin-Token={token}",
        "Host": host,
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:104.0) Gecko/20100101 Firefox/104.0"
    }
    return lazyrequests.lazy_requests(
        method='GET',
        url=url,
        headers=headers,
        params=params,
        return_json=True
    )


def get_novel_chapter_list(
        token,
        current_page: int = 1,
        page_size: int = 10,
        novel_id: str = None
):
    """
    获取小说章节列表
    :param token:
    :param current_page: 当前页码
    :param page_size: 每页数据量
    :param novel_id: 书id

    :return:
    """
    url = f'https://{host}/prod-api/v3/open/mng/novel/getNovelChapterList'
    params = {
        'currentPage': current_page,
        'pageSize': page_size,
        'novelId': novel_id
    }
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Authorization": f"Bearer {token}",
        "Connection": "keep-alive",
        "Cookie": f"sidebarStatus=0; Admin-Token={token}",
        "Host": host,
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:104.0) Gecko/20100101 Firefox/104.0"
    }
    return lazyrequests.lazy_requests(
        method='GET',
        url=url,
        headers=headers,
        params=params,
        return_json=True
    )
