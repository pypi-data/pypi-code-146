import unittest

from sparrow_order_lib.es.es_util.base import __EXAMPLE_DOC_TYPE as EXAMPLE_DOC_TYPE
from sparrow_order_lib.es.es_util.es_query_util import ESQueryUtil
from sparrow_order_lib.es.es_util.in_query_param import InQueryParam
from sparrow_order_lib.es.es_util.es_param import ESParamShouldGroup
from sparrow_order_lib.es.es_util.es_param import ESParamPageGroup


class TestESQueryUtil(unittest.TestCase):

    example_util = ESQueryUtil(EXAMPLE_DOC_TYPE)

    def test_properties(self):
        ''' 测试 ESQueryUtil 对不可变属性的控制 '''

        self.assertRaises(
            AttributeError,
            setattr,
            self.example_util,
            'doc_type',
            'test_doc_type'
        )

        self.assertRaises(
            AttributeError,
            setattr,
            self.example_util,
            'mapping',
            {}
        )

        self.assertRaises(
            AttributeError,
            setattr,
            self.example_util,
            'query_mapping',
            {}
        )

    def test_get_es_query_param(self):
        in_param = InQueryParam(in_param_key='all_number', in_param_value='18512341234')
        res = self.example_util.get_es_query_param(in_param)

        self.assertIsInstance(res, ESParamShouldGroup, msg="Test ESQueryUtil.get_es_query_param Failed")

        expected_result = {
            'should': [
                {
                    'term': {'number': '18512341234'},
                },
                {
                    'nested': {
                        'path': 'inner',
                        'query': {
                            'bool': {
                                'filter': {
                                    'term': {
                                        'inner.number': '18512341234'
                                    }
                                }
                            }
                        }
                    }
                }
            ]
        }

        self.assertDictEqual(res.get_dsl(), expected_result, msg="Test ESQueryUtil.get_es_query_param Failed")

    def test_get_page_param_group(self):
        res = self.example_util.get_page_param_group(page=2, page_size=10)

        self.assertIsInstance(res, ESParamPageGroup)

        expected_result = {'from': 10, 'size': 10}

        self.assertDictEqual(res.get_dsl(), expected_result, msg="Test ESQueryUtil.get_page_param Failed")


if __name__ == '__main__':
    unittest.main()
