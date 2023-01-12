"""
Created on 2022-04-11
@author:刘飞
@description:发布子模块逻辑处理
"""
import logging

from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from django.core.paginator import Paginator
from django.db.models import F
from rest_framework import serializers

# from ..models import ThreadAuth
from ..models import ThreadCategory
from ..models import ThreadClassify
from ..models import ThreadExtendField
from ..models import ThreadShow
from ..models import ThreadTag
# from ..serializers import ThreadAuthListSerializer
from ..serializers import ThreadTagSerializer
from ..utils.custom_tool import format_params_handle

log = logging.getLogger()


class ThreadOtherListServices:
    def __init__(self):
        pass

    @staticmethod
    def thread_category(params):
        """
        类别。类似于版块大类的概念，用于圈定信息内容所属的主要类别
        """
        category_set = ThreadCategory.objects.filter(is_deleted=0).order_by("-sort")
        params = format_params_handle(
            param_dict=params,
            filter_filed_list=["id", "platform_code", "category_value", "name", "need_auth", "description", "sort", "parent_id", ],
            alias_dict={"name": "name__contains"}
        )
        if params:
            category_set = category_set.filter(**params)
        thread_category_obj = category_set.annotate(category_value=F('value')).values(
            "id",
            "platform_code",
            "category_value",
            "name",
            "need_auth",
            "description",
            "sort",
            "parent_id",
        )
        if not thread_category_obj:
            return [], None
        return list(thread_category_obj), None

    @staticmethod
    def thread_classify(category_value=None, category_id=None, classify_id=None, classify_value=None, classify_description=None):
        """
        分类。具体的分类，可以是按行业、兴趣、学科的分类，是主类别下的子分类。
        """
        classify_set = ThreadClassify.objects.order_by('sort')
        if category_id:
            classify_set = classify_set.filter(category_id=category_id)
        if category_value:
            classify_set = classify_set.filter(category_id__value=category_value)
        if classify_id:
            classify_set = classify_set.filter(classify_id=classify_id)
        if classify_value:
            classify_set = classify_set.filter(value=classify_value)
        if classify_description:
            classify_set = classify_set.filter(description=classify_description)
        classify_set = classify_set.annotate(category_value=F('category_id__value'))
        classify_set = classify_set.annotate(show_value=F('show_id__value'))
        return list(classify_set.values()), None

    @staticmethod
    def thread_show(params=None):
        """
        展示类型。用于对前端界面的显示样式进行分类
        """
        thread_show_obj = list(ThreadShow.objects.annotate(label=F("value")).all().values("id", "label", "config", "description"))
        return thread_show_obj, None

    # @staticmethod
    # def thread_auth(params=None):
    #     """
    #     访问权限。作者指定允许哪里用户可以访问，例如私有、公开、好友、指定某些人可以访问等。
    #     """
    #     thread_auth_obj = ThreadAuth.objects.all()
    #     res = ThreadAuthListSerializer(thread_auth_obj, many=True)
    #     return res.data, None

    @staticmethod
    def thread_tag(params):
        """
        标签类型，存放预置标签。
        """
        size = params.get('size', 10)
        page = params.get('page', 1)
        thread_tag_obj = ThreadTag.objects.all()
        paginator = Paginator(thread_tag_obj, size)
        try:
            thread_tag_obj = paginator.page(page)
        except PageNotAnInteger:
            thread_tag_obj = paginator.page(1)
        except EmptyPage:
            thread_tag_obj = paginator.page(paginator.num_pages)
        except Exception as e:
            log.error(f'信息主表分页:{str(e)}')
            raise serializers.ValidationError(str(e))
        res = ThreadTagSerializer(thread_tag_obj, many=True)
        data = {'total': paginator.count, 'list': res.data}
        return data, None

    @staticmethod
    def thread_extend_field_list(params):
        """获取所有的扩展字段列表"""
        params = format_params_handle(
            param_dict=params,
            filter_filed_list=["category_value", "category_id", "id"],
            alias_dict={"category_value": "category__value"}
        )
        print("params:", params)
        extend_field_obj = ThreadExtendField.objects.annotate(field_label=F("value")).annotate(category_value=F("category__value")).annotate(category_description=F("category__description"))
        extend_field_obj = extend_field_obj.filter(**params)
        obj_list = extend_field_obj.values('category_value', 'category_description', 'category_id', "field", 'field_label', 'type', 'unit', 'config')
        return list(obj_list), None
