import unittest
import PIL.Image
import torch
from irisml.tasks.make_classification_dataset_from_object_detection import Task


class FakeDataset(torch.utils.data.Dataset):
    def __init__(self, data):
        self._data = data

    def __len__(self):
        return len(self._data)

    def __getitem__(self, index):
        return self._data[index]


class TestMakeClassificationDatasetFromObjectDetection(unittest.TestCase):
    def test_simple(self):
        fake_image = PIL.Image.new('RGB', (32, 32))
        dataset = FakeDataset([(fake_image, torch.tensor([[0, 0, 0, 0.5, 0.5], [1, 0, 0, 0.1, 0.1]])),
                               (fake_image, torch.tensor([[2, 0, 0, 0.5, 0.5], [3, 0, 0, 0.1, 0.1]]))])

        outputs = Task(Task.Config()).execute(Task.Inputs(dataset))
        self.assertEqual(len(outputs.dataset), 4)
        self.assertEqual(outputs.dataset[0][0].size, (16, 16))
        self.assertEqual(outputs.dataset[0][1], 0)
        self.assertEqual(outputs.dataset[1][0].size, (3, 3))
        self.assertEqual(outputs.dataset[1][1], 1)
        self.assertEqual(outputs.dataset[2][0].size, (16, 16))
        self.assertEqual(outputs.dataset[2][1], 2)
        self.assertEqual(outputs.dataset[3][0].size, (3, 3))
        self.assertEqual(outputs.dataset[3][1], 3)

    def test_given_multiclass_dataset(self):
        fake_image = PIL.Image.new('RGB', (32, 32))
        dataset = FakeDataset([(fake_image, torch.tensor(0)),
                               (fake_image, torch.tensor(1))])
        outputs = Task(Task.Config()).execute(Task.Inputs(dataset))
        self.assertEqual(len(outputs.dataset), 2)
        self.assertEqual(outputs.dataset[0][0].size, (32, 32))
        self.assertEqual(outputs.dataset[0][1], 0)
        self.assertEqual(outputs.dataset[1][1], 1)

    def test_given_multilabel_dataset(self):
        fake_image = PIL.Image.new('RGB', (32, 32))
        dataset = FakeDataset([(fake_image, torch.tensor([0, 1])),
                               (fake_image, torch.tensor([2, 3, 4]))])
        outputs = Task(Task.Config()).execute(Task.Inputs(dataset))
        self.assertEqual(len(outputs.dataset), 2)
        self.assertEqual(outputs.dataset[0][0].size, (32, 32))
        self.assertEqual(outputs.dataset[0][1].dim(), 1)
        self.assertEqual(outputs.dataset[1][1][2], 4)
