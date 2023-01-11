# encoding: utf-8
"""
@project: djangoModel->category_service
@author: 孙楷炎
@Email: sky4834@163.com
@synopsis: 小分类服务
@created_time: 2022/9/19 11:14
"""
from django.core.paginator import Paginator

from ..models import EnrollClassify
from ..utils.model_handle import format_params_handle


class ClassifyService(object):
    @staticmethod
    def list(params):
        size = params.pop('size', 10)
        page = params.pop('page', 1)
        params = format_params_handle(
            param_dict=params,
            filter_filed_list=["id", "classify_id", "value", "icon"],
        )
        classify_obj = EnrollClassify.objects.filter(**params).values()
        paginator = Paginator(classify_obj, size)
        try:
            classify_obj = paginator.page(page)
            data = {'total': paginator.count, 'list': list(classify_obj.object_list)}
            return data, None
        except Exception as e:
            return None, f'{str(e)}'

    @staticmethod
    def add(params):
        params = format_params_handle(
            param_dict=params,
            filter_filed_list=["category_id", "value", "description", "icon"],
        )
        if not params:
            return None, "参数不全，请补全参数"
        try:
            EnrollClassify.objects.create(**params)
        except Exception as e:
            return None, str(e)
        return None, None

    @staticmethod
    def delete(classify_id):
        classify_obj = EnrollClassify.objects.filter(id=classify_id)
        if not classify_obj:
            return None, None
        try:
            classify_obj.delete()
        except Exception as e:
            return None, "删除异常:" + str(e)
        return None, None

    @staticmethod
    def edit(params, classify_id):
        classify_id = params.pop("classify_id", None) or classify_id
        params = format_params_handle(
            param_dict=params,
            filter_filed_list=["classify_id", "value", "icon", "description"],
        )
        if not params:
            return None, "没有可修改的参数"
        classify_obj = EnrollClassify.objects.filter(id=classify_id)
        if not classify_obj:
            return None, None
        try:
            classify_obj.update(**params)
        except Exception as e:
            return None, "修改异常:" + str(e)
        return None, None
