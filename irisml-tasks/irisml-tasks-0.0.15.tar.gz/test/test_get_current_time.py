import time
import unittest
from irisml.tasks.get_current_time import Task


class TestGetCurrentTime(unittest.TestCase):
    def test_simple(self):
        outputs = Task(Task.Config()).execute(Task.Inputs())
        current_time = time.time()
        self.assertLessEqual(outputs.time, current_time)
