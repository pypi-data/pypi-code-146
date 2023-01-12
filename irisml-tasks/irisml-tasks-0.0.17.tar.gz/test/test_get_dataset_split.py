import collections
import typing
import unittest
import torch
from irisml.tasks.get_dataset_split import Task


class DummyDataset(torch.utils.data.Dataset):
    def __init__(self, data: typing.List):
        self._data = data

    def __len__(self):
        return len(self._data)

    def __getitem__(self, x):
        return None, self._data[x]


class TestGetDatasetSubset(unittest.TestCase):
    def test_simple(self):
        dataset = DummyDataset(list(range(100)))

        inputs = Task.Inputs(train_dataset=dataset)
        config = Task.Config(train_val_split=0.8)

        outputs = Task(config).execute(inputs)
        self.assertEqual(len(outputs.train_dataset), 80)
        self.assertEqual(len(outputs.val_dataset), 20)

    def test_edge(self):
        dataset = DummyDataset(list(range(100)))

        inputs = Task.Inputs(train_dataset=dataset)
        config = Task.Config(train_val_split=0.0)

        outputs = Task(config).execute(inputs)
        self.assertEqual(len(outputs.train_dataset), 0)
        self.assertEqual(len(outputs.val_dataset), 100)

    def test_edge2(self):
        dataset = DummyDataset(list(range(100)))

        inputs = Task.Inputs(train_dataset=dataset)
        config = Task.Config(train_val_split=1.0)

        outputs = Task(config).execute(inputs)
        self.assertEqual(len(outputs.train_dataset), 100)
        self.assertEqual(len(outputs.val_dataset), 0)

    def test_keep_distribution(self):
        dataset = DummyDataset([torch.tensor(i // 10) for i in range(100)])

        outputs = Task(Task.Config(train_val_split=0.8, keep_class_distribution=True)).execute(Task.Inputs(dataset))
        class_counter = collections.Counter([int(x[1]) for x in outputs.train_dataset])
        self.assertEqual(list(class_counter.values()), [8] * 10)

        class_counter = collections.Counter([int(x[1]) for x in outputs.val_dataset])
        self.assertEqual(list(class_counter.values()), [2] * 10)

    def test_keep_distribution_train_prioritized(self):
        # Train classes should have at least one image.
        dataset = DummyDataset([torch.tensor(i) for i in range(100)])

        outputs = Task(Task.Config(train_val_split=0.8, keep_class_distribution=True)).execute(Task.Inputs(dataset))
        # Since each class has only 1 sample, all samples will be used in train dataset.
        self.assertEqual(len(outputs.train_dataset), 100)
        self.assertEqual(len(outputs.val_dataset), 0)

    def test_keep_distribution_od(self):
        dataset = DummyDataset([torch.tensor([[i // 10, 0, 0, 1, 1]]) for i in range(100)])

        outputs = Task(Task.Config(train_val_split=0.8, keep_class_distribution=True)).execute(Task.Inputs(dataset))
        class_counter = collections.Counter([int(x[1][0][0]) for x in outputs.train_dataset])
        self.assertEqual(list(class_counter.values()), [8] * 10)

    def test_keep_distribution_with_negative_samples(self):
        dataset = DummyDataset([torch.empty(0) for i in range(10)] + [torch.tensor(i // 10) for i in range(10, 100)])

        outputs = Task(Task.Config(train_val_split=0.8, keep_class_distribution=True)).execute(Task.Inputs(dataset))
        class_counter = collections.Counter([int(x[1]) for x in outputs.train_dataset if not x[1].shape or len(x[1])])
        self.assertEqual(list(class_counter.values()), [8] * 9)
        self.assertEqual(sum(1 for x, c in outputs.train_dataset if c.shape and len(c) == 0), 8)  # The number of negative samples.

        class_counter = collections.Counter([int(x[1]) for x in outputs.val_dataset if not x[1].shape or len(x[1])])
        self.assertEqual(list(class_counter.values()), [2] * 9)
        self.assertEqual(sum(1 for x, c in outputs.val_dataset if c.shape and len(c) == 0), 2)  # The number of negative samples.

    def test_keep_distribution_multilabel(self):
        dataset = DummyDataset([torch.tensor([i // 10, i % 2 + 10]) for i in range(100)])

        outputs = Task(Task.Config(train_val_split=0.8, keep_class_distribution=True)).execute(Task.Inputs(dataset))
        num_ten_class = sum(1 for x in outputs.train_dataset if 10 in x[1].tolist())
        self.assertGreater(num_ten_class, 30)

        num_ten_class = sum(1 for x in outputs.val_dataset if 10 in x[1].tolist())
        self.assertLess(num_ten_class, 20)
