#! /usr/bin/env python
'''
@Author: xiaobaiTser
@Email : 807447312@qq.com
@Time  : 2023/1/13 23:47
@File  : myRequest.py
'''

from requests import request


def new_request(method, url, **kwargs):
    ''' 新增数据提取与断言 '''
