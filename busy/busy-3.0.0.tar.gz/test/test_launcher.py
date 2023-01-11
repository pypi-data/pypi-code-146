from unittest import TestCase
from unittest import mock
from tempfile import TemporaryDirectory
import os

from busy.launcher import Launcher
from busy.file_system_root import FilesystemRoot


class TestLauncher(TestCase):

    def setUp(self):
        self.tempdir = TemporaryDirectory()
        os.environ['BUSY_ROOT'] = self.tempdir.name

    def tearDown(self):
        self.tempdir.cleanup()

    def test_commands(self):
        b = Launcher('a', 'b')
        self.assertEqual(b.commands, ['a', 'b'])

    def test_default_storage(self):
        b = Launcher('a', 'b')
        self.assertIsInstance(b.root, FilesystemRoot)

    def test_root_option(self):
        with TemporaryDirectory() as d:
            b = Launcher('--root', d)
            self.assertEqual(str(b.root._path), d)
