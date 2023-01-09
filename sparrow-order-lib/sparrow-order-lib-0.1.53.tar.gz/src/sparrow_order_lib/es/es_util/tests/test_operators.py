import unittest

from sparrow_order_lib.es.es_util.field import ESField
from sparrow_order_lib.es.es_util.constants import ESParamOp
from sparrow_order_lib.es.es_util.constants import ESFieldType


class TestOperators(unittest.TestCase):

    field = ESField(path="test_operator", type=ESFieldType.TEXT)

    test_value = 'test_value'

    integer_field = ESField(path='test_integer_operator', type=ESFieldType.INTEGER)

    test_integer_value = 2

    def test_term_operator(self):

        expected_result = {'term': {'test_operator': self.test_value}}

        self.assertDictEqual(self.field == self.test_value, expected_result, msg="Test Operator term failed")

    def test_terms_operator(self):

        expected_result = {'terms': {'test_operator': [self.test_value]}}

        self.assertDictEqual(self.field.in_([self.test_value]), expected_result, msg="Test Operator terms failed")

    def test_wildcard_operator(self):

        expected_result = {'wildcard': {'test_operator': self.test_value}}

        self.assertDictEqual(self.field.like(self.test_value), expected_result, msg="Test Operator wildcard failed")

    def test_range_operator(self):

        core = {ESParamOp.gt: self.test_integer_value}
        expected_result = {'range': {'test_integer_operator': core}}
        self.assertDictEqual(self.integer_field > self.test_integer_value, expected_result, "Test Operator range failed")

        core = {ESParamOp.gte: self.test_integer_value}
        expected_result = {'range': {'test_integer_operator': core}}
        self.assertDictEqual(self.integer_field >= self.test_integer_value, expected_result, "Test Operator range failed")

        core = {ESParamOp.lt: self.test_integer_value}
        expected_result = {'range': {'test_integer_operator': core}}
        self.assertDictEqual(self.integer_field < self.test_integer_value, expected_result, "Test Operator range failed")

        core = {ESParamOp.lte: self.test_integer_value}
        expected_result = {'range': {'test_integer_operator': core}}
        self.assertDictEqual(self.integer_field <= self.test_integer_value, expected_result, "Test Operator range failed")


if __name__ == '__main__':
    unittest.main()
