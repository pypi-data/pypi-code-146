from unittest import TestCase
from tempfile import TemporaryDirectory
from pathlib import Path
from unittest import mock
from io import StringIO
from datetime import date as Date
import unittest

from busy.commander import Commander
from busy.file_system_root import FilesystemRoot
from busy.ui.shell_ui import ShellUI

class TestCommandFinish(TestCase):

    def test_finish(self):
        with TemporaryDirectory() as t:
            p = Path(t, 'tasks.txt')
            p.write_text('a\n')
            c = Commander(FilesystemRoot(t))
            with mock.patch('busy.dateparser.today', lambda : Date(2019,2,11)):
                c.handle('finish','--yes')
                o = Path(t, 'done.txt').read_text()
                self.assertEqual(o, '2019-02-11|a\n')

    def test_confirmation(self):
        with TemporaryDirectory() as t:
            p = Path(t, 'tasks.txt')
            p.write_text('a\n')
            c = Commander(FilesystemRoot(t))
            u = ShellUI(c)
            c.setUI(u)
            o = StringIO()
            with mock.patch('busy.dateparser.today', lambda : Date(2019,2,11)):
                with mock.patch('sys.stdin', StringIO('Y')):
                    with mock.patch('sys.stdout', o):
                        c.handle('finish')
                        o = Path(t, 'done.txt').read_text()
                        self.assertEqual(o, '2019-02-11|a\n')

    def test_followon(self):
        with TemporaryDirectory() as t:
            p = Path(t, 'tasks.txt')
            p.write_text('a>b\n')
            c = Commander(FilesystemRoot(t))
            c.handle('finish','--yes')
            o = p.read_text()
            self.assertEqual(o, 'b\n')

    def test_followon_records_only_first_task_as_done(self):
        with TemporaryDirectory() as t:
            p = Path(t, 'tasks.txt')
            p.write_text('a>b\n')
            c = Commander(FilesystemRoot(t))
            with mock.patch('busy.dateparser.today', lambda : Date(2019,2,11)):
                c.handle('finish','--yes')
                o = Path(t, 'done.txt').read_text()
                self.assertEqual(o, '2019-02-11|a\n')

    def test_followon_with_alt_chars(self):
        with TemporaryDirectory() as t:
            p = Path(t, 'tasks.txt')
            p.write_text('a  --> b\n')
            c = Commander(FilesystemRoot(t))
            with mock.patch('busy.dateparser.today', lambda : Date(2019,2,11)):
                c.handle('finish','--yes')
                o = p.read_text()
                self.assertEqual(o, 'b\n')
                o2 = Path(t, 'done.txt').read_text()
                self.assertEqual(o2, '2019-02-11|a\n')

    def test_repeat(self):
        with TemporaryDirectory() as t:
            p = Path(t, 'tasks.txt')
            p.write_text('a>repeat in 2 days\n')
            c = Commander(FilesystemRoot(t))
            with mock.patch('busy.dateparser.today', lambda : Date(2019,2,11)):
                c.handle('finish','--yes')
                o = p.read_text()
                self.assertEqual(o, '')
                o2 = Path(t, 'plans.txt').read_text()
                self.assertEqual(o2, '2019-02-13|a>repeat in 2 days\n')
                o3 = Path(t, 'done.txt').read_text()
                self.assertEqual(o3, '2019-02-11|a\n')

    def test_repeat_parse_fail(self):
        with TemporaryDirectory() as t:
            p = Path(t, 'tasks.txt')
            p.write_text('a>repeat in x\n')
            c = Commander(FilesystemRoot(t))
            with mock.patch('busy.dateparser.today', lambda : Date(2019,2,11)):
                with self.assertRaises(RuntimeError):
                    c.handle('finish','--yes')

    def test_repeat_tomorrow(self):
        with TemporaryDirectory() as t:
            p = Path(t, 'tasks.txt')
            p.write_text('a>repeat tomorrow\n')
            c = Commander(FilesystemRoot(t))
            with mock.patch('busy.dateparser.today', lambda : Date(2019,2,11)):
                c.handle('finish','--yes')
                o = p.read_text()
                self.assertEqual(o, '')
                o2 = Path(t, 'plans.txt').read_text()
                self.assertEqual(o2, '2019-02-12|a>repeat tomorrow\n')
                o3 = Path(t, 'done.txt').read_text()
                self.assertEqual(o3, '2019-02-11|a\n')

    def test_repeat_day_template(self):
        with TemporaryDirectory() as t:
            p = Path(t, 'tasks.txt')
            p.write_text('a>repeat on 16\n')
            c = Commander(FilesystemRoot(t))
            with mock.patch('busy.dateparser.today', lambda : Date(2019,2,11)):
                c.handle('finish','--yes')
                o = p.read_text()
                self.assertEqual(o, '')
                o2 = Path(t, 'plans.txt').read_text()
                self.assertEqual(o2, '2019-02-16|a>repeat on 16\n')

    def test_repeat_day_template_next_month(self):
        with TemporaryDirectory() as t:
            p = Path(t, 'tasks.txt')
            p.write_text('a>repeat on 4\n')
            c = Commander(FilesystemRoot(t))
            with mock.patch('busy.dateparser.today', lambda : Date(2019,2,11)):
                c.handle('finish','--yes')
                o = p.read_text()
                self.assertEqual(o, '')
                o2 = Path(t, 'plans.txt').read_text()
                self.assertEqual(o2, '2019-03-04|a>repeat on 4\n')

    def test_repeat_day_template_next_year(self):
        with TemporaryDirectory() as t:
            p = Path(t, 'tasks.txt')
            p.write_text('a>repeat on 4\n')
            c = Commander(FilesystemRoot(t))
            with mock.patch('busy.dateparser.today', lambda : Date(2019,12,11)):
                c.handle('finish','--yes')
                o = p.read_text()
                self.assertEqual(o, '')
                o2 = Path(t, 'plans.txt').read_text()
                self.assertEqual(o2, '2020-01-04|a>repeat on 4\n')

    def test_repeat_month_day_template(self):
        with TemporaryDirectory() as t:
            p = Path(t, 'tasks.txt')
            p.write_text('a>repeat on 7-16\n')
            c = Commander(FilesystemRoot(t))
            with mock.patch('busy.dateparser.today', lambda : Date(2019,2,11)):
                c.handle('finish','--yes')
                o = p.read_text()
                self.assertEqual(o, '')
                o2 = Path(t, 'plans.txt').read_text()
                self.assertEqual(o2, '2019-07-16|a>repeat on 7-16\n')

    def test_repeat_month_day_next_year(self):
        with TemporaryDirectory() as t:
            p = Path(t, 'tasks.txt')
            p.write_text('a>repeat on 7-16\n')
            c = Commander(FilesystemRoot(t))
            with mock.patch('busy.dateparser.today', lambda : Date(2019,9,11)):
                c.handle('finish','--yes')
                o = p.read_text()
                self.assertEqual(o, '')
                o2 = Path(t, 'plans.txt').read_text()
                self.assertEqual(o2, '2020-07-16|a>repeat on 7-16\n')

    def test_finish_caps(self):
        with TemporaryDirectory() as t:
            p = Path(t, 'tasks.txt')
            p.write_text('a>Repeat ON 7-16\n')
            c = Commander(FilesystemRoot(t))
            with mock.patch('busy.dateparser.today', lambda : Date(2019,9,11)):
                c.handle('finish','--yes')
                o = p.read_text()
                self.assertEqual(o, '')
                o2 = Path(t, 'plans.txt').read_text()
                self.assertEqual(o2, '2020-07-16|a>Repeat ON 7-16\n')
