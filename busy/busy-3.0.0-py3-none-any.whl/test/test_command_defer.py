from unittest import TestCase
from tempfile import TemporaryDirectory
from pathlib import Path
from unittest import mock
from io import StringIO
from datetime import date as Date

from busy.plugins.todo.task import Task
from busy.commander import Commander
from busy.file_system_root import FilesystemRoot

class TestCommandDefer(TestCase):

    def test_defer(self):
        with TemporaryDirectory() as t:
            p = Path(t, 'tasks.txt')
            p.write_text('a\nb\nc\nd')
            c = Commander(FilesystemRoot(t))
            c.handle('defer','2','--to','2019-09-06')
            o = p.read_text()
            self.assertEqual(o, 'a\nc\nd\n')
            o2 = Path(t, 'plans.txt').read_text()
            self.assertEqual(o2, '2019-09-06|b\n')

    def test_defer_for(self):
        with TemporaryDirectory() as t:
            p = Path(t, 'tasks.txt')
            p.write_text('a\nb\nc\nd')
            c = Commander(FilesystemRoot(t))
            c.handle('defer','2','--for','2019-09-06')
            o = p.read_text()
            self.assertEqual(o, 'a\nc\nd\n')
            o2 = Path(t, 'plans.txt').read_text()
            self.assertEqual(o2, '2019-09-06|b\n')

    def test_defer_days(self):
        with TemporaryDirectory() as t:
            p = Path(t, 'tasks.txt')
            p.write_text('a\nb\nc\nd')
            with mock.patch('busy.dateparser.today', lambda : Date(2019,2,11)):
                c = Commander(FilesystemRoot(t))
                c.handle('defer','2','--for','1 day')
                o = p.read_text()
                self.assertEqual(o, 'a\nc\nd\n')
                o2 = Path(t, 'plans.txt').read_text()
                self.assertEqual(o2, '2019-02-12|b\n')

    def test_defer_d(self):
        with TemporaryDirectory() as t:
            p = Path(t, 'tasks.txt')
            p.write_text('a\nb\nc\nd')
            with mock.patch('busy.dateparser.today', lambda : Date(2019,2,11)):
                c = Commander(FilesystemRoot(t))
                c.handle('defer','2','--for','5d')
                o = p.read_text()
                self.assertEqual(o, 'a\nc\nd\n')
                o2 = Path(t, 'plans.txt').read_text()
                self.assertEqual(o2, '2019-02-16|b\n')

    def test_defer_with_input(self):
        with TemporaryDirectory() as t:
            p = Path(t, 'tasks.txt')
            p.write_text('a\nb\n')
            c = Commander(FilesystemRoot(t))
            with mock.patch('sys.stdin', StringIO('2019-08-24')):
                c.handle('defer')
                o = p.read_text()
                self.assertEqual(o, 'b\n')
                o2 = Path(t, 'plans.txt').read_text()
                self.assertEqual(o2, '2019-08-24|a\n')

    def test_default_tomorrow(self):
        with TemporaryDirectory() as t:
            p = Path(t, 'tasks.txt')
            p.write_text('a\nb\n')
            c = Commander(FilesystemRoot(t))
            with mock.patch('busy.dateparser.today', lambda : Date(2019,2,11)):
                with mock.patch('sys.stdin', StringIO(' ')):
                    c.handle('defer')
                    o2 = Path(t, 'plans.txt').read_text()
                    self.assertEqual(o2, '2019-02-12|a\n')

    def test_tuesday(self):
        with TemporaryDirectory() as t:
            p = Path(t, 'tasks.txt')
            p.write_text('a\nb\n')
            c = Commander(FilesystemRoot(t))
            with mock.patch('busy.dateparser.today', lambda : Date(2019,2,14)):
                c.handle('defer','--to','tue')
                o2 = Path(t, 'plans.txt').read_text()
                self.assertEqual(o2, '2019-02-19|a\n')

    def test_thursday(self):
        with TemporaryDirectory() as t:
            p = Path(t, 'tasks.txt')
            p.write_text('a\nb\n')
            c = Commander(FilesystemRoot(t))
            with mock.patch('busy.dateparser.today', lambda : Date(2019,2,14)):
                c.handle('defer','--to','thursday')
                o2 = Path(t, 'plans.txt').read_text()
                self.assertEqual(o2, '2019-02-21|a\n')

    def test_capital_days(self):
        with TemporaryDirectory() as t:
            p = Path(t, 'tasks.txt')
            p.write_text('a\nb\n')
            c = Commander(FilesystemRoot(t))
            with mock.patch('busy.dateparser.today', lambda : Date(2019,2,14)):
                c.handle('defer','--to','THURS')
                o2 = Path(t, 'plans.txt').read_text()
                self.assertEqual(o2, '2019-02-21|a\n')

    def test_slashes(self):
        with TemporaryDirectory() as t:
            p = Path(t, 'tasks.txt')
            p.write_text('a')
            c = Commander(FilesystemRoot(t))
            c.handle('defer','--to','2019/09/06')
            o2 = Path(t, 'plans.txt').read_text()
            self.assertEqual(o2, '2019-09-06|a\n')
