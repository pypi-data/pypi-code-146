import unittest
import torch.nn
from irisml.tasks.check_model_parameters import Task


class TestCheckModelParameters(unittest.TestCase):
    def test_ok_model(self):
        model = torch.nn.Conv2d(3, 3, 3)
        outputs = Task(Task.Config(throw_exception=False)).execute(Task.Inputs(model))
        self.assertFalse(outputs.has_nan_or_inf)

    def test_nan_model(self):
        model = torch.nn.Conv2d(3, 3, 3)
        model.weight.data = model.weight.data * float('nan')
        outputs = Task(Task.Config(throw_exception=False)).execute(Task.Inputs(model))
        self.assertTrue(outputs.has_nan_or_inf)

        model.weight.data = model.weight.data * float('inf')
        outputs = Task(Task.Config(throw_exception=False)).execute(Task.Inputs(model))
        self.assertTrue(outputs.has_nan_or_inf)

    def test_throw_exception(self):
        model = torch.nn.Conv2d(3, 3, 3)
        model.weight.data = model.weight.data * float('nan')
        with self.assertRaises(ValueError):
            Task(Task.Config(throw_exception=True)).execute(Task.Inputs(model))
