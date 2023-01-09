# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time    : 2022-12-05 14:12:25
@Author  : Rey
@Contact : reyxbo@163.com
@Explain : Rey's decorators
"""


from typing import Any, Callable, Optional, Union
import time
from tqdm import tqdm as tqdm_tqdm
from threading import Thread
from functools import wraps as functools_wraps

from .rcommon import exc
from .rtext import print_frame
from .rtime import now


def wrap_frame(decorator: Callable) -> Callable:
    """
    Decorative frame.

    Parameters
    ----------
    decorator : Decorator function.

    Retuens
    -------
    Decorator after decoration.

    Examples
    --------
    Decoration function method one.
    >>> @wrap_func
    >>> def func(): ...
    >>> func_ret = func(parm_a, parm_b, parm_c=1, parm_d=2)

    Decoration function method two.
    >>> def func(): ...
    >>> func_ret = wrap_func(func, parm_a, parm_b, parm_c=1, parm_d=2)

    Decoration function method three.
    >>> def func(): ...
    >>> func_ret = wrap_func(func, _execute=True)
    
    Decoration function method four.
    >>> def func(): ...
    >>> func = wrap_func(func)
    >>> func_ret = func(parm_a, parm_b, parm_c=1, parm_d=2)

    Decoration function method five.
    >>> def func(): ...
    >>> func = wrap_func(func, parm_a, parm_c=1, _execute=False)
    >>> func_ret = func(parm_b, parm_d=2)
    """

    @functools_wraps(decorator)
    def wrap(func: Callable, *args: Any, _execute: Optional[bool] = None, **kwargs: Any) -> Union[Callable, Any]:
        """
        Decorative shell.

        Parameters
        ----------
        _execute : Whether execute function, otherwise decorate function.
            - bool : Use this value.
            - None : When parameter *args or **kwargs have values, then True, otherwise False.
        
        Returns
        -------
        Function after decoration or return of function.
        """

        if _execute == None:
            if args or kwargs:
                _execute = True
            else:
                _execute = False

        if _execute:
            func_ret = decorator(func, *args, **kwargs)
            return func_ret
        
        else:
            @functools_wraps(func)
            def wrap_sub(*_args: object, **_kwargs: object) -> object:
                """
                Decorative sub shell.
                """

                func_ret = decorator(func, *args, *_args, **kwargs, **_kwargs)
                return func_ret
            return wrap_sub
    return wrap

def wraps(*wrap_funcs: Callable) -> Callable:
    """
    Batch decorate.

    parameters
    ----------
    wrap_funcs : Decorator function.

    Retuens
    -------
    Function after decoration.

    Examples
    --------
    Decoration function.
    >>> @wraps(print_funtime, state_thread)
    >>> def func(): ...
    >>> func_ret = func()

        Same up and down

    >>> @print_funtime
    >>> @state_thread
    >>> def func(): ...
    >>> func_ret = func()

        Same up and down

    >>> def func(): ...
    >>> func = print_funtime(func)
    >>> func = state_thread(func)
    >>> func_ret = func()
    """

    def func(): ...
    for wrap_func in wrap_funcs:
        
        @functools_wraps(func)
        def wrap(func: Callable) -> Callable:
            """
            Decorative shell
            """

            @functools_wraps(func)
            def wrap_sub(*args: object, **kwargs: object) -> object:
                """
                Decorative sub shell
                """

                func_ret = wrap_func(func, *args, _execute=True, **kwargs)
                return func_ret
            return wrap_sub
        func = wrap
    return wrap

@wrap_frame
def runtime(func: Callable, *args: Any, _precision: int = 2, **kwargs: Any) -> Any:
    """
    Print run time of the function.

    Parameters
    ----------
    func : Function to be decorated.

    *args : Position parameter of input parameter decorated function.

    _precision : Precistion of print time.

    *kwargs : Keyword parameter of input parameter decorated function.

    Returns
    -------
    Return of decorated function.
    """

    start_datetime = now()
    start_timestamp = now("timestamp")
    func_ret = func(*args, **kwargs)
    end_datatime = now()
    end_timestamp = now("timestamp")
    spend_timestamp = end_timestamp - start_timestamp
    spend_second = round(spend_timestamp, _precision)
    print_content = "Start: %s -> Spend: %ss -> End: %s" % (start_datetime, spend_second, end_datatime)
    title = func.__name__
    print_frame(print_content, title=title)
    return func_ret

@wrap_frame
def start_thread(func: Callable, *args: Any, _daemon: bool = True, **kwargs: Any) -> None:
    """
    Function start in thread.

    Parameters
    ----------
    func : Function to be decorated.

    *args : Position parameter of input parameter decorated function.

    _daemon : Whether it is a daemon thread.

    *kwargs : Keyword parameter of input parameter decorated function.
    """

    thread_name = "%s_%s" % (func.__name__, str(int(time.time() * 1000)))
    thread = Thread(target=func, name=thread_name, args=args, kwargs=kwargs)
    thread.daemon = _daemon
    thread.start()

@wrap_frame
def try_exc(
    func: Callable,
    *args: Any,
    **kwargs: Any
) -> Union[Any, None]:
    """
    Execute function with 'try' syntax and print error information.

    Parameters
    ----------
    func : Function to be decorated.

    *args : Position parameter of input parameter decorated function.

    *kwargs : Keyword parameter of input parameter decorated function.

    Returns
    -------
    Return of decorated function or no return.
    """

    try:
        func_ret = func(*args, **kwargs)
        return func_ret
    except:
        func_name = func.__name__
        exc(func_name)

@wrap_frame
def update_tqdm(
    func: Callable,
    tqdm: tqdm_tqdm,
    *args: Any,
    _desc: Optional[str] = None,
    _step: Union[int, float] = 1,
    **kwargs: Any
) -> Any:
    """
    Update progress bar tqdm object of tqdm package.

    Parameters
    ----------
    func : Function to be decorated.

    tqdm : Progress bar tqdm object.

    *args : Position parameter of input parameter decorated function.
    
    _desc : Progress bar description.
        - str : Add description.
        - None : no description.

    _step : Progress bar step size.
        - When greater than 0, then forward.
        - When less than 0, then backward.

    *kwargs : Keyword parameter of input parameter decorated function.

    Returns
    -------
    Return of decorated function or no return.
    """

    if _desc != None:
        tqdm.set_description(_desc)
    func_ret = func(*args, **kwargs)
    tqdm.update(_step)
    return func_ret