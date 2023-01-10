import unittest
from time import sleep
from threading import Lock
from pypushflow.ThreadCountingActor import ThreadCountingActor
from pypushflow.ThreadCounter import ThreadCounter
from concurrent.futures import ThreadPoolExecutor


class Counter:
    def __init__(self):
        self.value = 0
        self._lock = Lock()

    def increment(self):
        with self._lock:
            self.value += 1


class MyThreadCountingActor(ThreadCountingActor):
    def __init__(self, thread_counter, downstream_actors=tuple()):
        super().__init__(thread_counter=thread_counter, name="MyThreadCountingActor")
        self.downstream_actors = downstream_actors

    def trigger(self, state):
        sleep(0.01)
        if not self.downstream_actors:
            state["ntasks"].increment()
        for actor in self.downstream_actors:
            actor.trigger(state)


class TestThreadCountingActor(unittest.TestCase):
    def setUp(self):
        self.thread_counter = ThreadCounter()

    def test_multiple_threads(self):
        workers1 = [MyThreadCountingActor(self.thread_counter) for _ in range(3)]
        workers2 = [
            MyThreadCountingActor(self.thread_counter, workers1) for _ in range(5)
        ]
        workers3 = [
            MyThreadCountingActor(self.thread_counter, workers2) for _ in range(10)
        ]
        state = {"ntasks": Counter()}
        with ThreadPoolExecutor(max_workers=10) as executor:
            executor.map(lambda w: w.trigger(state), workers3)
            self.thread_counter.wait_threads_finished()
            self.assertEqual(state["ntasks"].value, 150)
