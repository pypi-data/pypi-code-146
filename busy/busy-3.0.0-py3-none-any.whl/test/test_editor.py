from unittest import TestCase
import busy
from unittest import mock
from pathlib import Path

class MockSubprocess:

    @staticmethod
    def run(arg):
        Path(arg[-1]).write_text('v')

class MockShUtil:

    @staticmethod
    def which(arg):
        return False


class TestEditor(TestCase):

    def test_editor(self):
        with mock.patch('busy.subprocess', MockSubprocess):
            x = busy.editor('a')
            self.assertEqual(x, 'v')

    def test_no_command(self):
        with mock.patch('busy.shutil', MockShUtil):
            with self.assertRaises(RuntimeError):
                busy.editor('a')
