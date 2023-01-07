"""@Author: Rayane AMROUCHE

Addition to pandas.
"""
import inspect

from datetime import datetime
from typing import Any, List, Generator, Callable, Tuple

import pandas as pd  # type: ignore
import numpy as np  # type: ignore

from dsmanager.controller.utils import i_display


def _loop_pipe(
    df_: pd.DataFrame, generator: Generator[Tuple[Callable[..., Any], Any], None, None]
) -> pd.DataFrame:
    """Wrap chain function to a DataFrame using a generator to apply multiple functions
        and theirs arguments in chain.

    Args:
        df_ (pd.DataFrame): DataFrame that will be piped.
        generator (Generator[Tuple[Callable[..., Any], Any], None, None]): Reversed
            generator of functions and their respective arguments and keyword arguments.

    Returns:
        pd.DataFrame: Returns original DataFrame to keep chaining.
    """
    cur_args = {}
    try:
        cur = next(generator)
        if isinstance(cur, tuple):
            cur_func = cur[0]
            cur_args = cur[1]
        else:
            cur_func = cur
    except StopIteration:
        return df_
    return cur_func(_loop_pipe(df_, generator), **cur_args)


def to_datamanager(
    df_: pd.DataFrame, datamanager: Any, name: str, **kwargs: Any
) -> pd.DataFrame:
    """Get info for a specified dataset and return it as a DataFrame.

    Args:
        df_ (pd.DataFrame): DataFrame to be saved.
        dm (DataManager): DataManager where the DataFrame will be saved.
        name (str): Name of the dataset to save.

    Returns:
        pd.DataFrame: Returns original DataFrame to keep chaining.
    """
    file_info = datamanager.get_file_info(name)
    datamanager.save_data(df_, file_info, **kwargs)
    return df_


def pipe_sklearn(
    df_: pd.DataFrame,
    func: Any,
    filter_func: Any = lambda df__: df__,
    output_cols: List[str] | None = None,
    datamanager: Any = None,
    **kwargs: Any,
) -> pd.DataFrame:
    """Wrap sklearn functions and classes.

    Args:
        df_ (pd.DataFrame): DataFrame that will be piped.
        func (Any): Function to wrap.
        filter_func (Any, optional): Filter function to apply on original df_. Defaults
            to lambda df__ : df__.
        output_cols (List[str], optional): List of output columns expected. Defaults to
            None.
        datamanager (Any, optional): Datamanager instance. Defaults to None.

    Returns:
        pd.DataFrame: Returns original DataFrame to keep chaining.
    """
    index_list = filter_func(df_).index

    func_name = func.__qualname__.replace(".", "__")
    signature = inspect.signature(func).parameters.keys()

    var_x = []
    for x_param in ["X", "Xt", "data"]:
        if x_param in kwargs:
            var_x = kwargs[x_param]
            kwargs[x_param] = filter_func(df_)[var_x]

        if x_param in signature and not var_x:
            kwargs[x_param] = filter_func(df_)

    if "y" in kwargs:
        var_y = kwargs["y"]
        if len(var_y) == 1:
            kwargs["y"] = filter_func(df_)[var_y].values.ravel()
        else:
            kwargs["y"] = filter_func(df_)[var_y]

    res = func(**kwargs)

    if output_cols is None:
        try:
            output_cols = func.__self__.get_feature_names_out()
        except (AttributeError, ValueError) as _:
            output_cols = []

    if isinstance(res, np.ndarray) and len(index_list) == res.shape[0]:
        if len(output_cols) == 0:
            nb_cols = res.shape[-1] if res.ndim > 1 else 1
            output_cols = [func_name + "_" + str(e) for e in range(nb_cols)]
        res = np.r_["c", res]

        return (
            df_.drop(index_list)
            .pipe(
                lambda df__: pd.concat(
                    (
                        df__,
                        filter_func(df_).assign(
                            **{
                                output_cols[i]: res[:, i]
                                for i in np.arange(res.shape[-1])
                            }
                        ),
                    )
                )
            )
            .reindex(df_.index)
        )

    if datamanager:
        datamanager.logger.info("Result of %s:\n%s", func_name, i_display(res))
        datamanager.datas[
            func_name + "_var_" + str(datetime.now().strftime("%d%m%Y%H%M%S"))
        ] = res
    return df_


def pipe_leaf(
    df_: pd.DataFrame,
    func: Any,
    *args: Any,
    datamanager: Any = None,
    verbose: int = 1,
    **kwargs: Any,
) -> pd.DataFrame:
    """Wrap functions that returns nothing.

    Args:
        df_ (pd.DataFrame): DataFrame that will be piped.
        func (Any): Function to wrap.
        datamanager (DataManager): DataManager instance.
        verbose (int, optional): Level of verbose. Defaults to 1.

    Returns:
        pd.DataFrame: Returns original DataFrame to keep chaining.
    """
    if isinstance(func, str):
        func_name = func
        temp_func = getattr(df_, func)
        if inspect.ismethod(temp_func):
            res = temp_func(*args, **kwargs)
        else:
            res = getattr(df_, func)
    else:
        res = func(df_, *args, **kwargs)
        func_name = func.__qualname__.replace(".", "__")
    if datamanager:
        datamanager.logger.info("Result of %s:\n%s", func_name, i_display(res))
        datamanager.datas[
            func_name + "_var_" + str(datetime.now().strftime("%d%m%Y%H%M%S"))
        ] = res
    elif verbose:
        print(f"Result of {func_name}:")
        i_display(res, max_len=-1)
    return df_


def pipe_steps(df_: pd.DataFrame, steps: List[Tuple[Callable, Any]]) -> pd.DataFrame:
    """Wrap chain function to a DataFrame using a generator to apply multiple functions
        and theirs arguments in chain.

    Args:
        df_ (pd.DataFrame): DataFrame that will be piped.
        steps (List[Tuple[Callable, Any]): List of functions and their respective
            keyword arguments.

    Returns:
        pd.DataFrame: Returns original DataFrame to keep chaining.
    """
    return _loop_pipe(df_, (element for element in reversed(steps)))
