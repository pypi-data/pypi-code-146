import pathlib
import tempfile
import unittest

import torch
from irisml.tasks.save_state_dict import Task


class TestLoadStateDict(unittest.TestCase):
    def test_simple(self):
        fake_model = torch.nn.Conv2d(3, 3, 3)

        inputs = Task.Inputs(model=fake_model)
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_file = pathlib.Path(temp_dir) / 'test.pth'

            Task(Task.Config(path=temp_file)).execute(inputs)
            self.assertTrue(self._is_equal_state_dict(fake_model.state_dict(), torch.load(temp_file)))

    def test_fp16(self):
        fake_model = torch.nn.Conv2d(3, 3, 3)

        inputs = Task.Inputs(model=fake_model)
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_file = pathlib.Path(temp_dir) / 'test.pth'

            Task(Task.Config(path=temp_file, fp16=True)).execute(inputs)
            saved = torch.load(temp_file)
            self.assertEqual(saved['weight'].dtype, torch.float16)
            self.assertEqual(saved['bias'].dtype, torch.float16)

    def test_no_parent_directory(self):
        fake_model = torch.nn.Conv2d(3, 3, 3)

        inputs = Task.Inputs(model=fake_model)
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_file = pathlib.Path(temp_dir) / 'new_directory' / 'another_new_directory' / 'test.pth'

            self.assertFalse(temp_file.exists())
            Task(Task.Config(path=temp_file)).execute(inputs)
            self.assertTrue(temp_file.exists())

    def _is_equal_state_dict(self, state_dict1, state_dict2):
        if set(state_dict1) != set(state_dict2):
            return False

        for key in state_dict1:
            if not torch.equal(state_dict1[key], state_dict2[key]):
                return False
        return True
