from contextlib import contextmanager, ExitStack
import threading


class SharedLockPool:
    """
    Allows to acquire locks identified by name (hashable type) recursively.
    """

    def __init__(self):
        self.__locks = {}
        self.__locks_mutex = threading.Semaphore(value=1)

    def __len__(self):
        return len(self.__locks)

    @property
    def names(self):
        return list(self.__locks.keys())

    @contextmanager
    def _modify_locks(self):
        self.__locks_mutex.acquire()
        try:
            yield self.__locks
        finally:
            self.__locks_mutex.release()

    @contextmanager
    def acquire(self, name):
        with self._modify_locks() as locks:
            lock = locks.get(name, None)
            if lock is None:
                locks[name] = lock = threading.RLock()
        lock.acquire()
        try:
            yield
        finally:
            lock.release()
            with self._modify_locks() as locks:
                if name in locks:
                    locks.pop(name)

    @contextmanager
    def acquire_context_creation(self, name, contextmngr, *args, **kwargs):
        """
        Acquire lock only during context creation.

        This can be used for example to protect the opening of a file
        but not hold the lock while the file is open.
        """
        with ExitStack() as stack:
            with self.acquire(name):
                ret = stack.enter_context(contextmngr(*args, **kwargs))
            yield ret
