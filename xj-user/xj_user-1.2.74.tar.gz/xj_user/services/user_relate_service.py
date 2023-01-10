# encoding: utf-8
"""
@project: djangoModel->user_relate_service
@author: 孙楷炎
@Email: sky4834@163.com
@synopsis: 用户关系服务
@created_time: 2022/12/13 16:45
"""
from django.core.paginator import Paginator
from django.db.models import F

from xj_user.models import UserRelateType, UserRelateToUser
# 用户关系类型服务
from ..utils.custom_tool import format_params_handle


class UserRelateTypeService():
    @staticmethod
    def list(params=None):
        if params is None:
            params = {}
        size = params.get("size", 10)
        page = params.get("page", 20)
        filter_params = format_params_handle(
            param_dict=params,
            filter_filed_list=["id", "relate_key", "relate_name", ]
        )
        relate_obj = UserRelateType.objects.filter(**filter_params).values()
        count = relate_obj.count()
        page_set = Paginator(relate_obj, size).get_page(page)
        return {'count': count, "page": page, "size": size, "list": list(page_set.object_list)}, None

    @staticmethod
    def add(params=None):
        if params is None:
            params = {}
        filter_params = format_params_handle(
            param_dict=params,
            filter_filed_list=["relate_key", "relate_name", "description"]
        )
        try:
            relate_obj = UserRelateType.objects.create(**filter_params)
            return {"id": relate_obj.id}, None
        except Exception as e:
            return None, str(e)

    @staticmethod
    def edit(pk=None, update_params=None):
        if update_params is None:
            update_params = {}
        filter_params = format_params_handle(
            param_dict=update_params,
            filter_filed_list=["relate_key", "relate_name", "description"]
        )
        if not pk or not filter_params:
            return None, "没有可修改的数据"
        try:
            relate_obj = UserRelateType.objects.filter(id=pk)
            if not relate_obj:
                return None, "没有可修改的数据"
            relate_obj.update(**filter_params)

            return None, None
        except Exception as e:
            return None, str(e)

    @staticmethod
    def delete(pk=None):
        if not pk:
            return None, "参数错误"
        relate_obj = UserRelateType.objects.filter(id=pk)
        if not relate_obj:
            return None, None
        try:
            relate_obj.delete()
        except Exception as e:
            return None, "删除异常:" + str(e)
        return None, None


# 用户关系映射服务
class UserRelateToUserService():
    @staticmethod
    def list(params=None):
        if params is None:
            params = {}
        size = params.get("size", 10)
        page = params.get("page", 20)
        filter_params = format_params_handle(
            param_dict=params,
            filter_filed_list=["user", "user_id", "with_user", "with_user_id", "user_relate_type", "user_relate_type_id"]
        )
        relate_user_obj = UserRelateToUser.objects.filter(**filter_params) \
            .annotate(user_name=F("user__user_name")).annotate(with_user_name=F("with_user__user_name")).annotate(user_relate_type_name=F("user_relate_type__relate_name")).values()

        count = relate_user_obj.count()
        page_set = Paginator(relate_user_obj, size).get_page(page)
        return {'count': count, "page": page, "size": size, "list": list(page_set.object_list)}, None

    @staticmethod
    def add(params=None):
        if params is None:
            params = {}
        filter_params = format_params_handle(
            param_dict=params,
            filter_filed_list=["user", "user_id", "with_user", "with_user_id", "user_relate_type", "user_relate_type_id"],
            alias_dict={"user": 'user_id', "with_user": "with_user_id", "user_relate_type": "user_relate_type_id"}
        )
        if filter_params.get("user_id", None) is None or filter_params.get("with_user_id", None) is None or filter_params.get("user_relate_type_id", None) is None:
            return None, "参数错误"

        relate_user_obj = UserRelateToUser.objects.filter(
            user_id=filter_params['user_id'],
            with_user=filter_params['with_user_id'],
            user_relate_type_id=filter_params['user_relate_type_id']
        ).first()
        if relate_user_obj:
            return None, "该用户已经绑定，请勿重复绑定"

        try:
            relate_user_obj = UserRelateToUser.objects.create(**filter_params)
            return {"id": relate_user_obj.id}, None
        except Exception as e:
            return None, str(e)

    @staticmethod
    def edit(pk=None, params=None):
        if params is None:
            params = {}
        filter_params = format_params_handle(
            param_dict=params,
            filter_filed_list=["user", "user_id", "with_user", "with_user_id", "user_relate_type", "user_relate_type_id"],
            alias_dict={"user": 'user_id', "with_user": "with_user_id", "user_relate_type": "user_relate_type_id"}
        )
        if not pk or not params:
            return None, "没有可修改的数据"

        try:
            relate_user_obj = UserRelateToUser.objects.filter(id=pk)
            if not relate_user_obj:
                return None, "没有可修改的数据"
            relate_user_obj.update(**filter_params)
            return None, None
        except Exception as e:
            return None, str(e)

    @staticmethod
    def delete(pk=None):
        if not pk:
            return None, "参数错误"
        relate_user_obj = UserRelateToUser.objects.filter(id=pk)
        if not relate_user_obj:
            return None, None
        try:
            relate_user_obj.delete()
        except Exception as e:
            return None, "删除异常:" + str(e)
        return None, None
