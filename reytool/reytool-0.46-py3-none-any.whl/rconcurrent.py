# !/usr/bin/env python
# -*- coding: utf-8 -*-

'''
@Time    : 2022-12-19 20:06:20
@Author  : Rey
@Contact : reyxbo@163.com
@Explain : Rey's concurrent methods
'''


from typing import Callable, Any, Generator, Optional
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed
from concurrent.futures._base import Future

from .rwrap import update_tqdm


def threads(
    func: Callable,
    *args: Any,
    max_workers: Optional[int] = None,
    thread_name: Optional[str] = None,
    timeout: Optional[int] = None,
    to_tqdm: bool = True,
    **kwargs: Any
) -> Generator:
    """
    Concurrent multi tasks using thread pool.

    Parameters
    ----------
    func : Task function.

    *args : Position parameter of input parameter task function.

    max_workers: Maximum number of threads.
        - int : Use this value, no maximum limit.
        - None : Number of CPU + 4, 32 maximum.

    thread_name: Thread name prefix and progress bar description.
        - str : Use this value.
        - None : Thread name prefix is 'ThreadPoolExecutor-%d' % index, and no progress bar.

    timeout : Call generator maximum waiting second, overtime throw error.
        - int : Use this value.
        - None : Unlimited.

    to_tqdm : Whether print progress bar.

    *kwargs : Keyword parameter of input parameter task function.
    
    Returns
    -------
    Generator with multi Future object, object from concurrent package.
    When called, it will block until all tasks are completed.
    When 'for' syntax it, the task that complete first return first.

    Examples
    --------
    Get value.
    >>> results = [future.result() for future in Generator]
    """

    if thread_name == None:
        thread_name = func.__name__
    parms_lens = {len(parm) for parm in args}
    parms_lens -= {1}
    min_parm_len = min(parms_lens)
    args = [
        list(parm) * min_parm_len
        if len(parm) == 1
        else parm
        for parm in args
    ]
    kwargs = [
        [[key, val]] * min_parm_len
        if len(val) == 1
        else [
            [key, parm]
            for parm in val
        ]
        for key, val in kwargs.items()
    ]
    if args:
        args = zip(*args)
    else:
        args = [[]] * min_parm_len
    if kwargs:
        kwargs = zip(*kwargs)
        kwargs = [dict(parm) for parm in kwargs]
    else:
        kwargs = [{}] * min_parm_len
    parms = zip(args, kwargs)
    thread_pool = ThreadPoolExecutor(max_workers, thread_name)
    if to_tqdm:
        tqdm_desc = "ThreadPool " + thread_name
        obj_tqdm = tqdm(desc=tqdm_desc, total=min_parm_len)
        func = update_tqdm(func, obj_tqdm, _execute=False)
    tasks = [thread_pool.submit(func, *args, **kwargs) for args, kwargs in parms]
    obj_tasks = as_completed(tasks, timeout)
    return obj_tasks