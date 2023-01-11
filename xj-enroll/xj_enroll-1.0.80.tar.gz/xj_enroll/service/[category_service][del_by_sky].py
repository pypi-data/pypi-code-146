# encoding: utf-8
"""
@project: djangoModel->category_service
@author: 孙楷炎
@Email: sky4834@163.com
@synopsis: 大分类服务
@created_time: 2022/9/19 11:14
"""
from django.core.paginator import Paginator

from ..utils.model_handle import format_params_handle


class CategoryService(object):
    @staticmethod
    def list(params):
        size = params.pop('size', 10)
        page = params.pop('page', 1)
        params = format_params_handle(
            param_dict=params,
            filter_filed_list=["id", "value"],
        )
        enroll_obj = EnrollCategory.objects.filter(**params).values()
        paginator = Paginator(enroll_obj, size)
        try:
            enroll_obj = paginator.page(page)
            data = {'total': paginator.count, 'list': list(enroll_obj.object_list)}
            return data, None
        except Exception as e:
            return None, f'{str(e)}'

    @staticmethod
    def add(params):
        params = format_params_handle(
            param_dict=params,
            filter_filed_list=["value", "description"],
        )
        if not params:
            return None, "参数不全，请补全参数"
        try:
            EnrollCategory.objects.create(**params)
        except Exception as e:
            return None, str(e)
        return None, None

    @staticmethod
    def delete(category_id):
        category_obj = EnrollCategory.objects.filter(id=category_id)
        if not category_obj:
            return None, None
        try:
            category_obj.delete()
        except Exception as e:
            return None, "删除异常:" + str(e)
        return None, None

    @staticmethod
    def edit(params, category_id):
        category_id = params.pop("category_id", None) or category_id
        params = format_params_handle(
            param_dict=params,
            filter_filed_list=["value", "description"],
        )
        if not params:
            return None, "没有可修改的参数"
        category_obj = EnrollCategory.objects.filter(id=category_id)
        if not category_obj:
            return None, None
        try:
            category_obj.update(**params)
        except Exception as e:
            return None, "修改异常:" + str(e)
        return None, None
