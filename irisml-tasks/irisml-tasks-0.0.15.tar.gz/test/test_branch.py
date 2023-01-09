import contextlib
import io
import sys
import unittest
import unittest.mock
import irisml.core
from irisml.tasks.branch import Task


class TestBranch(unittest.TestCase):
    def test_single_task(self):
        class FakeTask(irisml.core.TaskBase):
            def execute(self, inputs):
                print("fake_task is called.")
                return self.Outputs()

        class FakeTask2(irisml.core.TaskBase):
            def execute(self, inputs):
                print("fake_task2 is called.")
                return self.Outputs()

        with unittest.mock.patch.dict(sys.modules, {'irisml.tasks.fake_task': unittest.mock.MagicMock(Task=FakeTask),
                                                    'irisml.tasks.fake_task2': unittest.mock.MagicMock(Task=FakeTask2)}):
            with contextlib.redirect_stdout(io.StringIO()) as f:
                Task(Task.Config(True, [irisml.core.TaskDescription.from_dict({'task': 'fake_task'})])).execute(Task.Inputs())
            self.assertEqual(f.getvalue().strip(), 'fake_task is called.')

            with contextlib.redirect_stdout(io.StringIO()) as f:
                Task(Task.Config(True,
                                 [irisml.core.TaskDescription.from_dict({'task': 'fake_task'})],
                                 [irisml.core.TaskDescription.from_dict({'task': 'fake_task2'})])).execute(Task.Inputs())
            self.assertEqual(f.getvalue().strip(), 'fake_task is called.')

            with contextlib.redirect_stdout(io.StringIO()) as f:
                Task(Task.Config(False,
                                 [irisml.core.TaskDescription.from_dict({'task': 'fake_task'})],
                                 [irisml.core.TaskDescription.from_dict({'task': 'fake_task2'})])).execute(Task.Inputs())
            self.assertEqual(f.getvalue().strip(), 'fake_task2 is called.')

    def test_dry_run(self):
        class FakeTask(irisml.core.TaskBase):
            def execute(self, inputs):
                raise RuntimeError()  # This method must not be called in dry_run.

        with unittest.mock.patch.dict(sys.modules, {'irisml.tasks.fake_task': unittest.mock.MagicMock(Task=FakeTask)}):
            outputs = Task(Task.Config(True, [irisml.core.TaskDescription.from_dict({'task': 'fake_task'})])).dry_run(Task.Inputs())
            self.assertIsNotNone(outputs)
