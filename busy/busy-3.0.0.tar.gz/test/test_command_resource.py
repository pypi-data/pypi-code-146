from unittest import TestCase
from tempfile import TemporaryDirectory
from pathlib import Path
from unittest import mock
from io import StringIO
from datetime import date as Date

from busy.plugins.todo.task import Task
from busy.commander import Commander
from busy.file_system_root import FilesystemRoot


class TestCommandResource(TestCase):

    def test_resource(self):
        with TemporaryDirectory() as t:
            p = Path(t, 'tasks.txt')
            p.write_text('a at g\n')
            c = Commander(FilesystemRoot(t))
            o = c.handle('resource')
            self.assertEqual(o, 'g')

    def test_get_without_resource(self):
        with TemporaryDirectory() as t:
            p = Path(t, 'tasks.txt')
            p.write_text('a at g\n')
            c = Commander(FilesystemRoot(t))
            o = c.handle('get-without-resource')
            self.assertEqual(o, 'a')
