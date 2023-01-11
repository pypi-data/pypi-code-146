from unittest import TestCase
from unittest.mock import MagicMock

from busy.commander import Commander
from busy.file_system_root import FilesystemRoot

import unittest
@unittest.skip("Skipping")
class TestOneQueueAtATime(TestCase):

    def test_dont_read_plans_when_reading_tasks(self):
        m = FilesystemRoot()
        m.get_queue = MagicMock()
        c = Commander(m)
        c.handle('list')
        try:
            m.get_queue.assert_called_once_with('tasks')
        except:
            self.fail()

    def test_dont_read_tasks_when_reading_plans(self):
        m = FilesystemRoot()
        m.get_queue = MagicMock()
        c = Commander(m)
        c.handle('list','--queue','plans')
        try:
            m.get_queue.assert_called_once_with('plans')
        except:
            self.fail()

    def test_dont_read_plans_when_pop(self):
        m = FilesystemRoot()
        m.get_queue = MagicMock()
        c = Commander(m)
        c.handle('pop')
        try:
            m.get_queue.assert_called_once_with('tasks')
        except:
            self.fail()

    def test_save_not_called_if_not_needed(self):    
        m = FilesystemRoot()
        m._save = MagicMock()
        c = Commander(m)
        c.handle('get')
        m._save.assert_not_called()

