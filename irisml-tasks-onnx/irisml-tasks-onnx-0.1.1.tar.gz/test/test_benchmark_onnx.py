import pathlib
import tempfile
import unittest
import torch
from irisml.tasks.benchmark_onnx import Task


class FakeDataset(torch.utils.data.Dataset):
    def __init__(self, data):
        super().__init__()
        self._data = data

    def __len__(self):
        return len(self._data)

    def __getitem__(self, index):
        return self._data[index]


def fake_transform(x):
    return x


class TestBenchmarkOnnx(unittest.TestCase):
    def test_simple(self):
        model = torch.nn.Conv2d(3, 3, 3)
        with tempfile.NamedTemporaryFile() as f:
            torch.onnx.export(model, torch.zeros(1, 3, 8, 8), f.name, input_names=['input'], output_names=['output'], dynamic_axes={'input': {0: 'batch'}, 'output': {0: 'batch'}})
            onnx_model_bytes = pathlib.Path(f.name).read_bytes()

        dataset = FakeDataset([(torch.zeros(3, 8, 8), torch.tensor(0)), (torch.zeros(3, 8, 8), torch.tensor(1))])
        outputs = Task(Task.Config(batch_size=1, device='cpu', num_iterations=2)).execute(Task.Inputs(onnx_model_bytes, dataset, fake_transform))
        self.assertGreater(outputs.prediction_time_per_iteration, 0)

        # batch_size=2
        outputs = Task(Task.Config(batch_size=2, device='cpu', num_iterations=2)).execute(Task.Inputs(onnx_model_bytes, dataset, fake_transform))
        self.assertGreater(outputs.prediction_time_per_iteration, 0)
