import io
import unittest
import torch
from irisml.tasks.predict_onnx import Task


class FakeDataset(torch.utils.data.Dataset):
    def __init__(self, data):
        self._data = data

    def __getitem__(self, index):
        return self._data[index]

    def __len__(self):
        return len(self._data)


class FakeModel(torch.nn.Module):
    def __init__(self):
        super().__init__()
        self.model = torch.nn.Conv2d(3, 3, 3)

    def forward(self, x):
        return self.predictor(torch.flatten(torch.nn.AdaptiveAvgPool2d(1)(self.model(x)), start_dim=1))

    @property
    def predictor(self):
        return torch.nn.Softmax(1)


def export_fake_model(input_size: int):
    model = FakeModel()
    x = torch.randn(1, 3, input_size, input_size)
    with io.BytesIO() as bytes_io:
        torch.onnx.export(model, x, bytes_io)
        return bytes(bytes_io.getbuffer())


def fake_transform(x, y):
    return x, y


class TestPredict(unittest.TestCase):
    def test_basic_inference(self):
        dataset = FakeDataset([[torch.rand(3, 256, 256), torch.tensor([1, 1, 1])], [torch.rand(3, 256, 256), torch.tensor([2, 2, 2])]])
        model_bytes = export_fake_model(256)

        inputs = Task.Inputs(dataset=dataset, transform=fake_transform, onnx_model_bytes=model_bytes)
        task = Task(Task.Config(device='cpu'))
        outputs = task.execute(inputs)

        self.assertEqual(len(outputs.predictions), len(dataset))
        self.assertEqual(len(outputs.targets), len(dataset))
        self.assertEqual(outputs.predictions.shape, outputs.targets.shape)
        self.assertIsInstance(outputs.predictions, torch.Tensor)
        self.assertIsInstance(outputs.targets, torch.Tensor)
