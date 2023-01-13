from threading import Thread, Event
from queue import Queue, Empty


class NonBlockingCSVReader:

    def __init__(self, stream):
        '''
        stream: the stream to read from.
                Usually a process' stdout or stderr.
        '''
        self._s = stream
        self._q = Queue()

        class PopulateQueue(Thread):

            def __init__(self, socket, queue):
                Thread.__init__(self)
                self.daemon = True
                self.socket = socket
                self.queue = queue
                self.event = Event()

            def run(self):
                try:
                    while True:
                        # if self.event.is_set(): break
                        line = next(stream)
                        if line:
                            self.queue.put(line)
                        else:
                            # self.event.set()
                            pass
                        # self.event.wait(0.05)
                except StopIteration:
                    pass

        self._t = PopulateQueue(self._s, self._q)
        self._t.daemon = True
        self._t.start()  # start collecting lines from the stream

    def readline(self, timeout=None):
        try:
            return self._q.get(block=timeout is not None, timeout=timeout)
        except Empty:
            return None

    def close(self):
        # self._t.event.set()
        pass


class UnexpectedEndOfStream(Exception):
    pass
