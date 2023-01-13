from qpi import functions
from qpi.tests import tools
import unittest


class FunctionsTest(unittest.TestCase):
    def test_expand_values(self):
        kwargs = {'was_key': 'was_value'}
        functions.expand_kwargs(kwargs, new_key='new_value')
        self.assertTrue(kwargs == {'was_key': 'was_value', 'new_key': 'new_value'})

    def test_execute_method_decorator(self):
        res_success = functions.execute_method_decorator('test_func_success')(tools.some_test_func_success)()
        self.assertTrue(res_success == 'Success')
        res_fail = functions.execute_method_decorator('test_func_fail')(tools.some_test_func_fail)()
        self.assertTrue(res_fail == 'Fail')


if __name__ == '__main__':
    unittest.main()
