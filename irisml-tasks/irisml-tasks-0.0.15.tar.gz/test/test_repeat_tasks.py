import dataclasses
import sys
import unittest
import unittest.mock
import irisml.core
from irisml.tasks.repeat_tasks import Task


class FakeTask:
    class Task(irisml.core.TaskBase):
        @dataclasses.dataclass
        class Inputs:
            int_value: int

        @dataclasses.dataclass
        class Outputs:
            float_value: float

        def execute(self, inputs):
            return self.Outputs(float(inputs.int_value * 2))


class TestRepeatTasks(unittest.TestCase):
    def test_no_outputs(self):
        with unittest.mock.patch.dict(sys.modules, {'irisml.tasks.fake_task': FakeTask}):
            config = Task.Config(tasks=[irisml.core.TaskDescription.from_dict({'task': 'fake_task', 'inputs': {'int_value': '$env.REPEAT_TASKS_INDEX'}})],
                                 num_repeats=3)
            outputs = Task(config).execute(Task.Inputs())
            self.assertEqual(outputs.float_output_values, [[], [], []])

    def test_collect_outputs(self):
        with unittest.mock.patch.dict(sys.modules, {'irisml.tasks.fake_task': FakeTask}):
            config = Task.Config(tasks=[irisml.core.TaskDescription.from_dict({'task': 'fake_task', 'inputs': {'int_value': '$env.REPEAT_TASKS_INDEX'}})],
                                 num_repeats=3,
                                 float_output_names=['fake_task.float_value'])
            outputs = Task(config).execute(Task.Inputs())
            self.assertEqual(outputs.float_output_values, [[0.0], [2.0], [4.0]])
