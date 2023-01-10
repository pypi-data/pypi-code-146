"""Utilities to terminate process pool tasks
"""

import os
import signal
from contextlib import contextmanager
from . import StopPypushflowTask

_TERMINATE_SIGNAL = signal.SIGINT


def task_main(fn, *args, **kwargs):
    with _task_context():
        return fn(*args, **kwargs)


def interrupt_task(pid) -> None:
    # TODO: on windows this kills the subprocess
    #       despite that fact that we handle the
    #       signal in the subprocess
    try:
        os.kill(pid, _TERMINATE_SIGNAL)
    except ProcessLookupError:
        pass  # process already ended


def worker_initializer():
    _set_terminate_handler(signal.SIG_IGN)


@contextmanager
def _task_context():
    def stop_task_handler(signum, frame):
        nonlocal old_handler
        if old_handler is None:
            old_handler = signal.SIG_IGN
        signal.signal(signum, old_handler)
        raise KeyboardInterrupt(f"stop task due to signal {signum}")

    old_handler = _set_terminate_handler(stop_task_handler)

    try:
        yield
    except KeyboardInterrupt as e:
        raise StopPypushflowTask(str(e)) from None
    finally:
        _set_terminate_handler(old_handler)


def _set_terminate_handler(handler):
    try:
        return signal.signal(_TERMINATE_SIGNAL, handler)
    except (OSError, AttributeError, ValueError, RuntimeError):
        pass
