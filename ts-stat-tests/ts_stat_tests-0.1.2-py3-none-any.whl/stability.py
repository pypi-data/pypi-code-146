from typing import Union

import numpy as np
import pandas as pd
from tsfeatures import lumpiness as ts_lumpiness
from tsfeatures import stability as ts_stability
from typeguard import typechecked


__all__ = ["stability", "is_stable", "lumpiness", "is_lumpy"]


# ------------------------------------------------------------------------------#
# Stability                                                                  ####
# ------------------------------------------------------------------------------#


@typechecked
def stability(data: Union[np.ndarray, pd.DataFrame, pd.Series], freq: int = 1) -> float:
    """
    !!! Summary
        Test for stability.

    Params:
        data (Union[np.ndarray, pd.DataFrame, pd.Series]):
            The time series.
        freq (int, optional):
            Frequency of the time series

    Returns:
        (float):
            Variance of the means of tiled windows.

    ??? Note
        For full documentation, see:

        - Python: [`tsfeatures`](https://github.com/Nixtla/tsfeatures/blob/master/tsfeatures/tsfeatures.py)
        - R: [`tsfeatures`](http://pkg.robjhyndman.com/tsfeatures/reference/lumpiness.html)

    ??? Example "Examples"
        Basic usage:
        ```python linenums="1"
        >>> from sktime.datasets import load_airline
        >>> data = load_airline()
        >>> print(stability(data))
        12702.672087912088
        ```
    """
    return ts_stability(x=data, freq=freq)["stability"]


@typechecked
def is_stable(
    data: Union[np.ndarray, pd.DataFrame, pd.Series], freq: int = 1, alpha: float = 0.5
) -> bool:
    """
    !!! Summary
        Check whether a data series is stable or not.

    Params:
        data (Union[np.ndarray, pd.DataFrame, pd.Series]):
            The time series.
        freq (int, optional):
            The frequency of the time series. Defaults to `1`.
        alpha (float, optional):
            The value, above which, the data will be stable. Defaults to `0.5`.

    Returns:
        (bool):
            A confirmaiont of whether or not the data is stable.

    ??? Note
        For full documentation, see:

        - Python: [`tsfeatures`](https://github.com/Nixtla/tsfeatures/blob/master/tsfeatures/tsfeatures.py)
        - R: [`tsfeatures`](http://pkg.robjhyndman.com/tsfeatures/reference/lumpiness.html)

    ??? Example "Examples"
        Basic usage:
        ```python linenums="1"
        >>> from sktime.datasets import load_airline
        >>> data = load_airline()
        >>> print(is_stable(data))
        True
        ```
    """
    return True if stability(data=data, freq=freq) > alpha else False


# ------------------------------------------------------------------------------#
# Lumpiness                                                                  ####
# ------------------------------------------------------------------------------#


@typechecked
def lumpiness(data: Union[np.ndarray, pd.DataFrame, pd.Series], freq: int = 1) -> float:
    """
    !!! Summary
        Test for lumpiness.

    Params:
        data (Union[np.ndarray, pd.DataFrame, pd.Series]):
            The time series.
        freq (int, optional):
            Frequency of the time series

    Returns:
        (float):
            Variance of the means of tiled windows.

    ??? Note
        For full documentation, see:

        - Python: [`tsfeatures`](https://github.com/Nixtla/tsfeatures/blob/master/tsfeatures/tsfeatures.py)
        - R: [`tsfeatures`](http://pkg.robjhyndman.com/tsfeatures/reference/lumpiness.html)

    ??? Example "Examples"
        Basic usage:
        ```python linenums="1"
        >>> from sktime.datasets import load_airline
        >>> data = load_airline()
        >>> print(lumpiness(data))
        5558930.856730431
        ```
    """
    return ts_lumpiness(x=data, freq=freq)["lumpiness"]


@typechecked
def is_lumpy(
    data: Union[np.ndarray, pd.DataFrame, pd.Series], freq: int = 1, alpha: float = 0.5
) -> bool:
    """
    !!! Summary
        Check whether a data series is lumpy or not.

    Params:
        data (Union[np.ndarray, pd.DataFrame, pd.Series]):
            The time series.
        freq (int, optional):
            The frequency of the time series. Defaults to `1`.
        alpha (float, optional):
            The value, above which, the data will be stable. Defaults to `0.5`.

    Returns:
        (bool):
            A confirmaiont of whether or not the data is lumpy.

    ??? Note
        For full documentation, see:

        - Python: [`tsfeatures`](https://github.com/Nixtla/tsfeatures/blob/master/tsfeatures/tsfeatures.py)
        - R: [`tsfeatures`](http://pkg.robjhyndman.com/tsfeatures/reference/lumpiness.html)

    ??? Example "Examples"
        Basic usage:
        ```python linenums="1"
        >>> from sktime.datasets import load_airline
        >>> data = load_airline()
        >>> print(is_lumpy(data))
        True
        ```
    """
    return True if lumpiness(data=data, freq=freq) > alpha else False
