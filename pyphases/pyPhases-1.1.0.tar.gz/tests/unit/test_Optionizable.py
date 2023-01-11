import unittest
from pyPhases.util.Optionizable import MissingOption, Optionizable

class TestOptionizable(unittest.TestCase):
    def setUp(self):
        self.options = {"option1": "value1", "option2": "value2"}
        self.optionizable = Optionizable(self.options)

    def test_getOption(self):
        self.assertEqual(self.optionizable.getOption("option1"), "value1")
        self.assertEqual(self.optionizable.getOption("option2"), "value2")
        self.assertRaises(MissingOption, self.optionizable.getOption, "option3")

    def test_initialOptions(self):
        self.assertDictEqual(self.optionizable.initialOptions(), {})


