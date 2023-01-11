# Tests for fee management.
import unittest
from zope.interface.verify import verifyClass, verifyObject
from waeup.kofa.fees import IFeeTable
from waeup.kofa.fees import FeeTable, nested_list, nested_tuple

SAMPLE_PARAMS = (('locals', 'non-locals'), ('art', 'science'),
                 ('fac1', 'fac2'))

SAMPLE_VALUES = (((10, 20),   # locals, art, fac1/fac2
                  (11, 21)),  #         science, fac1/fac2
                 ((12, 22),   # non-locals, art, fac1/fac2
                  (13, 23)))  #         science, fac1/fac2

class HelperTests(unittest.TestCase):

    def test_nested_list(self):
        # we can turn nested lists into nested tuples
        self.assertEqual(
            nested_list(()), [])
        self.assertEqual(
            nested_list((1,)), [1])
        self.assertEqual(
            nested_list(((1,2), (3,))), [[1,2],[3]])
        self.assertEqual(
            nested_list((((1,2),(3,4)),(5,6))), [[[1,2],[3,4]],[5,6]])
        return

    def test_nested_tuples(self):
        # we can turn nested tuples into nested lists
        self.assertEqual(
            nested_tuple([]), ())
        self.assertEqual(
            nested_tuple([1,]), (1,))
        self.assertEqual(
            nested_tuple([[1,2], [3,]]), ((1,2),(3,)))
        self.assertEqual(
            nested_tuple([[[1,2],[3,4]],[5,6]]), (((1,2),(3,4)),(5,6)))
        return

class FeeTests(unittest.TestCase):

    def test_iface(self):
        # make sure, we comply with interfaces
        obj = FeeTable()
        verifyClass(IFeeTable, FeeTable)
        verifyObject(IFeeTable, obj)
        return

    def test_constructor(self):
        # we can set values in constructor
        fees = FeeTable(params=SAMPLE_PARAMS, values=SAMPLE_VALUES)
        self.assertEqual(fees.values, SAMPLE_VALUES)
        self.assertEqual(fees.params, SAMPLE_PARAMS)
        return

    def test_import_values(self):
        # we can import a set of values (clearing old stuff)
        fees = FeeTable()
        fees.import_values(SAMPLE_PARAMS, SAMPLE_VALUES)
        self.assertEqual(fees.params, SAMPLE_PARAMS)
        self.assertEqual(fees.values, SAMPLE_VALUES)
        return

    def test_import_values_no_values(self):
        # w/o values the table is emptied
        fees = FeeTable()
        fees.import_values()
        self.assertEqual(fees.params, ())
        self.assertEqual(fees.values, ())
        return

    def test_as_dict(self):
        # we can get a fee table as dict
        fees = FeeTable(SAMPLE_PARAMS, SAMPLE_VALUES)
        result = fees.as_dict()
        self.assertEqual(
            result,
            {
                ('locals', 'art', 'fac1'): 10,
                ('locals', 'science', 'fac1'): 11,
                ('non-locals', 'art', 'fac1'): 12,
                ('non-locals', 'science', 'fac1'): 13,
                ('locals', 'art', 'fac2'): 20,
                ('locals', 'science', 'fac2'): 21,
                ('non-locals', 'art', 'fac2'): 22,
                ('non-locals', 'science', 'fac2'): 23,
                }
            )

    def test_get_fee(self):
        # we can get values
        fees = FeeTable(SAMPLE_PARAMS, SAMPLE_VALUES)
        result1 = fees.get_fee(('locals', 'science', 'fac2'),)
        result2 = fees.get_fee(('non-locals', 'art', 'fac1'),)
        self.assertEqual(result1, 21)
        self.assertEqual(result2, 12)
        return

    def test_get_fee_invalid_key(self):
        # invalid param values will raise a key error
        fees = FeeTable(SAMPLE_PARAMS, SAMPLE_VALUES)
        self.assertRaises(
            KeyError, fees.get_fee, ('NONSENSE', 'science', 'fac2'))
        self.assertRaises(
            KeyError, fees.get_fee, ('locals', 'NONSENSE', 'fac2'))
        self.assertRaises(
            KeyError, fees.get_fee, ('locals', 'science', 'NONSENSE'))
        # also the order of params matters
        self.assertRaises( # 'science' and 'locals' is wrong order...
            KeyError, fees.get_fee, ('science', 'locals', 'fac2'))
        return

    def test_set_fee(self):
        # we can set values
        fees = FeeTable(SAMPLE_PARAMS, SAMPLE_VALUES)
        result1 = fees.get_fee(('locals', 'science', 'fac2'),)
        fees.set_fee(('locals', 'science', 'fac2'), 42)
        result2 = fees.get_fee(('locals', 'science', 'fac2'),)
        self.assertEqual(result1, 21)
        self.assertEqual(result2, 42)
        return

    def test_set_fee_invalid(self):
        # invalid param values will raise a key error
        fees = FeeTable(SAMPLE_PARAMS, SAMPLE_VALUES)
        self.assertRaises(
            KeyError, fees.set_fee, ('NONSENSE', 'science', 'fac2'), 12)
        self.assertRaises(
            KeyError, fees.set_fee, ('locals', 'NONSENSE', 'fac2'), 12)
        self.assertRaises(
            KeyError, fees.set_fee, ('locals', 'science', 'NONSENSE'), 12)
       # also the order of params matters
        self.assertRaises( # 'science' and 'locals' is wrong order...
            KeyError, fees.set_fee, ('science', 'locals', 'fac2'), 12)
        return
