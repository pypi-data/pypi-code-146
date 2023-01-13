import logging
import sys
from concurrent.futures import ThreadPoolExecutor
from functools import wraps
from typing import Any
from typing import Callable
from typing import Optional
from typing import TypeVar

from jumonc import settings

if sys.version_info < (3, 10):
    from typing_extensions import ParamSpec
else:
    from typing import ParamSpec

logger = logging.getLogger(__name__)

_thread_pool: Optional[ThreadPoolExecutor] = None
_task_pool_avaiable = False



def setupTaskPool() -> None:
    global _thread_pool
    global _task_pool_avaiable
    if _task_pool_avaiable:
        return
    logger.info("started task pool with a maximum of %s workers", str(settings.MAX_WORKER_THREADS))
    _thread_pool = ThreadPoolExecutor(settings.MAX_WORKER_THREADS)
    _task_pool_avaiable = True


P = ParamSpec('P')
T = TypeVar('T')
def executeAsTask(func: Callable[P, T]) -> Callable[P, Optional[T]]:
    @wraps(func)
    def decorated_function(*args: Any, **kwargs: Any
                          ) -> Optional[T]:
        if kwargs["duration"] >= settings.SHORT_JOB_MAX_TIME:
            addTask(func, *args, **kwargs)
            return None
        return func(*args, **kwargs)
        
    return decorated_function
        
def addTask(func: Callable, *args: Any, **kwargs: Any) -> None:
    setupTaskPool()
    if _thread_pool is None:
        logger.error("Thread Pool should be available")
        return
    _thread_pool.submit(func, *args, **kwargs)
