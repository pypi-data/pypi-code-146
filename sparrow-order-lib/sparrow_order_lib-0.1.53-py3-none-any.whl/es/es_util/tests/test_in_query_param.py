from unittest import TestCase
import unittest

from sparrow_order_lib.es.es_util.in_query_param import InQueryParam


class TestInQueryParam(TestCase):

    def test_properties(self):
        in_param = InQueryParam('test_key', 'test_value')
        # in_param.in_param_key = 1
        self.assertRaises(AttributeError, setattr, in_param, 'in_param_key', 'test_value_2')
        self.assertRaises(AttributeError, setattr, in_param, 'in_param_value', 'test_value_2')


if __name__ == '__main__':
    unittest.main()
