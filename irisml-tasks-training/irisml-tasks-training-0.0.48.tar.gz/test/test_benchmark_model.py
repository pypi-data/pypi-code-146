import time
import unittest
import PIL.Image
import torch
import torchvision
from irisml.tasks.benchmark_model import Task


class FakeDataset:
    def __init__(self, data):
        self._data = data

    def __len__(self):
        return len(self._data)

    def __getitem__(self, index):
        return self._data[index]


class TestBenchmarkModel(unittest.TestCase):
    def test_simple_model(self):
        class FakeModel(torch.nn.Module):
            def training_step(self, inputs, targets):
                time.sleep(0.01)
                return {'loss': torch.tensor(1.0, requires_grad=True)}

            def prediction_step(self, inputs):
                time.sleep(0.01)
                return

        model = FakeModel()
        dataset = FakeDataset([(PIL.Image.new('RGB', (224, 224)), torch.tensor(1))] * 100)
        transform = torchvision.transforms.ToTensor()
        outputs = Task(Task.Config(1, 'cpu')).execute(Task.Inputs(model, dataset, transform))

        self.assertGreater(outputs.forward_time_per_iteration, 0.01)
        self.assertGreater(outputs.forward_backward_time_per_iteration, 0.01)
        self.assertGreater(outputs.prediction_time_per_iteration, 0.01)
        self.assertEqual(outputs.max_cuda_memory_in_mb, 0)  # On CPU

    def test_skip_training(self):
        class FakeModel(torch.nn.Module):  # Since this model doesn't have training_step(), it will fail if skip_training=False.
            def prediction_step(self, inputs):
                time.sleep(0.01)
                return

        model = FakeModel()
        dataset = FakeDataset([(PIL.Image.new('RGB', (224, 224)), torch.tensor(1))] * 100)
        transform = torchvision.transforms.ToTensor()
        outputs = Task(Task.Config(1, 'cpu', skip_training=True)).execute(Task.Inputs(model, dataset, transform))

        self.assertEqual(outputs.forward_time_per_iteration, 0)
        self.assertEqual(outputs.forward_backward_time_per_iteration, 0)
        self.assertGreater(outputs.prediction_time_per_iteration, 0.01)
        self.assertEqual(outputs.max_cuda_memory_in_mb, 0)  # On CPU

    def test_simple_model_with_tuple_inputs(self):
        class FakeModel(torch.nn.Module):
            def training_step(self, inputs, targets):
                time.sleep(0.01)
                return {'loss': torch.tensor(1.0, requires_grad=True)}

            def prediction_step(self, inputs):
                time.sleep(0.01)
                return

        model = FakeModel()
        dataset = FakeDataset([((PIL.Image.new('RGB', (224, 224)), torch.tensor([1, 2, 3])), torch.tensor(1))] * 100)

        def transform(inputs):
            return torchvision.transforms.functional.to_tensor(inputs[0]), inputs[1]
        outputs = Task(Task.Config(1, 'cpu')).execute(Task.Inputs(model, dataset, transform))

        self.assertGreater(outputs.forward_time_per_iteration, 0.01)

    def test_model_without_step_method(self):
        class FakeModel(torch.nn.Module):
            @property
            def criterion(self):
                return torch.nn.CrossEntropyLoss()

            def forward(self, x):
                time.sleep(0.01)
                return torch.zeros((x.shape[0], 8), requires_grad=True)

        model = FakeModel()
        dataset = FakeDataset([(PIL.Image.new('RGB', (224, 224)), torch.tensor(1))] * 100)
        transform = torchvision.transforms.ToTensor()
        outputs = Task(Task.Config(1, 'cpu')).execute(Task.Inputs(model, dataset, transform))
        self.assertGreater(outputs.forward_time_per_iteration, 0.01)
