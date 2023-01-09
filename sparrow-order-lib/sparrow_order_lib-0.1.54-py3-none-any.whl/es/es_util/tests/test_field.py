from unittest import TestCase
import unittest

from sparrow_order_lib.es.es_util.field import ESField
from sparrow_order_lib.es.es_util.field import TextField
from sparrow_order_lib.es.es_util.field import DateTimeField
from sparrow_order_lib.es.es_util.field import BooleanField
from sparrow_order_lib.es.es_util.field import KeywordField
from sparrow_order_lib.es.es_util.field import NestedField
from sparrow_order_lib.es.es_util.field import ObjectField
from sparrow_order_lib.es.es_util.field import IntegerField
from sparrow_order_lib.es.es_util.constants import ESFieldType


class TestESField(TestCase):

    def test_text_field(self):
        text_field = ESField(path='test_text_field_path_path', type=ESFieldType.TEXT)

        self.assertIsInstance(text_field, cls=TextField, msg="初始化 TextField 失败")

    def test_datetime_field(self):
        datetime_field = ESField(path='test_datetime_field_path', type=ESFieldType.DATETIME)

        self.assertIsInstance(datetime_field, DateTimeField, msg="初始化 DateTimeField 失败")

    def test_boolean_field(self):
        boolean_field = ESField(path='test_boolean_field_path', type=ESFieldType.BOOLEAN)

        self.assertIsInstance(boolean_field, BooleanField, msg="初始化 BooleanField 失败")

    def test_keyword_field(self):
        keyword_field = ESField(path='test_keyword_field_path', type=ESFieldType.KEYWORD)

        self.assertIsInstance(keyword_field, KeywordField, msg="初始化 KeywordField 失败")

    def test_nested_field(self):
        ''' nested 是指第一层 path 的类型, 传入的 type 是指目标查询字段类型 '''
        nested_field = ESField(path='test_nested_field.child_path', type=ESFieldType.KEYWORD)

        self.assertIsInstance(nested_field, NestedField, msg="初始化 NestedField 失败")

    def test_object_field(self):
        object_field = ESField(path='test_nested_field.child_path', type=ESFieldType.OBJECT)

        self.assertIsInstance(object_field, ObjectField, msg="初始化 ObjectField 失败")

    def test_integer_field(self):
        integer_field = ESField(path='test_integer_field_path', type=ESFieldType.INTEGER)

        self.assertIsInstance(integer_field, IntegerField, msg="初始化 IntegerField 失败")


if __name__ == '__main__':
    unittest.main()
