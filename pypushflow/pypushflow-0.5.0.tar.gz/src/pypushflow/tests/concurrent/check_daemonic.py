import sys
from concurrent.futures import ProcessPoolExecutor as CfPool

from multiprocessing.pool import Pool as MpPool
from multiprocessing import Value as MpValue
from multiprocessing import get_context as get_mp_context
from multiprocessing import current_process as current_mp_process
from multiprocessing import get_all_start_methods
from multiprocessing import set_start_method

from billiard.pool import Pool as BPool
from billiard import get_context as get_billiard_context
from billiard import Value as BValue
from billiard import current_process as current_b_process

from pypushflow.concurrent.non_daemonic import get_context as get_nd_context


def current_process_is_daemonic(result=None, billiard=False):
    if billiard:
        func = current_b_process
    else:
        func = current_mp_process
    if result is None:
        return func().daemon
    else:
        result.value = func().daemon


def exec_mppool(context=None):
    with MpPool(context=get_mp_context(context)) as pool:
        return pool.apply(current_process_is_daemonic)


def exec_nd_mppool(context=None):
    with MpPool(context=get_nd_context(context)) as pool:
        return pool.apply(current_process_is_daemonic)


def exec_bpool(context=None):
    with BPool(context=get_billiard_context(context)) as pool:
        return pool.apply(current_process_is_daemonic, kwds={"billiard": True})


def exec_cfpool(context=None):
    if sys.version_info >= (3, 7):
        with CfPool(mp_context=get_mp_context(context)) as pool:
            return pool.submit(current_process_is_daemonic).result()
    else:
        set_start_method(context, force=True)
        with CfPool() as pool:
            return pool.submit(current_process_is_daemonic).result()


def exec_nd_cfpool(context=None):
    if sys.version_info >= (3, 7):
        with CfPool(mp_context=get_nd_context(context)) as pool:
            return pool.submit(current_process_is_daemonic).result()


def exec_mpprocess(context=None):
    result = MpValue("i", 0)
    p = get_mp_context(context).Process(
        target=current_process_is_daemonic, args=(result,)
    )
    p.start()
    p.join()
    return bool(result.value)


def exec_nd_mpprocess(context=None):
    result = MpValue("i", 0)
    p = get_nd_context(context).Process(
        target=current_process_is_daemonic, args=(result,)
    )
    p.start()
    p.join()
    return bool(result.value)


def exec_bprocess(context=None):
    result = BValue("i", 0)
    p = get_billiard_context(context).Process(
        target=current_process_is_daemonic, args=(result,), kwargs={"billiard": True}
    )
    p.start()
    p.join()
    return bool(result.value)


if __name__ == "__main__":
    daemonic = {True: list(), False: list(), None: list()}
    for context in get_all_start_methods():
        for func in (
            exec_mppool,
            exec_nd_mppool,
            exec_bpool,
            exec_cfpool,
            exec_nd_cfpool,
            exec_mpprocess,
            exec_nd_mpprocess,
            exec_bprocess,
        ):
            daemonic[func(context)].append(f" {func.__name__}('{context}')")

    print("Daemonic:")
    for name in daemonic[True]:
        print(name)
    print("Non-Daemonic:")
    for name in daemonic[False]:
        print(name)
    print("Not supported:")
    for name in daemonic.get(None):
        print(name)
