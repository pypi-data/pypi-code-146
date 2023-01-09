import unittest

from sparrow_order_lib.es.es_util.es_builder import ESBuilder
from sparrow_order_lib.es.es_util.es_query_util import ESQueryUtil
from sparrow_order_lib.es.es_util.in_query_param import InQueryParam
from sparrow_order_lib.es.es_util.base import __EXAMPLE_DOC_TYPE as EXAMPLE_DOC_TYPE


class TestESBuilder(unittest.TestCase):

    example_builder = ESBuilder(EXAMPLE_DOC_TYPE)

    def test_properties(self):
        self.assertRaises(
            AttributeError,
            setattr,
            self.example_builder,
            'main_dsl',
            {}
        )

        self.assertRaises(
            AttributeError,
            setattr,
            self.example_builder,
            'page_dsl',
            {}
        )

    def test_get_dsl(self):

        example_util = ESQueryUtil(EXAMPLE_DOC_TYPE)
        in_param = InQueryParam(in_param_key='all_number', in_param_value='18512341234')
        es_param = example_util.get_es_query_param(in_param)
        page_param = example_util.get_page_param_group(page=2, page_size=10)

        self.example_builder.addQueryGroup(es_param).addQueryGroup(page_param)

        expected_main_dsl = {
            'query': {
                'bool': {
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
            }
        }

        self.assertDictEqual(self.example_builder.main_dsl, expected_main_dsl, msg="Test ESBuilder.main_dsl Failed")

        expected_page_dls = {
            'from': 10,
            'size': 10
        }
        expected_page_dls.update(expected_main_dsl)

        self.assertDictEqual(self.example_builder.page_dsl, expected_page_dls, msg="Test ESBuilder.page_dsl Failed")


if __name__ == '__main__':
    unittest.main()
