import random
import unittest
import torch.utils.data
from irisml.tasks.get_kfold_cross_validation_dataset import Task


class NumberDataset(torch.utils.data.Dataset):
    def __init__(self, num_samples):
        self._num_samples = num_samples

    def __len__(self):
        return self._num_samples

    def __getitem__(self, index):
        return index


class TestGetKfoldCrossValidationDataset(unittest.TestCase):
    def test_simple(self):
        dataset = NumberDataset(100)

        random.seed(0)
        outputs0 = Task(Task.Config(num_folds=3, index=0)).execute(Task.Inputs(dataset))
        self.assertEqual(len(outputs0.train_dataset), 66)
        self.assertEqual(len(outputs0.val_dataset), 34)
        self.assertEqual(set(outputs0.train_dataset) | set(outputs0.val_dataset), set(range(100)))

        random.seed(0)
        outputs1 = Task(Task.Config(num_folds=3, index=1)).execute(Task.Inputs(dataset))
        self.assertEqual(len(outputs1.train_dataset), 67)
        self.assertEqual(len(outputs1.val_dataset), 33)
        self.assertEqual(set(outputs1.train_dataset) | set(outputs1.val_dataset), set(range(100)))

        random.seed(0)
        outputs2 = Task(Task.Config(num_folds=3, index=2)).execute(Task.Inputs(dataset))
        self.assertEqual(len(outputs2.train_dataset), 67)
        self.assertEqual(len(outputs2.val_dataset), 33)
        self.assertEqual(set(outputs2.train_dataset) | set(outputs2.val_dataset), set(range(100)))

        self.assertEqual(set(outputs0.val_dataset) | set(outputs1.val_dataset) | set(outputs2.val_dataset), set(range(100)))
