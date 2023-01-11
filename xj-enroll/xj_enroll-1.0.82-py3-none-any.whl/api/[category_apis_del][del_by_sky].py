# encoding: utf-8
"""
@project: djangoModel->category_api
@author: 孙楷炎
@Email: sky4834@163.com
@synopsis: 分类API
@created_time: 2022/9/20 11:21
"""
from django.views.decorators.http import require_http_methods
from rest_framework.views import APIView

from ..service.category_service import CategoryService
from ..utils.model_handle import parse_data, util_response
from ..validator.category_validator import CategoryValidator


class CategoryApi(APIView):
    @require_http_methods(['GET'])
    def list(self, *args, **kwargs, ):
        params = parse_data(self)
        data, err = CategoryService.list(params=params)
        if err:
            return util_response(err=1000, msg=err)
        return util_response(data=data)

    @require_http_methods(['POST'])
    def add(self, *args, **kwargs, ):
        params = parse_data(self)
        # 表单数据验证
        is_valid, error = CategoryValidator(params).validate()
        if not is_valid:
            return util_response(err=1000, msg=error)
        # 添加数据
        data, err = CategoryService.add(params)
        if err:
            return util_response(err=1001, msg=err)
        return util_response(data=data)

    @require_http_methods(['PUT'])
    def edit(self, *args, **kwargs, ):
        params = parse_data(self)
        category_id = kwargs.get("category_id") or params.pop("category_id") or None
        if not category_id:
            return util_response(err=1000, msg="参数错误:enroll_id不可以为空")
        data, err = CategoryService.edit(params, category_id)
        if err:
            return util_response(err=1000, msg=err)
        return util_response(data=data)

    @require_http_methods(['DELETE'])
    def delete(self, *args, **kwargs, ):
        params = parse_data(self)
        category_id = kwargs.get("category_id") or params.pop("category_id") or None
        if not category_id:
            return util_response(err=1000, msg="参数错误:enroll_id不可以为空")
        data, err = CategoryService.delete(category_id)
        if err:
            return util_response(err=1000, msg=err)
        return util_response(data=data)
