import time
import kthread

kthread.KThread.starttime = None
import threading
from collections import defaultdict

nested_dict = lambda: defaultdict(nested_dict)
import sys
from functools import wraps
from time import sleep


_module = sys.modules[__name__]
_module.results = nested_dict()
_module.results["done"] = False


def thread_capture(f_py=None):

    assert callable(f_py) or f_py is None

    def _decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            stime = kwargs["_starttime"]
            del kwargs["_starttime"]
            _module.results[stime]["results"] = func(*args, **kwargs)

        return wrapper

    return _decorator(f_py) if callable(f_py) else _decorator


def start_all_threads(
    functionlist,
    threadtlimit=50,
    timeout=1.0,
    sleepafterkill=1.0,
    sleepafterstart=0.001,
    ignore_exceptions=True,
    verbose=False,
):
    _module.results = nested_dict()
    _module.results["done"] = False
    alle = []
    counter = 0
    for target, args, kwargs, starttime in reversed(functionlist):

        kwargs["_starttime"] = starttime
        testx = kthread.KThread(
            target=target, name=f"{starttime}", args=args, kwargs=kwargs
        )
        testx.starttime = starttime
        _module.results[starttime]["results"] = None
        _module.results[starttime]["realstart"] = None
        alle.append(testx)
        counter += 1
    tt = kthread.KThread(
        target=start_threads,
        name="controlthread",
        args=(
            alle,
            threadtlimit,
            timeout,
            sleepafterkill,
            sleepafterstart,
            ignore_exceptions,
            verbose,
        ),
    )
    tt.starttime = None
    tt.start()
    return tt


def start_threads(
    alle,
    threadtlimit=50,
    timeout=1.0,
    sleepafterkill=1.0,
    sleepafterstart=0.001,
    ignore_exceptions=True,
    verbose=False,
):

    startedthreads = {}
    alivenow = []

    while alle:
        howmanyadd = threadtlimit - len(alivenow)
        if not startedthreads:
            howmanyadd = threadtlimit
        counter = 0
        while counter <= howmanyadd and alle:
            try:
                g = alle.pop()
                startedthreads[g.starttime] = g
                startedthreads[g.starttime].start()
                _module.results[g.starttime]["realstart"] = time.time()
                if verbose:
                    print(startedthreads)
                counter += 1
                sleep(sleepafterstart)
            except Exception as axa:
                if verbose:
                    print(axa)
                if not ignore_exceptions:
                    raise axa
                continue
        alivenow = []

        for key, item in startedthreads.items():
            try:
                if item.is_alive():
                    alivenow.append(1)
                    if _module.results[item.starttime]["realstart"] is None:
                        continue

                    try:
                        if (
                            time.time() - _module.results[item.starttime]["realstart"]
                            > timeout
                        ):
                            try:
                                item.kill()
                                sleep(sleepafterkill)
                                if verbose:
                                    print(f"{item} is alive: {item.is_alive()}")
                            except Exception as faz:
                                if verbose:
                                    print(faz)
                                if not ignore_exceptions:
                                    raise faz
                                continue
                    except Exception as axs:
                        if verbose:
                            print(axs)
                        if not ignore_exceptions:

                            raise axs

            except Exception as fax:
                if verbose:
                    print(fax)
                if not ignore_exceptions:
                    raise fax
                continue
        if len(alivenow) >= threadtlimit:
            if verbose:
                print(f"Active threads: {len(alivenow)}")
            continue
    lastchecktime = time.time()
    somethingthere = True
    while somethingthere:
        somethingthere = False
        for key, item in threading.__dict__["_active"].copy().items():
            if item._name in _module.results.keys():
                if verbose:
                    print(f"{item._name} active")
                somethingthere = True
                sleep(0.001)
                if time.time() - lastchecktime > timeout:
                    try:
                        item.kill()
                        sleep(sleepafterkill)
                        if verbose:
                            print(f"{item} is alive: {item.is_alive()}")
                    except Exception as faz:
                        if verbose:
                            print(faz)
                        if not ignore_exceptions:
                            raise faz
                        continue

    _module.results["done"] = True
    if verbose:
        print(threading.__dict__["_active"])
