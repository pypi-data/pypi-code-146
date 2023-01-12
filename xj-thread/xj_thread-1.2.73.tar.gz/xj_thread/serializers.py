"""
Created on 2022-04-11
@author:刘飞
@description:发布子模块序列化器
"""

from django.utils.translation import gettext as tr
from rest_framework import serializers

from xj_user.models import BaseInfo, DetailInfo
from .models import (ThreadShow,
                     ThreadClassify,
                     ThreadCategory,
                     Thread,
                     ThreadStatistic,
                     ThreadTag,
                     ThreadTagMapping, ThreadExtendField)


# 捕获异常装饰器
def catch_except(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception:
            return ""

    return wrapper


class ThreadShowListSerializer(serializers.ModelSerializer):
    """展示类型序列化器"""
    label = serializers.SerializerMethodField()

    class Meta:
        model = ThreadShow
        fields = '__all__'

    def get_label(self, instance):
        return tr(instance.value)


class ThreadClassifyListSerializer(serializers.ModelSerializer):
    """分类序列化器"""
    label = serializers.SerializerMethodField()

    class Meta:
        model = ThreadClassify
        fields = '__all__'

    def get_label(self, instance):
        return tr(instance.value)


class ThreadCategoryListSerializer(serializers.ModelSerializer):
    """类别序列化"""
    label = serializers.SerializerMethodField()

    class Meta:
        model = ThreadCategory
        fields = ("id", "label", "description", "nead_auth")

    def get_label(self, instance):
        return str(getattr(instance, "value", ""))


# class ThreadAuthListSerializer(serializers.ModelSerializer):
#     """访问权限序列化"""
#     label = serializers.SerializerMethodField()
#
#     class Meta:
#         model = ThreadAuth
#         fields = ("id", "label")
#
#     def get_label(self, instance):
#         return tr(instance.value)


class ThreadStatisticListSerializer(serializers.ModelSerializer):
    """信息统计表序列化器"""

    class Meta:
        model = ThreadStatistic
        fields = [
            # "thread_id",
            # "flag_classifies",
            # "flag_weights",
            "weight",
            "views",
            "plays",
            "comments",
            "likes",
            "favorite",
            "shares",
        ]


class ThreadTagSerializer(serializers.ModelSerializer):
    """标签类型序列化器"""

    class Meta:
        model = ThreadTag
        exclude = ['thread']


class ThreadListSerializer(serializers.ModelSerializer):
    """信息表，即主表序列化"""

    create_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)
    update_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)
    # category_value = serializers.SerializerMethodField()
    # classify_value = serializers.SerializerMethodField()
    # show_value = serializers.SerializerMethodField()
    # auth_value = serializers.SerializerMethodField()
    # classify_label = serializers.SerializerMethodField()
    # auth_label = serializers.SerializerMethodField()
    # full_name = serializers.SerializerMethodField()  # 由于耦合了外部模块的用户表格，禁止使用
    # avatar = serializers.SerializerMethodField()  # 由于耦合了外部模块的用户表格，禁止使用
    # statistic = serializers.SerializerMethodField()
    # tag_list = serializers.SerializerMethodField()
    thread_extends = serializers.SerializerMethodField()

    class Meta:
        model = Thread
        fields = [
            # ----- Thread 信息主表 -----
            'id',
            'category_id',
            'category_value',
            'classify_id',
            'classify_value',
            'show_id',
            'show_value',
            'user_id',
            # 'avatar',  # 由于耦合了外部模块的用户表格，禁止使用
            # 'full_name',  # 由于耦合了外部模块的用户表格，禁止使用
            'auth_id',
            # 'auth_value',
            # 'auth_label',
            # 'is_deleted',
            'title',
            'summary',
            # 'content',
            'author',
            # 'ip',
            'has_enroll',
            'has_fee',
            'has_comment',
            'cover',
            'photos',
            'video',
            'files',
            'price',
            'is_original',
            'more',
            'create_time',
            'update_time',

            # ----- Thread Tags 标签信息表 -----
            # 'tag_list',

            # ----- Thread Statistic 统计信息表 -----
            # 'statistic',

            # ----- Thread Extend 扩展信息表 -----
            'thread_extends',
        ]
        # exclude = ('logs',)
        # fields = '__all__'

    def get_show_value(self, instance):
        show_value = instance.show_id.value if instance.show_id else None
        return show_value

    # def get_auth_value(self, instance):
    #     auth_value = instance.auth_id.value if instance.auth_id else None
    #     return auth_value

    def get_classify_label(self, instance):
        classify_value = tr(instance.classify_id.value) if instance.classify_id else None
        return classify_value

    # def get_auth_label(self, instance):
    #     auth_value = tr(instance.auth_id.value) if instance.auth_id else None
    #     return auth_value

    def get_thread_extends(self, instance):
        if not hasattr(instance, 'thread_extend_data'):
            return {}
        fields = ThreadExtendField.objects.filter(classify_id=instance.classify_id)
        return {field.field: getattr(instance.thread_extend_data, field.extend_field) for field in fields}


class ThreadDetailSerializer(serializers.ModelSerializer):
    """信息表，即主表详情序列化"""

    create_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)
    update_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)
    category_value = serializers.SerializerMethodField()
    classify_value = serializers.SerializerMethodField()
    show_value = serializers.SerializerMethodField()
    # auth_value = serializers.SerializerMethodField()
    show_label = serializers.SerializerMethodField()
    # auth_label = serializers.SerializerMethodField()
    full_name = serializers.SerializerMethodField()
    user_name = serializers.SerializerMethodField()
    nickname = serializers.SerializerMethodField()
    statistic = serializers.SerializerMethodField()
    tag_list = serializers.SerializerMethodField()
    avatar = serializers.SerializerMethodField()
    thread_extends = serializers.SerializerMethodField()

    class Meta:
        model = Thread
        fields = '__all__'

    @catch_except
    def get_avatar(self, instance):
        user_detail_obj = DetailInfo.objects.filter(user_id=instance.user_id).first()
        avatar = user_detail_obj.avatar if user_detail_obj else None
        return avatar

    @catch_except
    def get_category_value(self, instance):
        category_value = instance.category_id.value if instance.category_id else None
        return category_value

    @catch_except
    def get_classify_value(self, instance):
        return instance.classify_id.value

    @catch_except
    def get_show_value(self, instance):
        show_value = instance.show.value if instance.show_id else None
        return show_value

    # @catch_except
    # def get_auth_value(self, instance):
    #     auth_value = instance.auth.value if instance.auth_id else None
    #     return auth_value

    @catch_except
    def get_show_label(self, instance):
        show_value = tr(instance.show.value) if instance.show_id else None
        return show_value

    # # @catch_except
    # def get_auth_label(self, instance):
    #     auth_value = tr(instance.auth_id.value) if instance.auth_id else None
    #     return auth_value

    @catch_except
    def get_full_name(self, instance):
        user_obj = BaseInfo.objects.filter(id=instance.user_id).first()
        full_name = user_obj.full_name if user_obj else None
        return full_name

    @catch_except
    def get_user_name(self, instance):
        user_obj = BaseInfo.objects.filter(id=instance.user_id).first()
        user_name = user_obj.user_name if user_obj else None
        return user_name

    def get_nickname(self, instance):
        nickname = ""
        if instance.user_id:
            user_obj = BaseInfo.objects.filter(id=instance.user_id).first()
            nickname = user_obj.nickname if user_obj else None
        return nickname

    def get_statistic(self, instance):
        obj = ThreadStatistic.objects.filter(thread_id=instance.id).first()
        return ThreadStatisticListSerializer(obj).data

    def get_tag_list(self, instance):
        tag_list = []
        tag_id_list = ThreadTagMapping.objects.filter(thread_id=instance).values_list('tag_id', flat=True)
        tag_obj = ThreadTag.objects.filter(id__in=tag_id_list)
        for t in tag_obj:
            tag_list.append({"id": t.id, "value": t.value})
        return tag_list

    def get_thread_extends(self, instance):
        if not hasattr(instance, 'thread_extend_data'):
            return {}
        fields = ThreadExtendField.objects.filter(category_id=instance.category_id.id)
        return {field.field: getattr(instance.thread_extend_data, field.field_index, None) for field in fields}
