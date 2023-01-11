from unittest import TestCase
from tempfile import TemporaryDirectory
from pathlib import Path
from unittest import mock
from io import StringIO
from datetime import date as Date

from busy.plugins.todo.task import Task
from busy.commander import Commander
from busy.file_system_root import FilesystemRoot
from busy.__main__ import main


class TestCommander(TestCase):

    def test_with_root_param(self):
        with TemporaryDirectory() as t:
            c = Commander(FilesystemRoot(t))
            o = c.handle('add', '--task', 'a')
            x = Path(t, 'tasks.txt').read_text()
            self.assertEqual(x, 'a\n')
