import pathlib
import unittest
from irisml.tasks.join_filepath import Task


class TestJoinFilepath(unittest.TestCase):
    def test_simple(self):
        config = Task.Config(pathlib.Path('parent_dir'), 'my_file.txt')
        outputs = Task(config).execute(Task.Inputs())
        self.assertEqual(outputs.path, pathlib.Path('parent_dir/my_file.txt'))

    def test_abs_path(self):
        config = Task.Config(pathlib.Path('/parent_dir'), 'my_file.txt')
        outputs = Task(config).execute(Task.Inputs())
        self.assertEqual(outputs.path, pathlib.Path('/parent_dir/my_file.txt'))
