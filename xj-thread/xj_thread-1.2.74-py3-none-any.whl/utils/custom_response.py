"""
Created on 2022-01-17
@author:刘飞
@description:自定义返回格式
"""
import json

from django.http import JsonResponse
from rest_framework import status


# json 结果集返回
def parse_json(result):
    if not result is None:
        if type(result) is str:
            try:
                result = json.loads(result.replace("'", '"').replace('\\r', "").replace('\\n', "").replace('\\t', "").replace('\\t', ""))
            except Exception as e:
                return result
        if type(result) is list or type(result) is tuple:
            for index, value in enumerate(result):
                result[index] = parse_json(value)
        if type(result) is dict:
            for k, v in result.items():
                result[k] = parse_json(v)
    return result


# 数据返回规则
def util_response(data='', err=0, http_status=status.HTTP_200_OK, msg='ok', is_need_parse_json=True):
    if http_status == status.HTTP_200_OK:
        data = parse_json(data) if is_need_parse_json else data
        return JsonResponse({'err': err, 'msg': msg, 'data': data, })
    else:
        return JsonResponse({'err': http_status, 'msg': msg, }, status=http_status)


# 自定义错误页面时返回【DEBUG为True时生效】
def bad_request(request, exception):
    data = {'err': status.HTTP_400_BAD_REQUEST, 'msg': '参数错误', 'data': None}
    return JsonResponse(data=data, status=status.HTTP_400_BAD_REQUEST)


def permission_denied(request, exception):
    data = {'err': status.HTTP_403_FORBIDDEN, 'msg': '无权限', 'data': None}
    return JsonResponse(data=data, status=status.HTTP_403_FORBIDDEN)


def page_not_found(request, exception):
    data = {'err': status.HTTP_404_NOT_FOUND, 'msg': '资源不存在', 'data': None}
    return JsonResponse(data=data, status=status.HTTP_404_NOT_FOUND)


def page_error(exception):
    data = {'err': status.HTTP_500_INTERNAL_SERVER_ERROR, 'msg': '服务器错误', 'data': None}
    return JsonResponse(data=data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
