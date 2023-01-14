import multiprocessing
import sys
from contextlib import contextmanager
from typing import Callable, Iterable

from str2bool import str2bool

from reljicd_utils.collections import chunks, iter_counter
from reljicd_utils.config import get_env
from reljicd_utils.logger import get_logger

LOGGER = get_logger(__name__)
SPAWN: bool = str2bool(get_env(key='SPAWN', default='False'))


@contextmanager
def spawn_scope(spawn: bool = None):
    if spawn is None:
        spawn = SPAWN

    if spawn:
        multiprocessing.set_start_method('spawn', force=True)

    yield

    if spawn:
        if sys.platform != "win32":
            multiprocessing.set_start_method('fork', force=True)


def multiprocess(func: Callable,
                 iterable: Iterable,
                 num_of_processes: int,
                 chunks_size: int = 1,
                 map_chunk_size: int = 50,
                 spawn: bool = None,
                 print_progress: bool = False,
                 print_step: int = 10000) -> None:
    if print_progress:
        iterable = iter_counter(iterable=iterable,
                                print_step=print_step,
                                print_message='Processing element')

    if num_of_processes == 1:
        for args in iterable:
            func(args)
    else:
        with spawn_scope(spawn=spawn):
            with multiprocessing.Pool(processes=num_of_processes) as p:
                for iter_chunk in chunks(iterable, chunks_size):
                    for _ in p.imap_unordered(func,
                                              iter_chunk,
                                              chunksize=map_chunk_size):
                        pass
