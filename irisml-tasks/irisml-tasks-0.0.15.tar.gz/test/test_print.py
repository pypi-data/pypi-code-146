import unittest
import torch
from irisml.tasks.print import Task


class TestPrint(unittest.TestCase):
    def test_float(self):
        with self.assertLogs(level='INFO') as cm:
            Task(Task.Config()).execute(Task.Inputs(data_float=0.123))
            self.assertEqual(cm.output, ['INFO:irisml.tasks.print:0.123'])

    def test_pp_float(self):
        with self.assertLogs(level='INFO') as cm:
            Task(Task.Config(pretty=True)).execute(Task.Inputs(data_float=0.123))
            self.assertEqual(cm.output, ['INFO:irisml.tasks.print:0.123'])

    def test_dict_str_float(self):
        with self.assertLogs(level='INFO') as cm:
            Task(Task.Config()).execute(Task.Inputs(data_dict_str_float={'a': 0.1, 'b': 0.2}))
            self.assertEqual(cm.output, ["INFO:irisml.tasks.print:{'a': 0.1, 'b': 0.2}"])

    def test_tensor(self):
        with self.assertLogs(level='INFO') as cm:
            Task(Task.Config()).execute(Task.Inputs(data_tensor=torch.zeros(2)))
            self.assertEqual(cm.output, ['INFO:irisml.tasks.print:Tensor shape=torch.Size([2]), dtype=torch.float32',
                                         'INFO:irisml.tasks.print:tensor([0., 0.])'])

    def test_multiple_data(self):
        with self.assertRaises(ValueError):
            Task(Task.Config()).execute(Task.Inputs(data_int=3, data_float=0.1))

    def test_label(self):
        with self.assertLogs(level='INFO') as cm:
            Task(Task.Config('hello')).execute(Task.Inputs(data_float=0.123))
            self.assertEqual(cm.output, ['INFO:irisml.tasks.print:LABEL: hello', 'INFO:irisml.tasks.print:0.123'])
