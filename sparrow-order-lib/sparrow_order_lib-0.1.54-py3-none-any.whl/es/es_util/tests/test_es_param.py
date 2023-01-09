import unittest

from sparrow_order_lib.es.es_util.field import ESField
from sparrow_order_lib.es.es_util.es_param import ESParam
from sparrow_order_lib.es.es_util.es_param import ESParamsForOneGroup
from sparrow_order_lib.es.es_util.es_param import ESParamGroup
from sparrow_order_lib.es.es_util.es_param import ESParamShouldGroup
from sparrow_order_lib.es.es_util.es_param import ESParamMustGroup
from sparrow_order_lib.es.es_util.es_param import ESParamMustNotGroup
from sparrow_order_lib.es.es_util.es_param import ESParamPageGroup
from sparrow_order_lib.es.es_util.constants import ESParamOp
from sparrow_order_lib.es.es_util.constants import ESFieldType
from sparrow_order_lib.es.es_util.constants import ESQueryGroupName


field1 = ESField(path="field_1", type=ESFieldType.TEXT)
field2 = ESField(path="field_2", type=ESFieldType.TEXT)

param1 = ESParam(field1, ESParamOp.eq, "field_1_value")
param2 = ESParam(field2, ESParamOp.eq, "field_2_value")

param_for_one_group = ESParamsForOneGroup([param1, param2])


class TestESParam(unittest.TestCase):

    def test_ESParam_get_dsl(self):

        expected_dsl = {
            'term': {
                "field_1": "field_1_value"
            }
        }

        self.assertDictEqual(param1.get_dsl(), expected_dsl)

    def test_ESParamForOneGroup_get_dsl(self):

        excepted_dsl = [
            {
                'term': {
                    "field_1": "field_1_value"
                }
            },
            {
                'term': {
                    "field_2": "field_2_value"
                }
            }
        ]

        self.assertListEqual(param_for_one_group.get_dsl(), excepted_dsl)

    def test_ESParamMustGroup(self):
        must_group = ESParamGroup(param_for_one_group, query_name=ESQueryGroupName.MUST)
        self.assertIsInstance(must_group, ESParamMustGroup, msg="ESParamGroup 初始化 ESParamMustGroup 失败")

        expected_dsl = {
            'must': [
                {
                    'term': {
                        "field_1": "field_1_value"
                    }
                },
                {
                    'term': {
                        "field_2": "field_2_value"
                    }
                }
            ]
        }
        self.assertDictEqual(must_group.get_dsl(), expected_dsl)

    def test_ESParamMustNotGroup(self):
        must_not_group = ESParamGroup(param_for_one_group, query_name=ESQueryGroupName.MUST_NOT)
        self.assertIsInstance(must_not_group, ESParamMustNotGroup, msg="ESParamGroup 初始化 ESParamMustNotGroup 失败")

        expected_dsl = {
            'must_not': [
                {
                    'term': {
                        "field_1": "field_1_value"
                    }
                },
                {
                    'term': {
                        "field_2": "field_2_value"
                    }
                }
            ]
        }
        self.assertDictEqual(must_not_group.get_dsl(), expected_dsl)

    def test_ESParamShouldGroup(self):
        group = ESParamGroup(param_for_one_group, query_name=ESQueryGroupName.SHOULD)
        self.assertIsInstance(group, ESParamShouldGroup, msg="ESParamGroup 初始化 ESParamShouldGroup 失败")

        expected_dsl = {
            'should': [
                {
                    'term': {
                        "field_1": "field_1_value"
                    }
                },
                {
                    'term': {
                        "field_2": "field_2_value"
                    }
                }
            ]
        }
        self.assertDictEqual(group.get_dsl(), expected_dsl)

    def test_ESParamPageGroup(self):
        group = ESParamPageGroup(page=2, page_size=10)
        expected_dsl = {
            'size': 10,
            'from': 10
        }
        self.assertDictEqual(group.get_dsl(), expected_dsl)


if __name__ == '__main__':
    unittest.main()
