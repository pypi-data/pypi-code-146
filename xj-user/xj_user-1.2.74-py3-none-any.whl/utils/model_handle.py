# encoding: utf-8
"""
@project: djangoModel->tool
@author: 孙楷炎
@Email: sky4834@163.com
@synopsis: CURD 工具
@created_time: 2022/6/15 14:14
"""

# ===========  工具方法 start =============
import json

from django.core import serializers
from django.core.paginator import Paginator

from .custom_response import *


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
def format_params_handle(param_dict, filter_filed_list=None, remove_filed_list=None, alias_dict=None):
    # 转换的数据类型不符合，直接返回出去
    if not isinstance(param_dict, dict):
        raise Exception("param_dict 必须是字典格式")

    # 类型判断 过滤字段
    if filter_filed_list and isinstance(filter_filed_list, list):
        param_dict = {k: v for k, v in param_dict.copy().items() if k in filter_filed_list and v}

    # 类型判断， 剔除字段
    if remove_filed_list and isinstance(remove_filed_list, list):
        param_dict = {k: v for k, v in param_dict.copy().items() if not k in remove_filed_list and v}

    # 类型判断 字段转换
    if alias_dict and isinstance(alias_dict, dict):
        param_dict = {alias_dict.get(k, k): v for k, v in param_dict.copy().items()}

    return param_dict


# 请求参数解析
def parse_data(request, **kwargs):
    # 解析请求参数 兼容 APIView与View的情况，View 没有request.data
    content_type = request.META.get('CONTENT_TYPE', "").split(";")[0]
    method = request.method
    if method == "GET":
        data = request.GET
    elif method == "POST":
        if content_type == "application/json":
            data = json.loads(request.body)
        else:
            data = request.POST
    else:
        data = request.data
    return {k: v for k, v in data.items()}


# 模型解析
def parse_model(res_set, custom_serializers=None, is_simple=False, ):
    try:
        # 序列化转换执行
        if custom_serializers:
            custom_serializers_data = custom_serializers(res_set)
            return custom_serializers_data.data
        # 没有传序列化的时候默认进行，json序列化
        json_data = json.loads(serializers.serialize('json', res_set))
    except Exception as e:
        # 当使用了values()限制结果集会报错，使用list进行转换结果集
        return list(res_set)
    # 如果正常json过了，则进行格式化
    if not json_data:
        return None
    else:
        if is_simple:
            return json_data[0]['fields']
        else:
            res_set = []
            for i in json_data:
                fields = i['fields']
                fields['id'] = i['pk']
                res_set.append(fields)
            return res_set


# 序列换元组类型转换字典
def serializers_to_list(data):
    result = []
    for i in data:
        temp_dict = {}
        for k, v in i.items():
            if type(v) is tuple:
                serializers_to_list(v)
            temp_dict[k] = v
        result.append(temp_dict)
    return result


# =================== CURD ===============
def model_select(request, model, is_need_delete=False, json_parse_key=None):
    # 模型快速分页查询  分页+条件
    page = request.GET.get('page', 1)
    limit = request.GET.get('limit', 20)
    params = parse_data(request)
    if 'page' in params.keys():
        del params['page']
    if 'limit' in params.keys():
        del params['limit']

    if is_need_delete:
        params['is_delete'] = 0
    try:
        list_set = model.objects.filter(**params)
        count = model.objects.filter(**params).count()
    except Exception as e:
        return util_response("", 7557, e.__str__(), status.HTTP_400_BAD_REQUEST)
    # 分页数据
    limit_set = Paginator(list_set, limit)
    page_set = limit_set.get_page(page)
    # 数据序列化操作
    json_data = json.loads(serializers.serialize('json', page_set))
    final_res_dict = []
    for i in json_data:
        fields = i['fields']
        fields['id'] = i['pk']
        if not json_parse_key is None:
            fields[json_parse_key] = json.loads(fields[json_parse_key])
        final_res_dict.append(fields)
    # 数据拼装
    result = {'list': final_res_dict, 'limit': int(limit), 'page': int(page), 'count': count}
    return util_response(result, 0)


def model_create(request, model, validate):
    try:
        requestData = parse_data(request)
        if not validate is None:
            validator = validate(requestData)
            is_pass, error = validator.validate()
            if not is_pass:
                return util_response("", 7557, error)

        model.objects.create(**requestData)
    except Exception as e:
        return util_response("", 7557, e.__str__(), status.HTTP_400_BAD_REQUEST)
    return util_response()


def model_update(request, model, is_need_delete=False):
    # 模型修改
    from_data = parse_data(request)
    if not 'id' in from_data.keys():
        return util_response('', 7557, "ID不能为空")
    id = from_data['id']
    del from_data['id']
    if from_data == {}:
        return util_response('', 7557, "至少改点什么吧！！")
    # 是否存软删除条件
    if is_need_delete:
        res = model.objects.filter(id=id, is_delete=0)
    else:
        res = model.objects.filter(id=id)
    # 修改并返回
    if not res:
        return util_response('', 7557, "数据已不存在")
    try:
        res.update(**from_data)
        return util_response('', 0, "ok")
    except Exception as e:
        return util_response("", 7557, e.__str__(), status.HTTP_400_BAD_REQUEST)


def model_delete(request, model, is_real_delete=True):
    from_data = parse_data(request)
    if not 'id' in from_data.keys():
        return util_response('', 7557, "ID不能为空")
    if is_real_delete:
        res = model.objects.filter(id=from_data['id'])
        # res = model.objects.filter(**from_data)
        if not res:
            return util_response('', 7557, "数据已不存在")

        res.delete()
    else:
        from_data['is_delete'] = 0
        res = model.objects.filter(**from_data)
        if not res:
            return util_response('', 7557, "数据已不存在")
        res.update(is_delete=1)

    return util_response()
