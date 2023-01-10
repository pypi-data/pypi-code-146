from contextlib import contextmanager
from multiprocessing import get_context

try:
    from multiprocessing import get_context as bget_context
except ImportError:
    bget_context = None
import pytest

from ..conftest import gevent_patched


@contextmanager
def filter_callback(pool_type, task_name, context):
    assert pool_type
    assert task_name
    exception = None
    match = None
    context = _context_name(pool_type, context)
    gevent_incompatible_tasks = ("mppool", "bpool", "mpprocess", "bprocess")
    if pool_type in ("billiard", "multiprocessing"):
        if gevent_patched():
            pytest.skip("does not work with 'gevent' monkey patching")
        if task_name in ["mppool", "mpprocess", "cfpool"]:
            exception = AssertionError
            match = "daemonic processes are not allowed to have children"
        elif task_name in ["bpool"]:
            pytest.skip("hangs sometimes")
    elif pool_type == "ndmultiprocessing":
        if gevent_patched():
            pytest.skip("does not work with 'gevent' monkey patching")
        if task_name in ["bpool"]:
            pytest.skip("hangs sometimes")
    elif pool_type in ("process", "ndprocess"):
        if gevent_patched():
            if task_name in gevent_incompatible_tasks:
                pytest.skip("task not compatible with gevent")
            if context == "spawn":
                pytest.skip("spawn hangs with gevent")
        else:
            if task_name in ["bpool"]:
                pytest.skip("hangs sometimes")
    elif pool_type == "thread":
        if gevent_patched():
            if task_name in gevent_incompatible_tasks:
                pytest.skip("task not compatible with gevent")
        else:
            if task_name in ["bpool"]:
                pytest.skip("hangs sometimes")
    elif pool_type == "gevent":
        if task_name in gevent_incompatible_tasks:
            pytest.skip("task not compatible with gevent")

    if exception is None:
        yield
    else:
        with pytest.raises(exception, match=match):
            yield


@contextmanager
def filter_error_callback(pool_type, task_name, context):
    assert pool_type
    assert task_name
    context = _context_name(pool_type, context)
    if pool_type in ("process", "ndprocess"):
        if gevent_patched():
            if context == "spawn":
                pytest.skip("spawn hangs with gevent")
    yield


def _context_name(pool_type, context):
    if context is not None:
        return context
    if pool_type in "billiard":
        return bget_context()._name
    else:
        return get_context()._name
