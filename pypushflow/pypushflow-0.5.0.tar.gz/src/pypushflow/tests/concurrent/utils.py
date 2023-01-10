from contextlib import contextmanager
import subprocess
import traceback
import time
from typing import Any, Optional, Tuple

import pytest
from concurrent.futures import ProcessPoolExecutor as CfPool
from multiprocessing.pool import Pool as MpPool
from multiprocessing import get_context as get_mp_context
from multiprocessing import get_all_start_methods

try:
    from billiard.pool import Pool as BPool
    from billiard import get_context as get_billiard_context
except ImportError:
    BPool = None
    BProcess = None

from ...concurrent import get_pool
from ...concurrent import extract_remote_exception
from ...concurrent.factory import _POOLS


CONTEXTS = [None] + get_all_start_methods()
POOLS = [s for s in _POOLS if s and s != "scaling"]
TIMEOUT = 10


@contextmanager
def pool_context(scaling, pool_type, **pool_options):
    cpool_type = pool_type
    if scaling:
        cpool_type = "scaling"
        try:
            get_pool(pool_type)
        except ImportError as e:
            pytest.skip(str(e))
    try:
        pool_cls = get_pool(cpool_type)
    except ImportError as e:
        pytest.skip(str(e))
    pool_options.setdefault("wait_on_exit_timeout", TIMEOUT)
    with pool_cls(pool_type=pool_type, **pool_options) as pool:
        yield pool


def assert_callback(pool, name):
    libname, fn, result = SUCCESS[name]
    if fn is None:
        pytest.skip(f"requires {libname}")
    value, exception = _submit_with_cb(pool, fn)
    if exception is not None:
        raise exception
    assert value == result, str(value)


def assert_error_callback(pool, name):
    libname, fn, result = FAILURE[name]
    if fn is None:
        pytest.skip(f"requires {libname}")
    value, exception = _submit_with_cb(pool, fn)
    assert value is None
    assert str(exception) == str(result), str(value)
    assert isinstance(exception, type(result))

    tb = traceback.format_exception(type(exception), exception, exception.__traceback__)
    msg = "\n\n" + "".join(tb)
    assert any("in _fn_failure" in s for s in tb), msg
    assert any('raise RuntimeError("expected failure")' in s for s in tb), msg

    exception = extract_remote_exception(exception)

    tb = traceback.format_exception(type(exception), exception, exception.__traceback__)
    msg = "\n\n" + "".join(tb)
    assert any("in _fn_failure" in s for s in tb), msg
    assert any('raise RuntimeError("expected failure")' in s for s in tb), msg


def _submit_with_cb(pool, fn) -> Tuple[Any, Optional[Exception]]:
    value = None
    exception = None
    ev = Event()

    def cb(result):
        nonlocal value
        value = result
        ev.set()

    def ecb(result):
        nonlocal exception
        exception = result
        ev.set()

    pool.apply_async(fn, callback=cb, error_callback=ecb)
    assert ev.wait(timeout=TIMEOUT)

    return value, exception


def _fn_success() -> int:
    return 10


def _fn_failure():
    raise RuntimeError("expected failure")


def _fn_subprocess_success() -> int:
    return int(subprocess.check_output(["echo", "10"]).decode().strip())


def _fn_mppool_success() -> int:
    with MpPool() as pool:
        return pool.apply(_fn_success)


def _fn_mpprocess_success() -> int:
    ctx = get_mp_context()
    result = ctx.Manager().Value("i", 0)
    p = ctx.Process(target=_fn_mpprocess_success_helper, args=(result,))
    p.start()
    p.join()
    return result.value


def _fn_mpprocess_success_helper(result) -> None:
    result.value = 10


def _fn_cfpool_success() -> int:
    with CfPool() as pool:
        return pool.submit(_fn_success).result()


class Event:
    def __init__(self) -> None:
        self._is_set = False

    def set(self):
        self._is_set = True

    def wait(self, timeout=None):
        t0 = time.time()
        while not self._is_set:
            if timeout is not None:
                if (time.time() - t0) > timeout:
                    return False
            time.sleep(0.2)
        return True

    def reset(self):
        self._is_set = False


if BPool is None:
    _fn_bpool_success = None
    _fn_bprocess_success = None
else:

    def _fn_bpool_success() -> int:
        with BPool() as pool:
            return pool.apply(_fn_success)

    def _fn_bprocess_success() -> int:
        ctx = get_billiard_context()
        result = ctx.Manager().Value("i", 0)
        p = get_billiard_context().Process(
            target=_fn_bprocess_success_helper, args=(result,)
        )
        p.start()
        p.join()
        return result.value

    def _fn_bprocess_success_helper(result) -> None:
        result.value = 10


SUCCESS = {
    "simple": ("builtins", _fn_success, 10),
    "subprocess": ("subprocess", _fn_subprocess_success, 10),
    "cfpool": ("concurrent.futures", _fn_cfpool_success, 10),
    "mppool": ("multiprocessing", _fn_mppool_success, 10),
    "mpprocess": ("multiprocessing", _fn_mpprocess_success, 10),
    "bpool": ("billiard", _fn_bpool_success, 10),
    "bprocess": ("billiard", _fn_bprocess_success, 10),
}

FAILURE = {"simple": ("builtins", _fn_failure, RuntimeError("expected failure"))}
