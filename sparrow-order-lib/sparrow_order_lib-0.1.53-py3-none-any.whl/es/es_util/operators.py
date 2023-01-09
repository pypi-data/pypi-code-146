'''
定义所有逻辑运算符的行为
'''
from operator import eq
from operator import ge
from operator import gt
from operator import le
from operator import lt
# from operator import contains
from operator import ne
from decimal import Decimal

from sparrow_order_lib.es.es_util.constants import ESParamOp, ESFieldType
from sparrow_order_lib.core.datastructures import ImmutableDict


class Operators(object):

    def op(self, opstring, ):
        ''' 通用的运算符方法 '''
        operator = custom_op(opstring)

        def against(other):
            return operator(self, other)

        return against

    def operate(self, op, *other, **kwargs):
        ''' 运算符的具体实现 '''
        raise NotImplementedError


class custom_op(object):

    def __init__(self, opstring):
        self.opstring = opstring

    def __call__(self, left, right, **kw):
        return left.operate(self, right, **kw)


class FieldOperators(Operators):

    def operate(self, op: custom_op, other):
        comparator = ComparatorFactory(self)
        return comparator.operate(op.opstring, other)

    def __eq__(self, other):
        return {"term": {self.path: other}}

    def __o__(self, other, op_str):
        return {"range": {self.path: {op_str: other}}}

    def __ge__(self, other):
        return self.__o__(other, "gte")

    def __le__(self, other):
        return self.__o__(other, "lte")

    def __lt__(self, other):
        return self.__o__(other, "lt")

    def __gt__(self, other):
        return self.__o__(other, "gt")

    def in_(self, others):
        return {"terms": {self.path: others}}

    def like(self, other):
        return {"wildcard": {self.path: other}}


def in_op(a, b):
    return a.in_(b)


def like_op(a, b):
    return a.like(b)


class ComparatorFactory:
    __operator_lookup_map = ImmutableDict(
        {
            ESParamOp.lt: lt,
            ESParamOp.lte: le,
            ESParamOp.gt: gt,
            ESParamOp.gte: ge,
            ESParamOp.eq: eq,
            ESParamOp.ne: ne,
            ESParamOp.in_: in_op,
            ESParamOp.like: like_op
        }
    )

    def __init__(self, expr):
        self.expr = expr

    def operate(self, opstring, other):
        o = self.__operator_lookup_map[opstring]

        # TODO: 未来对不同的字段类型定制各自的 operator

        if self.expr.type == ESFieldType.NESTED:
            child_dsl = self.expr.child.operate(custom_op(opstring), other)
            return {
                "nested": {
                    "path": self.expr.path,
                    "query": {
                        "bool": {
                            "filter": {
                                **child_dsl
                            }
                        }
                    }
                }
            }
        else:
            if self.expr.type == ESFieldType.INTEGER:
                other = int(other)
            if self.expr.type == ESFieldType.BOOLEAN:
                other = bool(other not in ('', '0', 0, [], (), {}, set([]), float(0), Decimal(0), False, 'false'))
            return o(self.expr, other)
