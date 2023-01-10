import sys
import logging
from typing import Optional

from .thread import ThreadPool
from .process import ProcessPool

if sys.version_info >= (3, 7):
    from .ndprocess import NdProcessPool
else:
    NdProcessPool = None

try:
    from gevent.monkey import is_anything_patched

    if not is_anything_patched():
        raise ImportError("gevent did not patch anything")

    from .gevent import GreenletPool
except ImportError:
    # gevent is missing or didn't monkey patch the environment
    GreenletPool = None

    from .multiprocessing import MProcessPool
    from .ndmultiprocessing import NProcessPool

    try:
        from .billiard import BProcessPool
    except ImportError:
        BProcessPool = None
else:
    MProcessPool = None
    NProcessPool = None
    BProcessPool = None

from .scaling import ScalingPool

logger = logging.getLogger(__name__)

_POOLS = {
    "thread": ThreadPool,
    "process": ProcessPool,
    "ndprocess": NdProcessPool,
    "multiprocessing": MProcessPool,
    "ndmultiprocessing": NProcessPool,
    "billiard": BProcessPool,
    "gevent": GreenletPool,
    "scaling": ScalingPool,
}

_MESSAGES = {
    "ndprocess": "not supported in python < 3.6",
    "billiard": "requires 'billiard'"
    if GreenletPool is None
    else "does not work with 'gevent' monkey patching",
    "gevent": "requires 'gevent' with monkey patching",
    "multiprocessing": "does not work with 'gevent' monkey patching",
    "ndmultiprocessing": "does not work with 'gevent' monkey patching",
}


def get_pool(pool_type: Optional[str] = None):
    if pool_type is None:
        if GreenletPool is None:
            pool_type = "process"
        else:
            pool_type = "gevent"
    pool = _POOLS[pool_type]
    if pool is None:
        raise ImportError(
            _MESSAGES.get(pool_type, f"pool type '{pool_type}' is unknown")
        )
    logger.info(f"pypushflow concurrency: {pool_type}")
    return pool
