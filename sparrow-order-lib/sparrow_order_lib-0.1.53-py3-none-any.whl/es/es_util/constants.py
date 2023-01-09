'''
ES 查询组件中要用的常量
'''


import os

from sparrow_order_lib.core.datastructures import ImmutablePropertyClassBase
from sparrow_order_lib.core.datastructures import ImmutableList


class ESParamOp(ImmutablePropertyClassBase):
    ''' 定义 ES 字段支持的运算 '''
    lt = 'lt'
    lte = 'lte'
    eq = 'eq'
    ne = 'ne'
    gt = 'gt'
    gte = 'gte'
    in_ = 'in_op'
    like = 'like_op'


class ESFieldType(ImmutablePropertyClassBase):
    ''' 定义 ES 字段类型 '''
    TEXT = 'text'
    KEYWORD = 'keyword'
    DATETIME = 'date'
    BOOLEAN = 'boolean'
    INTEGER = 'integer'

    NESTED = 'nested'
    OBJECT = 'object'

    SUB_OBJECT_FIELD = ImmutableList([NESTED, OBJECT])


class ESQueryGroupName(ImmutablePropertyClassBase):
    ''' ES 查询的 query_name '''
    MUST = 'must'
    MUST_NOT = 'must_not'
    SHOULD = 'should'
    AGGS = 'aggs'
    PAGINATION = 'pagination'
    SORT = 'sort'


# ES查询数据时默认每页数据大小
ES_QUERY_PAGE_SIZE_DEFAULT = int(os.environ.get('ES_QUERY_PAGE_SIZE_DEFAULT', '10'))
# ES查询数据最大条数, 超过这个数量就要使用 scroll 深度分页 查询
ES_MAX_RESULT_WINDOW = int(os.environ.get('ES_MAX_RESULT_WINDOW', '10000'))
