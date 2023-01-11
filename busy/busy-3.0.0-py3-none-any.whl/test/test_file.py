from unittest import TestCase
from pathlib import Path
from tempfile import TemporaryDirectory

from busy.queues.todo_queue import TodoQueue
from busy.queues.todo_queue import PlanQueue
from busy.busyqueue import BusyQueue
from busy.plugins.todo.task import Task
from busy.file import File
from busy.item import Item

class TestFile(TestCase):

    def test_load_items(self):
        with TemporaryDirectory() as d:
            p = Path(d) / 'x.txt'
            p.write_text('a\nb\n')
            f = File(p)
            q = f.read()
            self.assertIsInstance(q[0], Item)
            self.assertEqual(q[0].description, 'a')

    def test_load_if_not_there(self):
        with TemporaryDirectory() as d:
            f = File(Path(d) / 'y.txt')
            q = f.read()
            self.assertIsInstance(q, list)
            self.assertEqual(len(q), 0)

    def test_save_items(self):
        with TemporaryDirectory() as d:
            p = Path(d) / 'z.txt'
            f1 = File(p)
            i = Item('a')
            f1.save(i)
            f2 = File(p)
            self.assertEqual(str(f2.read()[0]), 'a')

    # def test_plan_file_format(self):
    #     with TemporaryDirectory() as d:
    #         p = Path(d) / 'plans.txt'
    #         p.write_text('2018-12-01|a\n2018-12-09|b')
    #         q = File(p, PlanQueue).queue
    #         self.assertEqual(q.get().date.month, 12)
