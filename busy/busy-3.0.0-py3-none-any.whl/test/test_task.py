from unittest import TestCase
import datetime

from busy.plugins.todo.task import Task
from busy.plugins.todo.task import Plan

class TestTask(TestCase):

    def test_task(self):
        t = Task('b')
        self.assertIsInstance(t, Task)

    def test_description_as_string(self):
        t = Task('a')
        self.assertEqual(t.description, 'a')

    def test_task_requires_description(self):
        with self.assertRaises(AssertionError):
            t = Task('')

    def test_plan(self):
        t = Task('a')
        d = datetime.date(2018,12,1)
        t.as_plan(d)

    def test_plan_as_tuple(self):
        t = Task('b')
        p = t.as_plan((2018,12,1))
        self.assertEqual(p.date.month, 12)

    def test_plan_requires_date(self):
        t = Task('c')
        with self.assertRaises(RuntimeError):
            t.as_plan(54)

    def test_plan_with_date_as_string(self):
        t = Task('d')
        p = t.as_plan('2019-04-05')
        self.assertEqual(p.date.day, 5)

    def test_create_plan_with_dict(self):
        t = Plan(date=(2019, 4,15), description='a')
        self.assertEqual(t.date.month, 4)
 
    def test_tags(self):
        t = Task('f #a')
        self.assertEqual(t.tags, ['a'])

    def test_project(self):
        t = Task("k #oNe #two")
        self.assertEqual(t.project, 'one')

    def test_resource(self):
        t = Task("a at https://b.us #f")
        self.assertEqual(t.resource, "https://b.us")
    
    def test_resource_without_at(self):
        t = Task("e")
        self.assertEqual(t.resource, "")

    def test_without_resource(self):
        t = Task("a at https://b.us #f")
        self.assertEqual(t.without_resource, 'a #f')

    def test_without_resource_without_at(self):
        t = Task("f")
        self.assertEqual(t.without_resource, "f")
