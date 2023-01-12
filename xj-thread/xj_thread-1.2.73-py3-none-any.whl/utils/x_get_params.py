# encoding: utf-8
"""
@project: djangoModel->tool
@author: 孙楷炎
@Email: sky4834@163.com
@synopsis: CURD 工具
@created_time: 2022/6/15 14:14
"""

# 请求参数解析
import json

import typing


def x_get_params(request, content_type=None, **kwargs):
    # 解析请求参数 兼容 APIView与View的情况，View 没有request.data
    query_param = request.GET or {}  # 在APIView才有request.query_params方法
    body_param = request.POST or {}
    try:
        json_param = json.loads(request.body)
    except Exception as e:
        json_param = {}
    result_param = {}
    result_param.update(query_param)
    result_param.update(body_param)
    if isinstance(json_param, dict):
        result_param.update(json_param)
    return result_param
