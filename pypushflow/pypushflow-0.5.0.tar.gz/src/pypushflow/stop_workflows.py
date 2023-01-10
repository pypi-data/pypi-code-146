"""Utilities to stop workflows on certain signals
"""

import os
import signal
from weakref import WeakKeyDictionary
from typing import Optional, Sequence
from contextlib import contextmanager

if os.name == "nt":
    DEFAULT_STOP_SIGNALS = (signal.SIGINT,)
else:
    DEFAULT_STOP_SIGNALS = (signal.SIGTERM,)


class StopPypushflowWorkflow(Exception):
    pass


@contextmanager
def stop_on_signals_context(workflow, stop_signals: Optional[Sequence] = None):
    if workflow in _WORKFLOWS:
        yield
        return
    if stop_signals is None:
        stop_signals = DEFAULT_STOP_SIGNALS
    _WORKFLOWS[workflow] = stop_signals
    try:
        for signum in stop_signals:
            _stop_workflows_on_signal(signum)
        yield
    finally:
        _WORKFLOWS.pop(workflow)
        _reset_signals_handlers()


_WORKFLOWS = WeakKeyDictionary()
_OLD_HANDLERS = dict()


def _stop_workflows_on_signal(signum):
    if signum in _OLD_HANDLERS:
        return

    def stop_workflows_handler(signum, frame):
        for workflow, stop_signals in list(_WORKFLOWS.items()):
            if signum not in stop_signals:
                continue
            workflow.stop(f"stop workflow due to signal {signum}")

    _OLD_HANDLERS[signum] = _set_handler(signum, stop_workflows_handler)


def _reset_signals_handlers():
    keep = {signum for _, lst in _WORKFLOWS.values() for signum in lst}
    remove = set(_OLD_HANDLERS) - keep
    for signum in remove:
        old_handler = _OLD_HANDLERS.pop(signum)
        _set_handler(signum, old_handler)


def _set_handler(signum, handler):
    try:
        old_handler = signal.signal(signum, handler)
    except (OSError, AttributeError, ValueError, RuntimeError):
        pass
    if old_handler is None:
        return signal.SIG_IGN
    return old_handler
