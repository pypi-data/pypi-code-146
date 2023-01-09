import unittest
from unittest import mock

from sparrow_order_lib.es.es_util.es_door import ESDoor
from sparrow_order_lib.es.es_util.es_builder import ESBuilder
from sparrow_order_lib.es.es_util.base import __EXAMPLE_DOC_TYPE as EXAMPLE_DOC_TYPE


ESBuilder.__es = mock.Mock()


class TestESDoor(unittest.TestCase):

    def test_builder_in_es_door(self):
        door = ESDoor(
            query_type=EXAMPLE_DOC_TYPE,
            all_number='18512341234',
            main_id=10,
            created_time__before='2022-02-02 00:00:00',
            created_time__after='2022-01-01 00:00:00',
            page=3,
            page_size=10
        )

        builder = ESBuilder(EXAMPLE_DOC_TYPE)
        for query_group in door.es_params:
            builder.addQueryGroup(query_group)
        builder.addQueryGroup(door.es_query_util.get_page_param_group(door.page, door.page_size))

        expected_main_dsl = {
            'query': {
                'bool': {
                    'must': [
                        {
                            'term': {
                                'id': 10
                            }
                        },
                        {
                            'range': {
                                'created_time': {
                                    'lte': '2022-02-02 00:00:00',
                                    'time_zone': '+08:00'
                                }
                            }
                        },
                        {
                            'range': {
                                'created_time': {
                                    'gte': '2022-01-01 00:00:00',
                                    'time_zone': '+08:00'
                                }
                            }
                        },
                        {
                            'bool': {
                                'should': [
                                    {
                                        'term': {
                                            'number': '18512341234'
                                        }
                                    },
                                    {
                                        'nested': {
                                            'path': 'inner',
                                            'query': {
                                                'bool': {
                                                    'filter': {
                                                        'term': {'inner.number': '18512341234'}
                                                    }
                                                }
                                            }
                                        }
                                    }
                                ]
                            }
                        }
                    ]
                }
            }
        }

        self.assertDictEqual(builder.main_dsl, expected_main_dsl)

        expected_paged_dsl = {
            'from': 20,
            'size': 10
        }
        expected_paged_dsl.update(expected_main_dsl)

        self.assertDictEqual(builder.page_dsl, expected_paged_dsl)


if __name__ == '__main__':
    unittest.main()
