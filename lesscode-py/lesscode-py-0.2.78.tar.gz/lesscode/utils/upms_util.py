# -*- coding: utf-8 -*-
# @Time    : 2022/8/10 11:32
# @Author  : navysummer
# @Email   : navysummer@yeah.net
import tornado.options
from requests import post, get


def upms_register(item, full_url):
    if tornado.options.options.rms_register_enable:
        client_name = item[3] if item[3] else tornado.options.options.application_name
        title = item[4] if item[4] else full_url
        en_name = item[5] if item[5] else full_url
        access = item[6] if item[6] else 0
        client_res = get(url=f"{tornado.options.options.rms_register_server}/upms/client/fetchall",
                         params={"client_name": client_name}).json()
        if not client_res.get("data"):
            post(url=f"{tornado.options.options.rms_register_server}/upms/client/insert",
                 json={"client_name": client_name})
            client_res = get(url=f"{tornado.options.options.rms_register_server}/upms/client/fetchall",
                             params={"client_name": client_name}).json()
        client_id = client_res.get("data")[0].get("id")
        resource_res = get(
            url=f"{tornado.options.options.rms_register_server}/upms/resource/fetchall",
            params={"client_name": client_name, "resource_type": 2, "url": full_url}).json()
        if not resource_res.get("data"):
            res = post(url=f"{tornado.options.options.rms_register_server}/upms/resource/insert",
                       json={"client_id": client_id, "resource_type": 2, "url": full_url, "label": title,
                             "en_name": en_name, "access": access}).json()
            if res.get("status") == "00000":
                print(f"add url={full_url} to rms success")
            else:
                print(f"add url={full_url} to rms fail")
