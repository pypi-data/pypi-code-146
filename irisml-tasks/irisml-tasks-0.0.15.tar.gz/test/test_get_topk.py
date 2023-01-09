import unittest
import torch
from irisml.tasks.get_topk import Task


class TestGetTopk(unittest.TestCase):
    def test_2d(self):
        tensor = torch.randn(10, 24)
        outputs = Task(Task.Config(3)).execute(Task.Inputs(tensor))
        self.assertEqual(outputs.values.shape, (10, 3))
        self.assertEqual(outputs.indices.shape, (10, 3))

        topk_results = torch.topk(tensor, 3)
        self.assertTrue(torch.all(outputs.values == topk_results.values))
        self.assertTrue(torch.all(outputs.indices == topk_results.indices))

    def test_3d(self):
        tensor = torch.randn(10, 8, 24)
        outputs = Task(Task.Config(3)).execute(Task.Inputs(tensor))
        self.assertEqual(outputs.values.shape, (10, 8, 3))
        self.assertEqual(outputs.indices.shape, (10, 8, 3))

        topk_results = torch.topk(tensor, 3)
        self.assertTrue(torch.all(outputs.values == topk_results.values))
        self.assertTrue(torch.all(outputs.indices == topk_results.indices))

    def test_dry_run(self):
        tensor = torch.randn(10, 24)
        outputs = Task(Task.Config(3)).dry_run(Task.Inputs(tensor))
        self.assertEqual(outputs.values.shape, (10, 3))
        self.assertEqual(outputs.indices.shape, (10, 3))
