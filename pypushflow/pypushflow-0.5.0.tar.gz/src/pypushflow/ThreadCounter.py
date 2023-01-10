from threading import Condition
from pypushflow.logutils import PyPushflowLoggedObject


class ThreadCounter(PyPushflowLoggedObject):
    """Scheduling thread counter"""

    def __init__(self, parent=None):
        self.__counter = 0
        self.__condition = Condition()
        super().__init__(parent=parent)

    def start_thread(self, msg=None):
        with self.__condition:
            self.__counter += 1
            self._log_counter_change(msg=msg)
            self.__condition.notify_all()

    def end_thread(self, msg=None):
        with self.__condition:
            self.__counter = max(self.__counter - 1, 0)
            self._log_counter_change(msg=msg)
            self.__condition.notify_all()

    def __enter__(self):
        self.start_thread()
        return self

    def __exit__(self, *args):
        self.end_thread()

    def wait_threads_finished(self, timeout=None):
        """Returns False when timeout expires"""
        while True:
            with self.__condition:
                if self.__counter == 0:
                    break
                if not self.__condition.wait(timeout=timeout):
                    return False
        return True

    @property
    def nthreads(self):
        return self.__counter

    def _log_counter_change(self, msg=None):
        if msg is None:
            msg = "Thread counter changed"
        self.logger.debug("%s (%d threads running)", msg, self.__counter)
