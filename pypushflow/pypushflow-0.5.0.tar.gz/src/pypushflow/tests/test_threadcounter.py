import unittest
from time import sleep
from pypushflow.ThreadCounter import ThreadCounter
from concurrent.futures import ThreadPoolExecutor


class TestThreadCounter(unittest.TestCase):
    def setUp(self):
        self.counter = ThreadCounter()

    def mythread(self, sleep_time):
        with self.counter:
            sleep(1)
        return True

    def test_thread_count(self):
        self.assertEqual(self.counter.nthreads, 0)
        with self.counter as ctr:
            self.assertEqual(ctr.nthreads, 1)
            with self.counter as ctr:
                self.assertEqual(ctr.nthreads, 2)
            self.assertEqual(ctr.nthreads, 1)
        self.assertEqual(self.counter.nthreads, 0)

    def test_multiple_threads(self):
        with ThreadPoolExecutor(max_workers=10) as executor:
            results = executor.map(self.mythread, [1] * 10)
            self.counter.wait_threads_finished()
            for result in results:
                self.assertTrue(result)
