from unittest import TestCase

from busy.busyqueue import BusyQueue

class TestQueueReplace(TestCase):

    def test_replace_one(self):
        a = BusyQueue()
        a.add('a','b','c')
        a.replace([1], ['d'])
        self.assertEqual(str(a.get(2)), 'd')

    def test_replace_multi(self):
        a = BusyQueue()
        a.add('a','b','c','d')
        a.replace([1,2], ['1','2'])
        self.assertEqual(a.strings, ['a','1','2','d'])

    def test_replace_extra_index(self):
        a = BusyQueue()
        a.add('a','b','c','d')
        a.replace([1,2], ['1'])
        self.assertEqual(a.strings, ['a','1','d'])
