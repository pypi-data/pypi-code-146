#!/usr/bin/env python

from threading import Thread 
from abc import abstractmethod
import signal
import atexit
import sys,traceback
from codefast import logger
import threading


class BaseThread(Thread):
    def __init__(self, name=None, daemon=True):
        super().__init__(name=name, daemon=daemon)
        self._stop_event = threading.Event()

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()

    def process(self):
        raise NotImplementedError

    def __repr__(self):
        return f'{self.__class__.__name__}({self.name})'

    def __str__(self):
        return self.__repr__()

    def run(self):
        while not self.stopped():
            try:
                self.process()
            except Exception as e:
                self.stop()
                logger.warning(e)
                
class IOWorker(Thread):
    def __init__(self):
        super().__init__()
        self._terminate = False

    def run(self):
        while not self._terminate:
            self.process()

    @abstractmethod
    def process(self):
        pass

    def prepare_join(self):
        print('{} received terminate signal'.format(self.__class__.__name__))
        self._terminate = True
        

class ThreadPivot(object):
    def __init__(self):
        self.workers = []

    def exit_safely(self, signum, frame):
        print('safe exit handler: %s' % signum)
        for worker in self.workers:
            worker.prepare_join()

        for worker in self.workers:
            worker.join()

    def add_worker(self, worker_class: IOWorker, number: int):
        for _ in range(number):
            print('add worker: %s' % worker_class.__name__)
            self.workers.append(worker_class())
        return self

    def run(self):
        @atexit.register
        def _atexit():
            exc_type, exc_value, exc_tb = sys.exc_info()
            s = traceback.format_exception(exc_type, exc_value, exc_tb)
            print(__name__ + ' exit: ' + str(s))

        signal.signal(signal.SIGTERM, self.exit_safely)
        signal.signal(signal.SIGINT, self.exit_safely)
        signal.signal(signal.SIGHUP, self.exit_safely)

        for worker in self.workers:
            print('worker {} started'.format(worker.getName()))
            worker.start()


class DummyThread(IOWorker):
    def __init__(self):
        super().__init__()

    def process(self):
        import time, random
        print('{} processing'.format(self.getName()))
        time.sleep(random.randint(1,5))

if __name__ == "__main__":
    ThreadPivot().add_worker(DummyThread, 10).run()
