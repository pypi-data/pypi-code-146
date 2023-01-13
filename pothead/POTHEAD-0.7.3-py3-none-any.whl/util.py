from threading import get_ident, Condition
from typing import Optional, Set


class ObjectProxy:
    """Decorator allowing override of attributes on an instance of another object

    >>> s1 = "hello"
    >>> s2 = ObjectProxy(s1)
    >>> s2.encode = lambda: b"goodbye!"
    >>> assert s1.encode() == b"hello"
    >>> assert s2.encode() == b"goodbye!"
    """

    def __init__(self, inner):
        self.__inner = inner

    def __getattr__(self, name):
        return getattr(self.__inner, name)

    def __call__(self, *args, **kwargs):
        return self.__inner(*args, **kwargs)


class ThreadsTracker:
    _threads: Optional[Set[int]]

    def __init__(self):
        self._threads = set()
        self._cond = Condition()

    def __enter__(self):
        self._threads.add(get_ident())
        return self

    def __exit__(self, exc_type, exc_value, trace):
        with self._cond:
            self._threads.remove(get_ident())
            self._cond.notify_all()

    def drain(self):
        with self._cond:
            self._cond.wait_for(lambda: len(self._threads) == 0)
