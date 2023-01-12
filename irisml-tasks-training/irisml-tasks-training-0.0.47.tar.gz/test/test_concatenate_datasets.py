import unittest
import torch
from irisml.tasks.concatenate_datasets import Task


class FakeDataset(torch.utils.data.Dataset):
    def __init__(self, data):
        self._data = data

    def __len__(self):
        return len(self._data)

    def __getitem__(self, index):
        return self._data[index]


class TestConcatenateDatasets(unittest.TestCase):
    def test_same_classsspace_classification(self):
        dataset0 = FakeDataset([(None, torch.tensor(1)), (None, torch.tensor(2)), (None, torch.tensor(3))])
        dataset1 = FakeDataset([(None, torch.tensor(1)), (None, torch.tensor(2)), (None, torch.tensor(3))])
        outputs = Task(Task.Config(use_same_classspace=True)).execute(Task.Inputs(dataset0, dataset1))
        self.assertEqual(len(outputs.dataset), 6)
        self.assertEqual(outputs.dataset[0], (None, torch.tensor(1)))
        self.assertEqual(outputs.dataset[3], (None, torch.tensor(1)))
        self.assertEqual(outputs.dataset[5], (None, torch.tensor(3)))

    def test_different_classsspace_classification_with_same_name(self):
        dataset0 = FakeDataset([(None, torch.tensor(1)), (None, torch.tensor(2)), (None, torch.tensor(3))])
        dataset1 = FakeDataset([(None, torch.tensor(1)), (None, torch.tensor(2)), (None, torch.tensor(3))])
        class_names0 = ['label0', 'label1', 'label2', 'label3', 'label4']
        class_names1 = ['label0', 'label1', 'label2', 'label3', 'label4']
        outputs = Task(Task.Config(use_same_classspace=False)).execute(Task.Inputs(dataset0, dataset1, class_names0, class_names1))
        self.assertEqual(len(outputs.dataset), 6)
        self.assertEqual(outputs.dataset[0], (None, torch.tensor(1)))
        self.assertEqual(outputs.dataset[3], (None, torch.tensor(1)))
        self.assertEqual(outputs.dataset[5], (None, torch.tensor(3)))

    def test_different_classsspace_classification(self):
        dataset0 = FakeDataset([(None, torch.tensor(1)), (None, torch.tensor(2)), (None, torch.tensor(3))])
        dataset1 = FakeDataset([(None, torch.tensor(1)), (None, torch.tensor(2)), (None, torch.tensor(3))])
        class_names0 = ['label0', 'label1', 'label2', 'label3', 'label4']
        class_names1 = ['label00', 'label01', 'label02', 'label03', 'label04']
        outputs = Task(Task.Config(use_same_classspace=False)).execute(Task.Inputs(dataset0, dataset1, class_names0, class_names1))
        self.assertEqual(len(outputs.dataset), 6)
        self.assertEqual(outputs.dataset[0], (None, torch.tensor(1)))
        self.assertEqual(outputs.dataset[3], (None, torch.tensor(6)))
        self.assertEqual(outputs.dataset[5], (None, torch.tensor(8)))

    def test_different_classsspace_classification_with_duplicated_names(self):
        dataset0 = FakeDataset([(None, torch.tensor(1)), (None, torch.tensor(2)), (None, torch.tensor(3))])
        dataset1 = FakeDataset([(None, torch.tensor(1)), (None, torch.tensor(2)), (None, torch.tensor(3))])
        class_names0 = ['label0', 'label1', 'label2', 'label3', 'label4']
        class_names1 = ['label0', 'label1', 'label02', 'label03', 'label04']
        outputs = Task(Task.Config(use_same_classspace=False)).execute(Task.Inputs(dataset0, dataset1, class_names0, class_names1))
        self.assertEqual(len(outputs.dataset), 6)
        self.assertEqual(outputs.dataset[0], (None, torch.tensor(1)))
        self.assertEqual(outputs.dataset[3], (None, torch.tensor(1)))
        self.assertEqual(outputs.dataset[5], (None, torch.tensor(6)))

    def test_different_classsspace_object_detection_with_duplicated_names(self):
        dataset0 = FakeDataset([(None, torch.tensor([[1, 0, 0, 1, 1]])), (None, torch.tensor([[2, 0, 0, 1, 1]])), (None, torch.tensor([[3, 0, 0, 1, 1]]))])
        dataset1 = FakeDataset([(None, torch.tensor([[1, 0, 0, 1, 1]])), (None, torch.tensor([[2, 0, 0, 1, 1], [4, 0, 0, 1, 1]])), (None, torch.tensor([[3, 0, 0, 1, 1]]))])
        class_names0 = ['label0', 'label1', 'label2', 'label3', 'label4']
        class_names1 = ['label0', 'label1', 'label02', 'label03', 'label04']
        outputs = Task(Task.Config(use_same_classspace=False, task_type='object_detection')).execute(Task.Inputs(dataset0, dataset1, class_names0, class_names1))
        self.assertEqual(len(outputs.dataset), 6)
        self.assertTrue(torch.equal(outputs.dataset[0][1], torch.tensor([[1, 0, 0, 1, 1]])))
        self.assertTrue(torch.equal(outputs.dataset[3][1], torch.tensor([[1, 0, 0, 1, 1]])))
        self.assertTrue(torch.equal(outputs.dataset[5][1], torch.tensor([[6, 0, 0, 1, 1]])))

    def test_no_second_dataset(self):
        dataset0 = FakeDataset([(None, torch.tensor(1)), (None, torch.tensor(2)), (None, torch.tensor(3))])
        outputs = Task(Task.Config()).execute(Task.Inputs(dataset0, None))
        self.assertEqual(outputs.dataset, dataset0)
