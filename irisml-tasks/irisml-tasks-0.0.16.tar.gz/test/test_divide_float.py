import unittest
from irisml.tasks.divide_float import Task


class TestDivideFloat(unittest.TestCase):
    def test_simple(self):
        outputs = Task(Task.Config()).execute(Task.Inputs(3, 2))
        self.assertEqual(outputs.result, 1.5)

    def test_zero_division(self):
        with self.assertRaises(ZeroDivisionError):
            Task(Task.Config()).execute(Task.Inputs(3, 0))
