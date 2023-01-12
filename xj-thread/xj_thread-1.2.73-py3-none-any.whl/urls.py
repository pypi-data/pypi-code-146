"""
Created on 2022-04-11
@author:刘飞
@description:发布子模块路由分发
"""
from django.urls import re_path

from xj_thread.apis.thread_category_apis import ThreadCategoryApis
from xj_thread.apis.thread_classify_apis import ThreadClassifyApis
from .apis.thread_add import ThreadAdd
from .apis.thread_category_tree import ThreadCategoryTreeAPIView
from .apis.thread_classify_tree import ThreadClassifyTreeAPIView
from .apis.thread_item import ThreadItemAPI
from .apis.thread_list import ThreadListAPIView
from .apis.thread_other_list import AuthListAPIView, ShowListAPIView, TagListAPIView, ThreadExtendFieldList
from .apis.thread_statistic import ThreadStaticAPIView

# 应用名称
# app_name = 'thread'

urlpatterns = [
    re_path(r'^category_add/?$', ThreadCategoryApis.add, name='category_add'),  # 类别列表
    re_path(r'^category_del/?(?P<pk>[-_\w]+)?', ThreadCategoryApis.delete, name='category_del'),  # 类别列表
    re_path(r'^category_edit/?(?P<pk>[-_\w]+)?', ThreadCategoryApis.edit, name='category_edit'),  # 类别列表
    re_path(r'^category_list/?$', ThreadCategoryApis.list, name='category_list'),  # 类别列表
    re_path(r'^category_tree/?(?P<category_value>[-_\w]+)?/?$', ThreadCategoryTreeAPIView.as_view(), name='thread_category_tree'),

    re_path(r'^classify_list/?$', ThreadClassifyApis.list, name='classify_list'),  # 分类列表
    re_path(r'^classify_add/?$', ThreadClassifyApis.add, name='classify_list'),  # 分类列表
    re_path(r'^classify_edit/?$', ThreadClassifyApis.edit, name='classify_list'),  # 分类列表
    re_path(r'^classify_del/?$', ThreadClassifyApis.edit, name='classify_list'),  # 分类列表
    re_path(r'^classify_tree/?(?P<classify_value>[-_\w]+)?/?$', ThreadClassifyTreeAPIView.as_view(), name='thread_classify_tree'),

    re_path(r'^show_list/?$', ShowListAPIView.as_view(), name='show_list'),  # 展示类型列表
    re_path(r'^tag_list/?$', TagListAPIView.as_view(), name='tag_list'),  # 展示类型列表
    re_path(r'^list/?(?P<category_value>[-_\w]+)?/?$', ThreadListAPIView.as_view(), name='list'),  # 信息列表/新增
    re_path(r'^item_add/?$', ThreadAdd.as_view(), name='list'),  # 信息列表/新增
    re_path(r'^item/(?P<pk>\d+)/?$', ThreadItemAPI.as_view(), name='detail'),  # 信息单挑操作：详情/编辑/删除
    # 列表 信息相关
    re_path(r'^auth[_/]list/?$', AuthListAPIView.as_view(), name='auth_list'),  # 权限列表
    re_path(r'^extend_field_list/?$', ThreadExtendFieldList.as_view(), name='tag_list'),  # 展示类型列表
    re_path(r'^statistic/?$', ThreadStaticAPIView.as_view(), name='tag_list'),  # 计数统计，前端埋点接口
]
