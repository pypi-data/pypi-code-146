import itertools
import os
from typing import Callable, List

from reljicd_utils.file_system.file_system import (files_in_dir,
                                                   files_in_dir_recursive)
from reljicd_utils.logger.logger import get_logger
from reljicd_utils.multiprocessing.multiprocess import multiprocess
from reljicd_utils.utils import s3

LOGGER = get_logger(__name__)


def process_path(path: str,
                 func: Callable,
                 extension: str = '*',
                 recursive: bool = False,
                 num_of_processes: int = 1,
                 files_per_process: int = 1,
                 continue_from: int = 1,
                 log_every=1000,
                 spawn=False) -> None:
    files = files_in_path(path=path,
                          recursive=recursive,
                          extension=extension)

    files = itertools.islice(files, continue_from - 1, None)

    multiprocess(func, files, num_of_processes=num_of_processes,
                 map_chunk_size=files_per_process, spawn=spawn,
                 print_step=log_every,
                 print_progress=True)

    LOGGER.info("Done")


def files_in_path(path: str,
                  extension: str = '*',
                  recursive: bool = False) -> List[str]:
    if os.path.isfile(path):
        return [path]
    elif os.path.isdir(path):
        if recursive:
            return files_in_dir_recursive(path,
                                          extension=extension)
        else:
            return files_in_dir(path,
                                extension=extension)

    elif path.startswith('s3'):
        return list(s3.get_filenames(s3_path=path, full_names=True))
    else:
        raise FileNotFoundError
