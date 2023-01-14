import functools
from typing import Callable, List
from concurrent.futures import ThreadPoolExecutor


class FuncThread(object):
    sub_tasks: list
    workers: ThreadPoolExecutor

    def __init__(self, fn, *, run_times: int = 1):
        self.f: Callable = fn
        self.thrds = run_times

    def __len__(self):
        return len(self.sub_tasks)

    def cancel(self, shutdown=False):
        if hasattr(self, 'sub_tasks'):
            [t.cancel() for t in self if not t.running()]
        shutdown and self.workers.shutdown()

    def __iter__(self):
        if hasattr(self, 'sub_tasks'):
            yield from self.sub_tasks
        else:
            raise Exception('func not start')

    def __call__(self, *args, block=False, **kwargs):
        thrds = min(self.thrds, 5)
        if thrds > 0:
            self.workers = ThreadPoolExecutor(thrds)
            self.sub_tasks = [self.workers.submit(self.f, *args, **kwargs)
                              for _ in range(self.thrds)]
            return block and [t.result() for t in self.sub_tasks] or self
        raise Exception('run times is 0')


class GroupThread(object):
    sub_tasks: list

    def __init__(self, fns: List = None, *, concurrency=1):
        self.concurrency = concurrency
        self.group = [self.add(f) for f in fns or []]

    def add(self, fn=None, **default_kwargs):
        def pack(f):
            f = self._f_wrap(f)

            @functools.wraps(f)
            def inner(*args, **kwargs):
                params = {**default_kwargs, **kwargs}
                self.group.append(functools.partial(f, *args, **params))

            return inner

        return fn and pack(fn) or pack

    @staticmethod
    def _f_wrap(f):
        @functools.wraps(f)
        def inner(*args, **kwargs):
            return {f.__name__: f(*args, **kwargs)}

        return inner

    def cancel(self):
        if hasattr(self, 'sub_tasks'):
            [t.cancel() for t in self.sub_tasks if not t.running()]

    def __iter__(self):
        if hasattr(self, 'sub_tasks'):
            yield from self.sub_tasks
        else:
            raise Exception('group not start')

    def __call__(self, block=False):
        concurrency = min(self.concurrency, len(self.group), 5)
        if concurrency > 0:
            worker = ThreadPoolExecutor(concurrency)
            self.sub_tasks = [worker.submit(f) for f in self.group]
            return block and [t.result() for t in self.sub_tasks] or self
        raise Exception('concurrency is 0')


def repeat_wraps(fn=None, *, run_times=1, **default_args):
    def wrap(f):
        @functools.wraps(f)
        def inner(*args, **kwargs):
            params = {**default_args, **kwargs}
            return FuncThread(f, run_times=run_times)(*args, **params)

        return inner

    return fn and wrap(fn) or wrap


__all__ = ('FuncThread', 'repeat_wraps', 'GroupThread')
