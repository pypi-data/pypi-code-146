# encoding: utf-8
"""
@project: djangoModel->thread_v2
@author: 孙楷炎
@Email: sky4834@163.com
@synopsis:
@created_time: 2022/7/29 15:11
"""
import datetime
import logging

from django.core.paginator import Paginator
from django.db.models import F
from rest_framework import serializers as serial

from xj_thread.services.thread_extend_service import ThreadExtendOutPutService
from ..models import Thread
from ..models import ThreadTagMapping

log = logging.getLogger()


# 信息服务CURD(支持扩展字段配置)
class ThreadListService:
    @staticmethod
    def list(params, page=1, size=20, filter_fields=None, sort=None):
        """
        信息列表
        @param params 筛选条件
        @param page 第几页
        @param size 每页条数
        @param filter_fields 过渡条件
        @param sort 指定排序字段，仅支持['id', '-id', 'sort', '-sort', 'create_time', '-create_time', 'update_time', '-update_time']
        """
        # page = params.get('page', 1)
        # size = params.get('size', 20)
        # 边界检查，不写这行，当size为0时，页面会报分母不能为零

        if int(size) <= 0:
            raise serial.ValidationError(f'请求每页数量(size)不能为零。')
        is_admin = params.pop("is_admin", False)
        tag_id_list = params.get('tag_id_list') if params.get('tag_id_list') else None  # 列表[1,2,3,4]
        exclude_category_list = params.get('exclude_categorys').split(',') if params.get('exclude_categorys') else None
        # 边界检查：时间格式验证
        try:
            if params.get('start_time'):
                datetime.datetime.strptime(params.get('start_time'), "%Y-%m-%d %H:%M:%S")
            if params.get('end_time'):
                datetime.datetime.strptime(params.get('end_time'), "%Y-%m-%d %H:%M:%S")
        except ValueError:
            return None, f'时间格式错误:它的格式应该是YYYY-MM-DD HH:MM:SS'

        # 允许进行过渡的字段条件
        conditions = {
            "category_id": params.get('category_id'),
            "category_id__value": params.get('category_value'),
            "category_id__parent_id": params.get("category_parent_id"),
            "classify_id": params.get('classify_id'),
            "classify_id__value": params.get('classify_value'),
            "title__icontains": params.get('title'),
            "create_time__gte": params.get('start_time'),
            "create_time__lte": params.get('end_time'),
            "user_id": params.get('user_id'),
            "user_id__in": params.get('user_id__in'),
            "user_id__not_in": params.get("user_id__not_in"),
        }

        conditions = {k: v for k, v in conditions.items() if v or v == []}
        # print("> ThreadListService conditions:", conditions)
        thread_set = Thread.objects
        if sort and sort in ['id', '-id', 'sort', '-sort', 'create_time', '-create_time', 'update_time', '-update_time']:
            thread_set = thread_set.order_by(sort)
        # 否则默认不会排序，会增加数据库排序时间
        # else:
        #     thread_set = thread_set.order_by('sort')

        # 指定不需要过滤的类别字段
        if exclude_category_list:
            thread_set = thread_set.exclude(category_id__in=exclude_category_list)

        # 开始按过滤条件
        try:
            thread_set = thread_set.annotate(category_value=F("category_id__value")) \
                .annotate(need_auth=F("category_id__need_auth")) \
                .annotate(classify_value=F("classify_id__value")) \
                .annotate(show_value=F("show_id__value"))

            # 边界考虑不周全（is_deleted=0），删除的判断除了0，还有Null也需要考虑在内
            thread_set = thread_set.exclude(is_deleted=True)
            thread_set = thread_set.filter(**conditions)
            # if is_admin:
            #     thread_set = thread_set.filter(**conditions)
            # else:
            #     has_auth = False
            #     if conditions.get("user_id__not_in") == []:  # 这种情况等价于所有人可见
            #         has_auth = True
            #         del conditions["user_id__not_in"]
            #
            #     if conditions.get("user_id__not_in"):  # 权限判断1
            #         has_auth = True
            #         thread_set = thread_set.filter(~Q(user_id__in=conditions.pop("user_id__not_in")))
            #
            #     if conditions.get("user_id__in"):  # 权限判断2
            #         has_auth = True
            #         thread_set = thread_set.filter(user_id__in=conditions.pop("user_id__in"))
            #     # print("conditions", conditions)
            #     if has_auth:  # token 验证成功
            #         thread_set = thread_set.filter(**conditions)
            #     else:  # 没有传token 只允许看不需要权限的信息
            #         thread_set = thread_set.filter(Q(**conditions))
            #         thread_set = thread_set.exclude(category_id__need_auth=False)
            #         # 边界写法错误，need_auth是别名，不能使用别名做为索引条件，会导致布尔类型判断null/0失作用
            #         # thread_set = thread_set.filter(Q(**conditions) & Q(need_auth=0))
            #         thread_set = thread_set.filter(**conditions)

            # print("> ThreadListService thread_set.query:", thread_set.query)
            # print("> ThreadListService thread_set:", thread_set)

            count = thread_set.count()
            filter_field_list = [
                'id', 'category_id', 'category_value', 'classify_id', 'classify_value', 'show_id',
                'show_value', 'need_auth', 'user_id', 'author', 'title', 'subtitle', 'summary',
                'ip', 'has_enroll', 'has_fee', 'has_comment', 'cover', 'photos', 'video',
                'files', 'price', 'is_original', 'more', 'create_time', 'update_time',
            ]
            if filter_fields:
                filter_field_list = filter_fields.split(';')
            # print("> filter_field_list:", filter_field_list)
            thread_set = thread_set.values(*filter_field_list)
        except Exception as e:
            return None, "err:" + e.__str__() + "line:" + str(e.__traceback__.tb_lineno)

        # 这里先处理标签查询
        if tag_id_list:
            try:
                thread_id_list = ThreadTagMapping.objects.filter(tag_id__in=tag_id_list).values_list('thread_id', flat=True)  # flat转列表形式
                thread_set = thread_set.filter(id__in=thread_id_list)
            except ValueError as e:
                log.error(f'信息表标签查询{e}')
        # 分页数据
        finish_set = list(Paginator(thread_set, size).page(page))

        # 如果有指定字段则不拼接了。避免再次循环
        if filter_fields:
            return {'size': int(size), 'page': int(page), 'total': count, 'list': finish_set}, None

        # 主键提取获取 扩展数据(thread_extends)# 扩展字段拼装服务
        category_id_list = list(set([item['category_id'] for item in finish_set if item['category_id']]))
        thread_id_list = list(set([item['id'] for item in finish_set if item['id']]))
        # 扩展数据拼接
        extend_merge_service = ThreadExtendOutPutService(category_id_list=category_id_list, thread_id_list=thread_id_list)
        finish_set = extend_merge_service.merge(finish_set)
        return {'size': int(size), 'page': int(page), 'total': count, 'list': finish_set}, None

    @staticmethod
    def search(id_list, need_map=False):
        if not id_list:
            return [], None
        thread_set = Thread.objects.filter(id__in=id_list)
        # 开始按过滤条件
        try:
            thread_set = thread_set \
                .annotate(thread_category_value=F("category_id__value")) \
                .annotate(need_auth=F("category_id__need_auth")) \
                .annotate(thread_classify_value=F("classify_id__value")) \
                .annotate(show_value=F("show_id__value"))

            thread_set = thread_set.filter(is_deleted=0)
            thread_set = thread_set.values(
                'id', 'category_id', 'thread_category_value', 'classify_id', 'thread_classify_value',
                'show_id', 'show_value', 'need_auth', 'user_id', 'author', 'title',
                'subtitle', 'summary', 'ip', 'has_enroll', 'has_fee', 'has_comment', 'cover',
                'photos', 'video', 'files', 'is_original', 'more', 'create_time', 'update_time',

            )
        except Exception as e:
            return None, "err:" + e.__str__()
        thread_set = list(thread_set)
        # 分页数据 主键提取获取 扩展数据(thread_extends)# 扩展字段拼装服务
        category_id_list = list(set([item['category_id'] for item in thread_set if item['category_id']]))
        thread_id_list = list(set([item['id'] for item in thread_set if item['id']]))
        # # 扩展数据拼接
        extend_merge_service = ThreadExtendOutPutService(
            category_id_list=category_id_list,
            thread_id_list=thread_id_list
        )
        finish_set = extend_merge_service.merge(thread_set)
        if need_map:
            finish_set = {i['id']: i for i in finish_set}
        return finish_set, None

    @staticmethod
    def search_ids(search_prams=None):
        # 用于条件搜索
        if not search_prams:
            return None, None

        thread_set = Thread.objects
        try:
            thread_set = thread_set \
                .annotate(thread_category_value=F("category_id__value")) \
                .annotate(need_auth=F("category_id__need_auth")) \
                .annotate(thread_classify_value=F("classify_id__value")) \
                .annotate(show_value=F("show_id__value")).filter(is_deleted=0)
            thread_set = thread_set.filter(**search_prams)
            thread_set = thread_set.values('id')
        except Exception as e:
            return None, "err:" + e.__str__()
        thread_id_list = [i["id"] for i in list(thread_set)]
        # 如果超过255个，mysql的性能会非常打折扣.
        # if len(thread_id_list) > 255:
        #     thread_id_list = []
        return thread_id_list, None
