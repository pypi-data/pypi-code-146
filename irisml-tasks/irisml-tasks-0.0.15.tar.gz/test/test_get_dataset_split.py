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
        return self._data[x]


class TestGetDatasetSubset(unittest.TestCase):
    def test_simple(self):
        dataset = DummyDataset(list(range(100)))

        inputs = Task.Inputs(train_dataset=dataset)
        config = Task.Config(train_val_split=0.8)

        task = Task(config)
        outputs = task.execute(inputs)
        self.assertEqual(len(outputs.train_dataset), 80)
        self.assertEqual(len(outputs.val_dataset), 20)

    def test_edge(self):
        dataset = DummyDataset(list(range(100)))

        inputs = Task.Inputs(train_dataset=dataset)
        config = Task.Config(train_val_split=0.0)

        task = Task(config)
        outputs = task.execute(inputs)
        self.assertEqual(len(outputs.train_dataset), 0)
        self.assertEqual(len(outputs.val_dataset), 100)

    def test_edge2(self):
        dataset = DummyDataset(list(range(100)))

        inputs = Task.Inputs(train_dataset=dataset)
        config = Task.Config(train_val_split=1.0)

        task = Task(config)
        outputs = task.execute(inputs)
        self.assertEqual(len(outputs.train_dataset), 100)
        self.assertEqual(len(outputs.val_dataset), 0)
