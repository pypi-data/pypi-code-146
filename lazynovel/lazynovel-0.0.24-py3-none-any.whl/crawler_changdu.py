#!/usr/bin/env python3
# coding = utf8
"""
@ Author : ZeroSeeker
@ e-mail : zeroseeker@foxmail.com
@ GitHub : https://github.com/ZeroSeeker
@ Gitee : https://gitee.com/ZeroSeeker
"""
from lazysdk import lazyrequests


def create_customer_service_message(
        cookie: str,
        app_id,
        app_type,
        distributor_id,
        msg_name: str,
        msg_type: int,
        send_time: str,
        send_target: int,
        content,
):
    """
    运营配置-客服消息-新建消息
    目前仅支持文字消息
    :param cookie: cookie
    :param app_id: 应用id
    :param app_type: 应用类型：3-公众号
    :param distributor_id:
    :param msg_name: 消息名称
    :param msg_type: 消息类型：1-文字消息，2-图文消息
    :param content: 消息内容，
    文字消息：f'<p>{text_content}</p>'，
    图文消息：{
            'img_uri': img_uri,
            'img_url': img_url,
            'link_html': link_html,
            'msg_url': msg_url,
            'title': title,
            'url_title': url_title,
        }
    :param send_time: 发送时间，例如：2022-12-31 17:27:33
    :param send_target: 发送用户，1-全部用户，2-已充值用户，3-未充值用户
    """
    url = 'https://www.changdunovel.com/novelsale/distributor/customer_service_message/create/v1/'
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Connection": "keep-alive",
        "Cookie": cookie,
        "Host": "www.changdunovel.com",
        "Origin": "https://www.changdunovel.com",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "TE": "trailers",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:108.0) Gecko/20100101 Firefox/108.0",
        "agw-js-conv": "str",
        "appid": str(app_id),
        "apptype": str(app_type),
        "content-type": "application/json",
        "distributorid": str(distributor_id)
    }
    data = {
        "msg_name": msg_name,
        "msg_type": msg_type,
        "send_time": send_time,
        "send_target": send_target
    }
    if msg_type == 1:
        data['msg_detail'] = {
            "content": content  # 消息内容
        }
    elif msg_type == 2:
        data['msg_detail'] = content
    else:
        return
    return lazyrequests.lazy_requests(
        method='POST',
        url=url,
        json=data,
        headers=headers,
        return_json=True
    )


def wx_get_page_url(
        cookie: str,
        app_id,
        app_type,
        distributor_id
):
    """
    位置：（H5书城分销）运营配置-客服消息-新建消息-消息链接（页面链接）
    功能：获取页面链接列表
    :param cookie: cookie
    :param app_id: 应用id
    :param app_type: 应用类型：3-公众号
    :param distributor_id:
    """
    url = 'https://www.changdunovel.com/novelsale/distributor/wx/get_page_url/v1/'
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Connection": "keep-alive",
        "Cookie": cookie,
        "Host": "www.changdunovel.com",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "TE": "trailers",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:108.0) Gecko/20100101 Firefox/108.0",
        "agw-js-conv": "str",
        "appid": str(app_id),
        "apptype": str(app_type),
        "distributorid": str(distributor_id)
    }
    return lazyrequests.lazy_requests(
        method='GET',
        url=url,
        headers=headers,
        return_json=True
    )


def customer_service_message_upload(
        cookie: str,
        app_id,
        app_type,
        distributor_id,
        file_dir
):
    """
    位置：（H5书城分销）运营配置-客服消息-新建消息-消息图片
    功能：上传图片
    :param cookie: cookie
    :param app_id: 应用id
    :param app_type: 应用类型：3-公众号
    :param distributor_id:
    :param file_dir: 需要上传的文件路径
    """
    url = 'https://www.changdunovel.com/novelsale/distributor/customer_service_message/upload/v1/'
    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Connection": "keep-alive",
        "Cookie": cookie,
        "Host": "www.changdunovel.com",
        "Origin": "https://www.changdunovel.com",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:108.0) Gecko/20100101 Firefox/108.0",
        "appid": str(app_id),
        "apptype": str(app_type),
        "distributorid": str(distributor_id)
    }
    files = [
        ('file', (open(file_dir, 'rb')))
    ]
    return lazyrequests.lazy_requests(
        method='POST',
        url=url,
        headers=headers,
        files=files,
        return_json=True
    )
