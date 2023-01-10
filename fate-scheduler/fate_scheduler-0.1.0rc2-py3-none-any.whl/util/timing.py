import time


class Timing:

    class StaleTimer(ValueError):
        pass

    def __init__(self):
        self.t0 = self.t1 = self.proc0 = self.proc1 = None

    def start(self):
        if self.t0 is not None:
            raise self.StaleTimer

        self.t0 = time.time()
        self.proc0 = time.process_time()

    def stop(self):
        if self.t1 is not None:
            raise self.StaleTimer

        self.t1 = time.time()
        self.proc1 = time.process_time()

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, *exc_info):
        self.stop()

    @property
    def time_elapsed(self):
        if self.t0 is None or self.t1 is None:
            return None

        return self.t1 - self.t0

    @property
    def proc_elapsed(self):
        if self.proc0 is None or self.proc1 is None:
            return None

        return self.proc1 - self.proc0

    def __iter__(self):
        yield self.time_elapsed
        yield self.proc_elapsed

    def __repr__(self):
        return f'<{self.__class__.__name__}: {self}>'

    def __str__(self):
        return (f'total time elapsed {self.time_elapsed} | '
                f'process time elapsed {self.proc_elapsed}')
