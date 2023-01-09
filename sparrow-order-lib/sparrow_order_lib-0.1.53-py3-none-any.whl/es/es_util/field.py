'''
定义 ES 各类 field, 实现逻辑关系行为
'''
from abc import ABC

from sparrow_order_lib.es.es_util.constants import ESFieldType
from sparrow_order_lib.es.es_util.exceptions import ESUtilParamException, ESUtilValueException, ESUtilTypeException
from sparrow_order_lib.es.es_util.operators import FieldOperators


class ESField(ABC, FieldOperators):

    def __new__(cls, **kwargs):
        if 'type' not in kwargs:
            raise ESUtilParamException("缺少关键字参数 type")
        if 'path' not in kwargs:
            raise ESUtilParamException("缺少关键字参数 path")

        path = kwargs['path']
        type = kwargs['type']
        if '.' in path and type != ESFieldType.OBJECT:
            return object.__new__(NestedField)

        for sc in ESField.__subclasses__():
            if sc.type == type:
                return object.__new__(sc)
        else:
            raise ESUtilValueException(f"无法解析的字段类型: {type}")

    def __init__(self, *, path, type):
        self.path = path
        # self.type = type


class TextField(ESField):
    type = ESFieldType.TEXT


class DateTimeField(ESField):
    type = ESFieldType.DATETIME

    # TODO: 时间格式检查

    def __o__(self, other, op_str):
        return {"range": {self.path: {op_str: other, 'time_zone': '+08:00'}}}


class BooleanField(ESField):
    type = ESFieldType.BOOLEAN


class KeywordField(ESField):
    type = ESFieldType.KEYWORD


class NestedField(ESField):
    type = ESFieldType.NESTED

    def __init__(self, *, path: str, type: str):
        paths = path.split('.')
        self.path = paths[0]
        child_path = '.'.join(paths[1:])

        if type == ESFieldType.NESTED:
            type = ESFieldType.KEYWORD
        for sc in ESField.__subclasses__():
            if sc.type == type:
                self.child = sc(path=child_path, type=type)
                self.child.path = f'{self.path}.{self.child.path}'  # 初始化完, 补偿 path
                break
        else:
            raise ESUtilTypeException(f'未找到字段类型{type}')


class ObjectField(ESField):
    type = ESFieldType.OBJECT


class IntegerField(ESField):
    type = ESFieldType.INTEGER
