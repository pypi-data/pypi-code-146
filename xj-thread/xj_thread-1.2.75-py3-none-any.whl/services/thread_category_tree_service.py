"""
Created on 2022-04-11
@author:刘飞
@description:发布子模块逻辑处理
"""
import logging

from django.db.models import F

from ..models import ThreadCategory
from ..utils.j_recur import JRecur

log = logging.getLogger()


class ThreadCategoryTreeServices:
    def __init__(self):
        pass

    @staticmethod
    def get_category_tree(category_id=None, category_value=None):
        """
        类别树。
        """

        # 第一步，把类别列表全部读出来
        category_set = ThreadCategory.objects.filter(is_deleted=0).annotate(category_value=F('value')).order_by('sort').values(
            'id',
            'platform_code',
            'category_value',
            'name',
            'need_auth',
            'description',
            'sort',
            'parent_id',
        )
        # print("> category_set:", category_set)
        category_list = list(category_set)
        # print("> category_list:", category_list)

        # 第二步，遍历列表，把数据存放在dict里
        filter_key = 'id' if category_id else ('category_value' if category_value else None)
        filter_value = category_id if category_id else (category_value if category_value else None)

        category_tree = JRecur.create_forest(source_list=category_list)
        # print("> category_tree:", category_tree)

        if filter_key and filter_value:
            category_tree = JRecur.filter_forest(category_tree, filter_key, filter_value)
            if len(category_tree) == 1:
                category_tree = category_tree[0]

        return category_tree, None
