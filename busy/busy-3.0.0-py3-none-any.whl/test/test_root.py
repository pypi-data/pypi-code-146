from unittest import TestCase
from tempfile import TemporaryDirectory
from pathlib import Path
from unittest import mock
from unittest.mock import MagicMock

from busy.queues.todo_queue import TodoQueue
from busy.file_system_root import FilesystemRoot
from busy.file import File


class TestFilesystemRoot(TestCase):

    def test_root(self):
        with TemporaryDirectory() as d:
            sd = FilesystemRoot(Path(d))
            s = sd.get_queue('tasks')
            self.assertIsInstance(s, TodoQueue)

    def test_add_todo(self):
        with TemporaryDirectory() as td:
            sd1 = FilesystemRoot(Path(td))
            sd1.get_queue('x').add('a')
            sd1.save()
            sd2 = FilesystemRoot(Path(td))
            self.assertEqual(str(sd2.get_queue('x').get()), 'a')

    def test_make_dir_pater(self):
        with TemporaryDirectory() as td:
            r = FilesystemRoot(Path(td))
            r.get_queue('y').add('a')
            r.save()
            r2 = FilesystemRoot(Path(td))
            self.assertEqual(str(r2.get_queue('y').get()), 'a')

    def test_env_var_as_backup(self):
        with TemporaryDirectory() as td:
            with mock.patch.dict('os.environ', {'BUSY_ROOT': td}):
                sd1 = FilesystemRoot()
                sd1.get_queue('p').add('a')
                sd1.save()
                f = Path(td) / 'p.txt'
                self.assertEqual(f.read_text(), 'a\n')

    def test_user_root(self):
        with TemporaryDirectory() as td:
            with mock.patch.dict('os.environ', clear=True):
                with mock.patch('pathlib.Path.home', lambda: Path(td)):
                    sd1 = FilesystemRoot()
                    sd1.get_queue('w').add('a')
                    sd1.save()
                    f = Path(td) / '.busy' / 'w.txt'
                    self.assertEqual(f.read_text(), 'a\n')

    def test_list_queues(self):
        with TemporaryDirectory() as td:
            r = FilesystemRoot(Path(td))
            q1 = r.get_queue('a')
            q1.add('a')
            q2 = r.get_queue('b')
            q2.add('b')
            r.save()
            r2 = FilesystemRoot(Path(td))
            self.assertEqual(len(r2.queue_names), 2)
