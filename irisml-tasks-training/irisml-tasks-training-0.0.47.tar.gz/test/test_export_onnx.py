import unittest
import torch
from irisml.core import Context
from irisml.tasks.export_onnx import Task


class TestExportOnnx(unittest.TestCase):
    def test_model_with_prediction_step(self):
        class FakeModel(torch.nn.Module):
            def __init__(self):
                super().__init__()
                self._model = torch.nn.Conv2d(3, 3, 3)
                self._predictor = torch.nn.Softmax(1)

            def prediction_step(self, x):
                return self._predictor(self(x))

            def forward(self, x):
                return self._model(x)

        model = FakeModel()

        task = Task(Task.Config(), Context())
        outputs = task.execute(Task.Inputs(model))
        self.assertIsNotNone(outputs)

    def test_model_with_predictor(self):
        class FakeModel(torch.nn.Module):
            def __init__(self):
                super().__init__()
                self._model = torch.nn.Conv2d(3, 3, 3)
                self._predictor = torch.nn.Softmax(1)

            @property
            def predictor(self):
                return self._predictor

            def forward(self, x):
                return self._model(x)

        model = FakeModel()

        task = Task(Task.Config(), Context())
        outputs = task.execute(Task.Inputs(model))
        self.assertIsNotNone(outputs)

    def test_model_without_predictor(self):
        class FakeModel(torch.nn.Module):
            def __init__(self):
                super().__init__()
                self._model = torch.nn.Conv2d(3, 3, 3)

            def forward(self, x):
                return self._model(x)

        model = FakeModel()

        task = Task(Task.Config(), Context())
        outputs = task.execute(Task.Inputs(model))
        self.assertIsNotNone(outputs)
