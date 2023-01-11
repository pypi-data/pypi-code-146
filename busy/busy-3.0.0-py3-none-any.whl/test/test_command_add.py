from unittest import TestCase
from tempfile import TemporaryDirectory
from pathlib import Path
from unittest import mock
from io import StringIO
from datetime import date as Date

from busy.plugins.todo.task import Task
from busy.commander import Commander
from busy.file_system_root import FilesystemRoot

class TestCommandAdd(TestCase):

    def test_by_parameter(self):
        with TemporaryDirectory() as t:
            c = Commander(FilesystemRoot(t))
            c.handle('add','u p')
            x = Path(t, 'tasks.txt').read_text()
            self.assertEqual(x, 'u p\n')

    def test_add_by_input(self):
        with TemporaryDirectory() as t:
            c = Commander(FilesystemRoot(t))
            with mock.patch('sys.stdin', StringIO('g')):
                c.handle('add')
                x = Path(t, 'tasks.txt').read_text()
                self.assertEqual(x, 'g\n')
