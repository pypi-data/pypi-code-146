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

class TestAlternateQueue(TestCase):

    def test_get_from(self):
        with TemporaryDirectory() as t:
            p = Path(t, 'a.txt')
            p.write_text('b\n')
            c = Commander(FilesystemRoot(t))
            o = c.handle('get','--queue','a')
            self.assertEqual(o, 'b')

    def test_default_queue(self):
        with TemporaryDirectory() as t:
            p = Path(t, 'tasks.txt')
            p.write_text('b\n')
            c = Commander(FilesystemRoot(t))
            o = c.handle('get')
            self.assertEqual(o, 'b')

    def test_add(self):
        with TemporaryDirectory() as t:
            c = Commander(FilesystemRoot(t))
            with mock.patch('sys.stdin', StringIO('g')):
                c.handle('add','--queue','j')
                x = Path(t, 'j.txt').read_text()
                self.assertEqual(x, 'g\n')

    def test_drop(self):
        with TemporaryDirectory() as t:
            p = Path(t, 'u.txt')
            p.write_text('a\nb\nc\nd')
            c = Commander(FilesystemRoot(t))
            c.handle('drop','2','4','--queue','u')
            o = p.read_text()
            self.assertEqual(o, 'a\nc\nb\nd\n')

    def test_delete(self):
        with TemporaryDirectory() as t:
            p = Path(t, 'w.txt')
            p.write_text('a\nb\nc\nd')
            c = Commander(FilesystemRoot(t))
            c.handle('delete','--yes','3-', '--queue', 'w')
            o = p.read_text()
            self.assertEqual(o, 'a\nb\n')

    def test_manage(self):
        with TemporaryDirectory() as t:
            p = Path(t, 'y.txt')
            p.write_text('a\n')
            with mock.patch('busy.editor', lambda x: 'b\n'):
                c = Commander(FilesystemRoot(t))
                c.handle('manage', '--queue', 'y')
                f = p.read_text()
                self.assertEqual(f, 'b\n')
