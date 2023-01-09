import pathlib
import tempfile
import unittest
import PIL.Image
import torch.utils.data
from irisml.tasks.make_cached_dataset import Task


class FakeDataset(torch.utils.data.Dataset):
    def __init__(self, data):
        self._data = data

    def __len__(self):
        return len(self._data)

    def __getitem__(self, index):
        return self._data[index]


class TestMakeCachedDataset(unittest.TestCase):
    def test_classification_multiclass(self):
        dataset = FakeDataset([(PIL.Image.new('RGB', (32, 32)), torch.tensor(1)), (PIL.Image.new('RGB', (32, 32)), torch.tensor(2))])
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_dir = pathlib.Path(temp_dir)
            outputs = Task(Task.Config(temp_dir)).execute(Task.Inputs(dataset))

            for original, cached in zip(dataset, outputs.dataset):
                self.assertEqual(original, cached)
