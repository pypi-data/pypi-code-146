from unittest import TestCase
from tempfile import TemporaryDirectory
from pathlib import Path
from unittest import mock
from io import StringIO
from datetime import date as Date

from busy.commander import Commander
from busy.file_system_root import FilesystemRoot


class TestCommandQueues(TestCase):

    def test_queues(self):
        with TemporaryDirectory() as t:
            p = Path(t, 'a.txt')
            p.write_text('a')
            p2 = Path(t, 'b.txt')
            p2.write_text('b')
            c = Commander(FilesystemRoot(t))
            o = c.handle('queues')
            self.assertEqual(o, 'a\nb')
