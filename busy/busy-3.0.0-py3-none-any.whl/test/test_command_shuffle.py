from unittest import TestCase
from tempfile import TemporaryDirectory
from pathlib import Path
from io import StringIO
from datetime import date as Date
import unittest
import random

from busy.plugins.todo.task import Task
from busy.commander import Commander
from busy.file_system_root import FilesystemRoot


class TestCommandShuffle(TestCase):

    def test_shuffle(self):
        with TemporaryDirectory() as t:
            p = Path(t, 'tasks.txt')
            p.write_text('a\nb\nc\n')
            random.seed(1)
            c = Commander(FilesystemRoot(t))
            c.handle('shuffle')
            f = p.read_text()
            self.assertEqual(f, 'b\nc\na\n')

