import unittest
import torch
from irisml.tasks.make_oversampled_dataset import Task


class TestMakeOversampledDataset(unittest.TestCase):
    def test_get_class_id(self):
        def assert_result(input_targets, expected_class_ids):
            outputs = Task._get_class_id((None, input_targets))
            self.assertEqual(set(outputs), set(expected_class_ids))

        assert_result(1, [1])
        assert_result(0, [0])
        assert_result([1, 2, 3], [1, 2, 3])
        assert_result(0.1, [])
        assert_result([0.1], [])
        assert_result([], [])
        assert_result([[]], [])
        assert_result([[3, 0.1, 0.1, 0.1, 0.1]], [3])
        assert_result(torch.tensor(1), [1])
        assert_result(torch.tensor([1]), [1])
        assert_result(torch.tensor([1, 2, 3]), [1, 2, 3])
        assert_result(torch.tensor([[3, 1.0, 2.0, 3.0, 4.0]]), [3])
        assert_result(torch.tensor(2.0), [])

    def test_calculate_weights(self):
        dataset = [(None, [1]), (None, [1]), (None, [0])]
        results = Task._calculcate_weights(dataset, 100, 0)
        self.assertEqual(results[0], results[1])
        self.assertGreater(results[2], results[0])

    def test_min_num_samples(self):
        dataset = [(None, [1]), (None, [1]), (None, [0])]
        outputs = Task(Task.Config(10)).execute(Task.Inputs(dataset))
        self.assertEqual(len(outputs.dataset), 10)
        self.assertIsNotNone(outputs.dataset[0])
        self.assertIsNotNone(outputs.dataset[9])

        dataset = [(None, [1]), (None, [1]), (None, [0])]
        outputs = Task(Task.Config(3)).execute(Task.Inputs(dataset))
        self.assertEqual(outputs.dataset, dataset)  # no oversampling

    def test_oversampling_rate(self):
        dataset = [(None, [1]), (None, [1]), (None, [0])]
        outputs = Task(Task.Config(0, 3)).execute(Task.Inputs(dataset))
        self.assertEqual(len(outputs.dataset), 9)

        dataset = [(None, [1]), (None, [1]), (None, [0])]
        outputs = Task(Task.Config(0, 1)).execute(Task.Inputs(dataset))
        self.assertEqual(outputs.dataset, dataset)  # no oversampling

    def test_balancing(self):
        dataset = [(None, [1]), (None, [1]), (None, [0])]
        outputs = Task(Task.Config(0, 3, balance=True)).execute(Task.Inputs(dataset))
        self.assertEqual(len(outputs.dataset), 9)
