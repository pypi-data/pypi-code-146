"""Utilities to terminate gevent pool tasks
"""

from gevent import GreenletExit
from . import StopPypushflowTask


def task_main(fn, *args, **kwargs):
    try:
        return fn(*args, **kwargs)
    except GreenletExit:
        raise StopPypushflowTask("stop task due to interrupt") from None


def interrupt_task(glt) -> None:
    glt.kill()
