from unittest import TestCase
import datetime

from busy.plugins.todo.task import Task
from busy.queues.todo_queue import TodoQueue

class TestTodoQueue(TestCase):

    def test_get(self):
        q = TodoQueue()
        q.add(Task('a'))
        t = q.get()
        self.assertEqual(str(t),'a')

    def test_list(self):
        s = TodoQueue()
        s.add(Task('a'))
        s.add(Task('b'))
        i = s.list()
        self.assertEqual(len(i), 2)
        self.assertEqual(i[1][0], 2)
        self.assertEqual(str(i[0][1]), 'a')
        self.assertIsInstance(i[1][1], Task)

    def test_defer(self):
        s = TodoQueue()
        s.add(Task('a'))
        d = datetime.date(2018,12,25)
        s.defer(d)
        self.assertEqual(s.plans.count(), 1)
        self.assertEqual(s.plans.get(1).date.year, 2018)

    def test_pop(self):
        s = TodoQueue()
        t1 = Task('a')
        t2 = Task('b')
        s.add(t1)
        s.add(t2)
        s.pop()
        i = s.list()
        self.assertEqual(len(i), 2)
        self.assertEqual(str(i[0][1]), 'b')

    def test_by_number(self):
        s = TodoQueue()
        s.add(Task('a'))
        s.add(Task('b'))
        t = s.get(2)
        self.assertEqual(str(t), 'b')

    def test_create_with_string(self):
        s = TodoQueue()
        s.add('a')
        self.assertEqual(str(s.get()), 'a')
        self.assertIsInstance(s.get(), Task)

    def test_create_with_multiple_strings(self):
        s = TodoQueue()
        s.add('a','b','c')
        self.assertIsInstance(s.get(), Task)
        self.assertEqual(s.count(), 3)
        self.assertEqual(str(s.get(2)), 'b')

    def test_select_multiple(self):
        s = TodoQueue()
        s.add('a','b','c')
        t = s.select(1,3)
        self.assertEqual(len(t), 2)

    def test_list_plans(self):
        s = TodoQueue()
        s.add('a','b')
        s.defer((2018,12,4))
        self.assertEqual(s.plans.count(), 1)

    def test_defer_by_index(self):
        s = TodoQueue()
        s.add('a','b')
        s.defer((2018,12,4),2)
        t = s.get()
        self.assertEqual(s.plans.count(),1)
        self.assertEqual(str(t), 'a')

    def test_defer_multiple(self):
        s = TodoQueue()
        s.add('a','b','c')
        s.defer((2018,12,5),1,3)
        p = s.plans.get(2)
        self.assertEqual(str(p), 'c')

    def test_list_by_criteria(self):
        s = TodoQueue()
        s.add('a','b','c')
        i = s.list(2,3)
        self.assertEqual(len(i), 2)
        self.assertEqual(str(i[1][1]), 'c')

    def test_drop(self):
        s = TodoQueue()
        s.add('a','b','c')
        s.drop()
        self.assertEqual(str(s.get()), 'b')
        self.assertEqual(str(s.get(3)), 'a')

    def test_drop_by_criteria(self):
        s = TodoQueue()
        s.add('a','b','c','d')
        s.drop('2-3')
        self.assertEqual(str(s.get(1)), 'a')
        self.assertEqual(str(s.get(2)), 'd')
        self.assertEqual(str(s.get(3)), 'b')
        self.assertEqual(str(s.get(4)), 'c')

    def test_activate(self):
        s = TodoQueue()
        s.add('a','b')
        s.defer((2018,12,4),2)
        s.activate(1)
        t = s.get()
        self.assertEqual(str(t), 'b')

    def test_done_no_manager(self):
        s = TodoQueue()
        d = s.done
        self.assertIsNotNone(d)