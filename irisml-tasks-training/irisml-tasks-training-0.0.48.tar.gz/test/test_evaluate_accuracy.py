import unittest
import torch
from irisml.tasks.evaluate_accuracy import Task


class TestEvaluateAccuracy(unittest.TestCase):
    def test_simple(self):
        predictions = torch.Tensor([[0.1, 0.2, 0.1], [0.9, 0.2, 0.2], [0.4, 0.4, 0.8]])
        targets = torch.Tensor([1, 0, 2])
        outputs = Task(Task.Config()).execute(Task.Inputs(predictions, targets))

        self.assertEqual(outputs.accuracy, 1.0)

        targets = torch.Tensor([2, 1, 1])
        outputs = Task(Task.Config()).execute(Task.Inputs(predictions, targets))
        self.assertEqual(outputs.accuracy, 0.0)

    def test_list_targets(self):
        predictions = torch.Tensor([[0.1, 0.2, 0.1], [0.9, 0.2, 0.2], [0.4, 0.4, 0.8]])
        targets = torch.Tensor([[1], [0], [2]])
        outputs = Task(Task.Config()).execute(Task.Inputs(predictions, targets))

        self.assertEqual(outputs.accuracy, 1.0)
