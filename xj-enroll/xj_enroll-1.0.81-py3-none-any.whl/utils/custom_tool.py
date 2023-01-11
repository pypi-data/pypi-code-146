# encoding: utf-8
"""
@project: djangoModel->tool
@author: 孙楷炎
@Email: sky4834@163.com
@synopsis: CURD 工具
@created_time: 2022/6/15 14:14
"""

import json
import random
from urllib.parse import parse_qs

from django.core.handlers.asgi import ASGIRequest
from django.core.handlers.wsgi import WSGIRequest
from rest_framework.request import Request
import xmltodict


def is_number(s):
    """识别任何语言的数字字符串"""
    try:
        float(s)
        return True
    except ValueError:
        pass

    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass

    return False


# json 结果集返回
def parse_json(result):
    if not result is None:
        if type(result) is str:
            try:
                result = json.loads(result.replace("'", '"').replace('\\r', "").replace('\\n', "").replace('\\t', "").replace('\\t', ""))
            except Exception as e:
                return result
        if type(result) is list:
            for index, value in enumerate(result):
                result[index] = parse_json(value)
        if type(result) is dict:
            for k, v in result.items():
                result[k] = parse_json(v)
    return result


# 字段筛选并替换成别名
def format_params_handle(param_dict, filter_filed_list=None, remove_filed_list=None, alias_dict=None, is_remove_null=True):
    """
    字段筛选并替换成别名
    :param param_dict: 参数值
    :param filter_filed_list: 字段白名单
    :param remove_filed_list: 字段黑名单
    :param alias_dict: 表明字典
    :param is_remove_null:  是否把带有None的值移除掉
    :return: param_dict
    """
    # 转换的数据类型不符合，直接返回出去
    if not isinstance(param_dict, dict):
        raise Exception("param_dict 必须是字典格式")

    # 类型判断 过滤字段
    if filter_filed_list and isinstance(filter_filed_list, list):
        param_dict = {k: v for k, v in param_dict.copy().items() if k in filter_filed_list and (not v is None or not is_remove_null)}

    # 类型判断， 剔除字段
    if remove_filed_list and isinstance(remove_filed_list, list):
        param_dict = {k: v for k, v in param_dict.copy().items() if not k in remove_filed_list and (not v is None or not is_remove_null)}

    # 类型判断 字段转换
    if alias_dict and isinstance(alias_dict, dict):
        param_dict = {alias_dict.get(k, k): v for k, v in param_dict.copy().items()}

    return param_dict


# 结果接字段过滤
def filter_result_field(result_list, filter_filed_list=None, remove_filed_list=None, alias_dict=None):
    # 转换的数据类型不符合，直接返回出去
    if filter_filed_list is None and remove_filed_list is None and alias_dict is None:
        return result_list
    result = []
    for item in result_list:
        row_res = {}
        # 类型判断 过滤字段
        if filter_filed_list and isinstance(filter_filed_list, list):
            row_res = {k: v for k, v in item.copy().items() if k in filter_filed_list}
        # 类型判断， 剔除字段
        if remove_filed_list and isinstance(remove_filed_list, list):
            row_res = {k: v for k, v in item.copy().items() if not k in remove_filed_list}
        # 类型判断 字段转换
        if alias_dict and isinstance(alias_dict, dict):
            row_res = {alias_dict.get(k, k): v for k, v in item.copy().items()}

        if row_res:
            result.append(row_res)

    return result


# 请求参数解析
def parse_data(request):
    # 解析请求参数 兼容 APIView与View的情况，View 没有request.data
    content_type = request.META.get('CONTENT_TYPE', "").split(";")[0]
    method = request.method
    if content_type == "text/plain" or method == "GET":
        try:
            body = request.body.decode("utf-8")
            data = json.loads(body)
        except Exception:
            data = request.GET
            if not data:
                data = request.POST
            if not data:
                data = {}
    elif content_type == "application/json":
        return json.loads(request.body)
    elif content_type == "multipart/form-data":
        data = request.POST
    elif content_type == "application/xml":
        try:
            data = xmltodict.parse(request.body)
            return data.get("body") or data.get("data", {})
        except Exception as e:
            data = {}
    elif content_type == "application/x-www-form-urlencoded":
        data = parse_qs(request.body.decode())
        if data:
            data = {k: v[0] for k, v in data.items()}
        else:
            data = {}

    else:
        data = getattr(request, 'data', {})
    return {k: v for k, v in data.items()}


# 请求参数解析
def request_params_wrapper(func):
    # 解析请求参数 兼容 APIView与View的情况，View 没有request.data
    def wrapper(instance, arg_request=None, *args, request=None, **kwargs):
        """
        @param instance 实例是一个APIView的实例
        @param args 其它可变参数元组
        @param kwargs 其它可变关键字参数字典
        """
        if isinstance(instance, WSGIRequest) or isinstance(instance, Request) or isinstance(instance, ASGIRequest):
            request = instance
        if isinstance(arg_request, WSGIRequest) or isinstance(arg_request, Request) or isinstance(arg_request, ASGIRequest):
            request = arg_request
        if request is None:
            return func(instance, *args, request=request, request_params={}, **kwargs, )

        # 参数解析
        content_type = request.META.get('CONTENT_TYPE', "").split(";")[0]
        method = request.method
        # print("content_type:", content_type, "method:", method)
        if content_type == "text/plain" or method == "GET":
            try:
                body = request.body.decode("utf-8")
                data = json.loads(body)
            except Exception:
                data = request.GET
                if not data:
                    data = request.POST
                if not data:
                    data = {}
        elif content_type == "application/json":
            data = json.loads(request.body)
        elif content_type == "multipart/form-data":
            data = request.POST
        elif content_type == "application/xml":
            try:
                data = xmltodict.parse(request.body)
                data = data.get("body") or data.get("data", {})
            except Exception as e:
                data = {}
        elif content_type == "application/x-www-form-urlencoded":
            data = parse_qs(request.body.decode())
            if data:
                data = {k: v[0] for k, v in data.items()}
            else:
                data = {}
        else:
            data = getattr(request, 'data', {})
        # 闭包抛出
        return func(instance, *args, request=request, request_params={k: v for k, v in data.items()}, **kwargs, )

    return wrapper


def deal_equally(total: int, num: int):
    """
    发牌均分，发完截至, 然后打乱顺序
    :param total: 总数
    :param num: 平均分配给这些人
    :return: list
    """
    every_one_jetton = int((total / num))
    overplus_jetton = total % num
    jetton_list = [every_one_jetton for i in range(num)]
    if overplus_jetton == 0:
        return jetton_list
    for index in range(overplus_jetton):
        jetton_list[index] = every_one_jetton + 1
    random.shuffle(jetton_list)
    return jetton_list
