import copy
import random
import unittest
from unittest.mock import MagicMock
import torch
from irisml.tasks.train_with_gradient_cache import Task, GradientCachingTrainer


def fake_transform(x, y):
    return x, y


class FakeModel(torch.nn.Module):
    def __init__(self):
        super().__init__()
        self._model = torch.nn.Sequential(torch.nn.Conv2d(3, 3, 3), torch.nn.AdaptiveAvgPool2d(1))
        self.call_count = 0

    def forward(self, x):
        self.call_count += 1
        return self._model(x)

    @property
    def criterion(self):
        return torch.nn.L1Loss()

    @property
    def predictor(self):
        return torch.nn.Identity()


class FakeDataset(torch.utils.data.Dataset):
    def __init__(self, num_samples):
        self._num_samples = num_samples

    def __len__(self):
        return self._num_samples

    def __getitem__(self, index):
        return torch.zeros((3, 4, 4)), torch.zeros((3, ))


class TestTrainWithGradientCache(unittest.TestCase):
    def test_train(self):
        config = Task.Config(num_epochs=3, batch_size=2)
        model = FakeModel()
        dataset = FakeDataset(4)
        transform = fake_transform
        outputs = Task(config).execute(Task.Inputs(model, dataset, transform))
        self.assertIsNotNone(outputs.model)
        self.assertEqual(model.call_count, 0)  # Input model is not modified.
        self.assertEqual(outputs.model.call_count, 24)  # 4 iterations per epoch, 3 epochs, then twice for gradient caching.

    def test_split_tensor_or_list(self):
        trainer = GradientCachingTrainer(sub_batch_size=2, model=MagicMock(), lr_scheduler_factory=MagicMock(), optimizer_factory=MagicMock())
        results = trainer._split_tensor_or_list(torch.tensor([[3]] * 4))
        self.assertIsInstance(results, tuple)
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0].shape, (2, 1))

        results = trainer._split_tensor_or_list((torch.tensor([[3]] * 4), torch.tensor([[2, 2]] * 4)))
        self.assertIsInstance(results, list)
        self.assertEqual(len(results), 2)
        self.assertIsInstance(results[0], tuple)
        self.assertEqual(results[0][0].shape, (2, 1))
        self.assertEqual(results[0][1].shape, (2, 2))
        self.assertEqual(results[1][0].shape, (2, 1))
        self.assertEqual(results[1][1].shape, (2, 2))

        # scalar tensor is returned as-is.
        results = trainer._split_tensor_or_list(torch.tensor(3))
        self.assertEqual(results, torch.tensor(3))

    def test_single_feature(self):
        class Model(torch.nn.Module):
            def __init__(self):
                super().__init__()
                self._model = torch.nn.Conv2d(3, 3, 3)

            @property
            def criterion(self):
                return torch.nn.CrossEntropyLoss()

            def forward(self, inputs):
                return self._model(inputs).flatten(1)

        self._check_with_model(Model())

    def test_three_features(self):
        class Model(torch.nn.Module):
            class Criterion(torch.nn.Module):
                def forward(self, features, targets):
                    return sum(torch.nn.functional.cross_entropy(f, targets) for f in features)

            def __init__(self):
                super().__init__()
                self._model = torch.nn.Conv2d(3, 3, 3)
                self._model2 = torch.nn.Conv2d(3, 3, 3)
                self._model3 = torch.nn.Conv2d(3, 3, 3)

            @property
            def criterion(self):
                return self.Criterion()

            def forward(self, inputs):
                return self._model(inputs).flatten(1), self._model2(inputs).flatten(1), self._model3(inputs).flatten(1)

        self._check_with_model(Model())

    def test_scalar_feature(self):
        class Model(torch.nn.Module):
            class Criterion(torch.nn.Module):
                def forward(self, features, targets):
                    return torch.sum(features[0]) + torch.sum(features[1])

            def __init__(self):
                super().__init__()
                self._model = torch.nn.Conv2d(3, 3, 3)
                self._param = torch.nn.Parameter(torch.tensor(0.1))

            @property
            def criterion(self):
                return self.Criterion()

            def forward(self, inputs):
                return self._param, self._model(inputs)

        self._check_with_model(Model())

    def test_two_inputs(self):
        class Dataset(torch.utils.data.Dataset):
            def __init__(self, num_examples=8, num_classes=3):
                self._data = [((torch.rand(3, 3, 3), torch.rand(4, 3, 3)), 0)] * num_examples

            def __len__(self):
                return len(self._data)

            def __getitem__(self, index):
                return self._data[index]

        class FakeModel(torch.nn.Module):
            class Criterion(torch.nn.Module):
                def forward(self, features, targets):
                    return sum(torch.sum(f) for f in features)

            def __init__(self):
                super().__init__()
                self._conv = torch.nn.Conv2d(3, 3, 3)
                self._conv2 = torch.nn.Conv2d(4, 3, 3)
                self._received_inputs = []

            def forward(self, inputs):
                self._received_inputs.append(copy.deepcopy(inputs))
                return self._conv(inputs[0]).flatten(1), self._conv2(inputs[1]).flatten(1)

            @property
            def criterion(self):
                return self.Criterion()

        dataset = Dataset()
        model = FakeModel()
        config = Task.Config(batch_size=4, sub_batch_size=1, num_epochs=1)
        outputs = Task(config).execute(Task.Inputs(model, dataset, fake_transform))
        self.assertTrue(all(torch.allclose(dataset[0][0][0], i[0]) for i in outputs.model._received_inputs))
        self.assertTrue(all(torch.allclose(dataset[0][0][1], i[1]) for i in outputs.model._received_inputs))

    def _check_with_model(self, model):
        class Dataset(torch.utils.data.Dataset):
            def __init__(self, num_examples=8, num_classes=3):
                self._data = [(torch.rand(3, 3, 3), random.randrange(num_classes)) for i in range(num_examples)]

            def __len__(self):
                return len(self._data)

            def __getitem__(self, index):
                return self._data[index]

        dataset = Dataset()

        torch.manual_seed(0)
        config = Task.Config(batch_size=4, sub_batch_size=1, num_epochs=1, base_lr=1)
        outputs = Task(config).execute(Task.Inputs(copy.deepcopy(model), dataset, fake_transform))
        model0 = outputs.model

        torch.manual_seed(0)
        config = Task.Config(batch_size=4, sub_batch_size=2, num_epochs=1, base_lr=1)
        outputs = Task(config).execute(Task.Inputs(copy.deepcopy(model), dataset, fake_transform))
        model1 = outputs.model

        torch.manual_seed(0)
        config = Task.Config(batch_size=4, sub_batch_size=4, num_epochs=1, base_lr=1)
        outputs = Task(config).execute(Task.Inputs(copy.deepcopy(model), dataset, fake_transform))
        model2 = outputs.model

        torch.manual_seed(0)
        config = Task.Config(batch_size=4, sub_batch_size=4, num_epochs=3, base_lr=1)
        outputs = Task(config).execute(Task.Inputs(copy.deepcopy(model), dataset, fake_transform))
        model3 = outputs.model

        # All three models are exactly same.
        parameters0 = list(model0.parameters())
        parameters1 = list(model1.parameters())
        parameters2 = list(model2.parameters())
        parameters3 = list(model3.parameters())
        for i in range(len(parameters0)):
            self.assertTrue(torch.allclose(parameters0[i], parameters1[i], atol=0.001))
            self.assertTrue(torch.allclose(parameters0[i], parameters2[i], atol=0.001))
            self.assertFalse(torch.allclose(parameters0[i], parameters3[i], atol=0.001))  # Make sure the allclose() is not too loose.
