import contextlib
import io
import unittest
from irisml.tasks.print_environment_info import Task


class TestPrintEnvironmentInfo(unittest.TestCase):
    def test_print_something(self):
        with contextlib.redirect_stdout(io.StringIO()) as f:
            Task(Task.Config()).execute(Task.Inputs())
        s = f.getvalue()
        self.assertGreater(len(s), 0)
