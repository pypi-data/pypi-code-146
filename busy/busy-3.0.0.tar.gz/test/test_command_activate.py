from unittest import TestCase
from tempfile import TemporaryDirectory
from pathlib import Path
from unittest import mock
from io import StringIO
from datetime import date as Date
import unittest

from busy.plugins.todo.task import Task
from busy.commander import Commander
from busy.file_system_root import FilesystemRoot

class TestCommandActivate(TestCase):

    def test_activate(self):
        with TemporaryDirectory() as t:
            p = Path(t, 'plans.txt')
            p.write_text('2018-09-04|a\n')
            c = Commander(FilesystemRoot(t))
            c.handle('activate','1')
            self.assertEqual(p.read_text(), '')
            p2 = Path(t, 'tasks.txt')
            self.assertEqual(p2.read_text(), 'a\n')

    def test_activate_with_today_option(self):
        with TemporaryDirectory() as t:
            p = Path(t, 'plans.txt')
            p.write_text('2018-09-04|a\n2019-03-25|b\n')
            p2 = Path(t, 'tasks.txt')
            p2.write_text('')
            c = Commander(FilesystemRoot(t))
            with mock.patch('busy.dateparser.today', lambda : Date(2019,2,11)):
                c.handle('activate','--today')
                self.assertEqual(p.read_text(), '2019-03-25|b\n')
                p2 = Path(t, 'tasks.txt')
                self.assertEqual(p2.read_text(), 'a\n')

    def test_pop(self):
        with TemporaryDirectory() as t:
            p1 = Path(t, 'tasks.txt')
            p1.write_text('x\n')
            p2 = Path(t, 'plans.txt')
            p2.write_text('2018-09-04|a\n')
            c = Commander(FilesystemRoot(t))
            c.handle('activate','1')
            self.assertEqual(p1.read_text(), 'a\nx\n')

    def test_activate_no_args_does_nothing(self):
        with TemporaryDirectory() as t:
            p = Path(t, 'plans.txt')
            p.write_text('2018-09-04|a\n')
            c = Commander(FilesystemRoot(t))
            c.handle('activate')
            self.assertEqual(p.read_text(), '2018-09-04|a\n')
            p2 = Path(t, 'tasks.txt')
            self.assertFalse(p2.exists())
