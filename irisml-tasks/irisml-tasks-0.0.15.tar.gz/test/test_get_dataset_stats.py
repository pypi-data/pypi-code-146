import unittest
import torch
from irisml.tasks.get_dataset_stats import Task


class FakeDataset(torch.utils.data.Dataset):
    def __init__(self, data):
        self._data = data

    def __len__(self):
        return len(self._data)

    def __getitem__(self, index):
        return self._data[index]


class TestGetDatasetStats(unittest.TestCase):
    def test_multiclass_classification(self):
        dataset = FakeDataset([(torch.zeros((3, 100, 100)), torch.tensor([0])),
                               (torch.zeros((3, 100, 100)), torch.tensor([1])),
                               (torch.zeros((3, 100, 100)), torch.tensor([2]))])
        task = Task(Task.Config())
        outputs = task.execute(Task.Inputs(dataset))
        self.assertEqual(outputs.num_images, 3)
        self.assertEqual(outputs.num_classes, 3)
        self.assertEqual(outputs.dataset_type, 'multiclass_classification')

    def test_multiclass_classification_scalar(self):
        dataset = FakeDataset([(torch.zeros((3, 100, 100)), torch.tensor(0)),
                               (torch.zeros((3, 100, 100)), torch.tensor(1)),
                               (torch.zeros((3, 100, 100)), torch.tensor(2))])
        task = Task(Task.Config())
        outputs = task.execute(Task.Inputs(dataset))
        self.assertEqual(outputs.num_images, 3)
        self.assertEqual(outputs.num_classes, 3)
        self.assertEqual(outputs.dataset_type, 'multiclass_classification')

    def test_multilabel_classification(self):
        dataset = FakeDataset([(torch.zeros((3, 100, 100)), torch.tensor([0, 1, 2])),
                               (torch.zeros((3, 100, 100)), torch.tensor([0])),
                               (torch.zeros((3, 100, 100)), torch.tensor([]))])
        task = Task(Task.Config())
        outputs = task.execute(Task.Inputs(dataset))
        self.assertEqual(outputs.num_images, 3)
        self.assertEqual(outputs.num_classes, 3)
        self.assertEqual(outputs.dataset_type, 'multilabel_classification')

    def test_object_detection(self):
        dataset = FakeDataset([(torch.zeros((3, 100, 100)), torch.tensor([[0, 0.1, 0.1, 0.2, 0.2], [1, 0.1, 0.1, 0.2, 0.2], [2, 0.1, 0.1, 0.2, 0.2]])),
                               (torch.zeros((3, 100, 100)), torch.tensor([[0, 0.1, 0.1, 0.2, 0.2]])),
                               (torch.zeros((3, 100, 100)), torch.tensor([]))])
        task = Task(Task.Config())
        outputs = task.execute(Task.Inputs(dataset))
        self.assertEqual(outputs.num_images, 3)
        self.assertEqual(outputs.num_classes, 3)
        self.assertEqual(outputs.dataset_type, 'object_detection')
