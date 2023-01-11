from big_thing_py.common.common import *

from threading import Thread, Event, Lock
from queue import Queue, Empty


class SoPThread:

    class Mode(Enum):
        LOCK = 0
        EVENT = 1

    def __init__(self, name: str = None, func: Callable = None, arg_list: Tuple = None, kwargs_list: dict = None, daemon: bool = True, mode: List[str] = []) -> None:
        self._name: str = name
        self._func: Callable = func
        self._arg_list: Tuple = arg_list
        self._kwargs_list: dict = kwargs_list
        self._daemon: List[str] = daemon

        self._thread = Thread()

        if func:
            self.set_thread()
        else:
            raise Exception('[SoPThread] No function to run')

    def set_thread(self) -> None:
        if isinstance(self._arg_list, tuple):
            self._arg_list: list = list(self._arg_list)
        else:
            self._arg_list = []

        self._arg_list = tuple(self._arg_list)

        if not self._name:
            self._name = '_'.join(self._func.__name__.split('_')[:-1])

        if self._kwargs_list:
            self._thread = Thread(
                target=self._func, name=self._name, kwargs=self._kwargs_list, daemon=self._daemon)
        else:
            self._thread = Thread(
                target=self._func, name=self._name, args=self._arg_list, daemon=self._daemon)

    def start(self) -> None:
        self._thread.start()

    def join(self) -> None:
        self._thread.join()
        
    def is_alive(self) -> bool:
        return self._thread.is_alive()

    def get_name(self) -> str:
        return self._name
