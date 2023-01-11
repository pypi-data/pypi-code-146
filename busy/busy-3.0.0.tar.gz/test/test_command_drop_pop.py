from unittest import TestCase
from tempfile import TemporaryDirectory
from pathlib import Path
from unittest import mock
from io import StringIO
from datetime import date as Date

from busy.plugins.todo.task import Task
from busy.commander import Commander
from busy.file_system_root import FilesystemRoot

class TestCommandDrop(TestCase):

    def test_drop(self):
        with TemporaryDirectory() as t:
            p = Path(t, 'tasks.txt')
            p.write_text('a\nb\nc\nd')
            c = Commander(FilesystemRoot(t))
            c.handle('drop','2','4')
            o = p.read_text()
            self.assertEqual(o, 'a\nc\nb\nd\n')

    def test_pop(self):
        with TemporaryDirectory() as t:
            p = Path(t, 'tasks.txt')
            p.write_text('a\nb\nc\nd')
            c = Commander(FilesystemRoot(t))
            c.handle('pop','2','4')
            o = p.read_text()
            self.assertEqual(o, 'b\nd\na\nc\n')

    def test_output(self):
        with TemporaryDirectory() as t:
            p = Path(t, 'tasks.txt')
            p.write_text('a\nb\n')
            c = Commander(FilesystemRoot(t))
            o = c.handle('drop','1')
            self.assertIsNone(o)
