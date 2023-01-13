import unittest
from anagrams.exm import *


class TestsUnitFirst(unittest.TestCase):

    def test_isdigit(self):
        with self.assertRaises(AttributeError) as e:
            separate_word(1234)
        self.assertEqual("'int' object has no attribute 'split'", e.exception.args[0])

    def test_ttt(self):
        s = "abcd efgh"
        self.assertEqual(separate_word(s), "dcba hgfe")


unittest.main()
