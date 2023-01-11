from unittest import TestCase
from tempfile import TemporaryDirectory
from pathlib import Path
from unittest import mock
from io import StringIO
from datetime import date as Date

from busy.commander import Commander
from busy.file_system_root import FilesystemRoot


class TestCommandTags(TestCase):

    def test_tags(self):
        with TemporaryDirectory() as t:
            p = Path(t, 'tasks.txt')
            p.write_text('a #b\nc #d\ne #b\n')
            c = Commander(FilesystemRoot(t))
            o = c.handle('tags')
            self.assertEqual(o, 'b\nd')
