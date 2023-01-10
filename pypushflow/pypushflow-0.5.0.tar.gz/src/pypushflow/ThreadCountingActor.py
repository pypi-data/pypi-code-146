from functools import wraps
from contextlib import contextmanager
from pypushflow.logutils import PyPushflowLoggedObject
from pypushflow.ActorInterface import ActorInterface


def with_thread_context(trigger):
    """Wraps the `trigger` method of all derived classes of ThreadCountingActor"""

    @wraps(trigger)
    def wrapper(self, *args, **kw):
        with self._thread_context():
            return trigger(self, *args, **kw)

    return wrapper


def callback_with_end_thread(async_callback, end_thread, log_msg):
    """Wraps a async_callback"""

    @wraps(async_callback)
    def wrapper(*args, **kw):
        try:
            return async_callback(*args, **kw)
        finally:
            end_thread(msg=log_msg)

    return wrapper


class ThreadCountingActor(PyPushflowLoggedObject, ActorInterface):
    """The `trigger` method will increase the thread counter
    at the start and decrease the thread counter at the end.
    """

    def __init__(self, name=None, parent=None, thread_counter=None):
        if name is None:
            raise RuntimeError("Actor name is None!")
        if thread_counter is None:
            raise ValueError("Actor requires a 'thread_counter' argument")
        super().__init__(log_metadata={"actor": name}, parent=parent)
        self.name = name
        self.parent = parent
        if parent is not None:
            parent.addActorRef(self)
        self.__thread_counter = thread_counter
        self.__in_thread_context = False
        self.__postpone_end_thread = False

    def __init_subclass__(subcls, **kw):
        """Wrap the `trigger` method"""
        super().__init_subclass__(**kw)
        subcls.trigger = with_thread_context(subcls.trigger)

    @contextmanager
    def _thread_context(self):
        """Re-entrant context manager that starts a thread
        on first entrance and ends a thread on last exit,
        unless the thread ending is post-poned until after
        and async callback.
        """
        if self.__in_thread_context:
            yield
            return
        self.__thread_counter.start_thread(msg="Thread started for " + repr(self.name))
        try:
            self.__in_thread_context = True
            self.__postpone_end_thread = False
            try:
                yield
            finally:
                self.__in_thread_context = False
        finally:
            if self.__postpone_end_thread:
                self.__postpone_end_thread = False
            else:
                self.__thread_counter.end_thread(
                    msg="Thread ended for " + repr(self.name)
                )

    @contextmanager
    def _postpone_end_thread(self, *async_callbacks):
        """Post-pone thread ending until after an async callback is executed.

        Only one of the async callbacks is expected to be called.
        """
        if self.__in_thread_context:
            self.__postpone_end_thread = True
        try:
            async_callbacks = tuple(
                callback_with_end_thread(
                    async_callback,
                    self.__thread_counter.end_thread,
                    "Thread ended for " + repr(self.name),
                )
                for async_callback in async_callbacks
            )
            yield async_callbacks
        except BaseException:
            if self.__in_thread_context:
                self.__postpone_end_thread = False
            raise

    def _wait_threads_finished(self, **kw):
        return self.__thread_counter.wait_threads_finished(**kw)
