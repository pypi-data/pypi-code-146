from unittest import TestCase
from tempfile import TemporaryDirectory
from pathlib import Path
from unittest import mock
from io import StringIO
from datetime import date as Date

from busy.plugins.todo.task import Task
from busy.commander import Commander
from busy.file_system_root import FilesystemRoot

class TestCommandList(TestCase):

    def test_list(self):
        with TemporaryDirectory() as t:
            c = Commander(FilesystemRoot(t))
            c.handle('add','--task','a')
            o = c.handle('list')
            self.assertEqual(o, '     1  a')

    def test_list_plans(self):
        with TemporaryDirectory() as t:
            p = Path(t, 'plans.txt')
            p.write_text('2019-01-04|g\n2019-02-05|p')
            c = Commander(FilesystemRoot(t))
            o = c.handle('list','--queue','plans')
            self.assertEqual(o, '     1  2019-01-04  g\n     2  2019-02-05  p')

    def test_list_with_criteria(self):
        with TemporaryDirectory() as t:
            p = Path(t, 'tasks.txt')
            p.write_text('a\nb\nc\nd')
            c = Commander(FilesystemRoot(t))
            o = c.handle('list','2','4')
            self.assertEqual(o, '     2  b\n     4  d')
