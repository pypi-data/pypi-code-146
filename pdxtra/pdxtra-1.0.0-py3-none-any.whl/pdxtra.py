"""
PDXtra is a data analysis library built on top of Pandas and geared toward
time-series data analysis. The library offers subclasses of traditional
Pandas ``Series`` and ``DataFrame`` objects which provide additional
convenience methods for querying and manipulating data while retaining all
of the functionality of the original Pandas API. Additionally, the library also
provides ``TimeSeries`` and ``TimeSeriesDataFrame`` subclasses which are
specifically designed to be used for time-series and financial data analysis.

This distribution has been developed and tested on a standalone Python build
and could--under rare circumstances--exibit unexpected behavior on standard
CPython. Although no differences between the execution of code in the
standalone build and normal CPython have been found during the process of
development, I nevertheless wish to provide fair warning.
"""
from __future__ import annotations

__author__ = "Ben Ohling"
__copyright__ = f"Copyright (C) 2022, {__author__}"
__version__ = "1.0.0"

import numpy as np
import pandas as pd

from contextlib import contextmanager
from datetime import date, datetime, timedelta
from functools import wraps
from typing import Any, Callable, Optional, Sequence, Union

from numpy.typing import NDArray

# Copyright 2022, Ben Ohling
# Licensed under GNU General Public License


class DowncastTypeError(TypeError):
    """Warn user that ``downcast_dataframe`` cannot be used on a ``Series``."""

    def __init__(self):
        self.message = (
            "using 'downcast_dataframe' to downcast an individual series "
            "would be inefficient. Use 'pd.to_numeric' instead."
        )
        super().__init__(self.message)


def downcast_dataframe(
        df: DataFrame,
        integers: bool = True,
        floats: bool = True,
        ) -> DataFrame:
    """
    Downcast all numeric columns of the dataframe while retaining the sign
    of the values. The precision warnings associated with ``pandas.to_numeric``
    also apply here.

    Parameters
    ----------
    df : `Dataframe`
        The dataframe to be downcast.
    integers : `bool`, default `True`
        Whether or not to downcast integer columns.
    floats : `bool`, default `True`
        Whether or not to downcast floating-point columns.

    .. note::
       Due to the way in which `pandas.select_dtypes` selects columns,
       nullable Pandas types will automatically be downcast and cannot be
       selectively excluded when calling the function. Instead, exclude
       the nullable type columns and downcast the view or copy.

    Returns
    -------
    A Pandas ``DataFrame``.

    Raises
    ------
    ``DowncastTypeError``:
        When attempting to downcast an individual ``Series``.

    Examples
    ^^^^^^^^
    Downcast a dataframe containing an integer and a float column.

    >>> import pdxtra as pdx
    >>> df = pdx.DataFrame({"a": [1, 2, 3], "b": [1.0, 2.0, 3.0]})
    >>> df.dtypes
    a      int64
    b    float64
    dtype: object
    >>> df = pdx.downcast_dataframe(df)
    >>> df.dtypes
    a       int8
    b    float32
    dtype: object

    Downcast only the integer columns.

    >>> df = pdx.DataFrame({"a": [1, 2, 3], "b": [1.0, 2.0, 3.0]})
    >>> df.dtypes
    a      int64
    b    float64
    dtype: object
    >>> df = pdx.downcast_dataframe(df, floats=False)
    >>> df.dtypes
    a       int8
    b    float64
    dtype: object
    """
    if isinstance(df, (pd.Series, Series)):
        raise DowncastTypeError

    # Since indexing multiple columns produces a dataframe with a different
    # ID from the original, we must copy the dataframe in order for values
    # to be updated reliably for both the original dataframe and its
    # views/copies. Attempting to mutate the original dataframe here is bad.
    # Don't do it!
    df = df.copy()
    if integers:
        icols = df.select_dtypes(include="integer").columns
        if not icols.empty:
            df[icols] = df[icols].apply(
                pd.to_numeric,
                downcast="integer",
                raw=True,
            )

    if floats:
        fcols = df.select_dtypes(include="float").columns
        if not fcols.empty:
            df[fcols] = df[fcols].apply(
                pd.to_numeric,
                downcast="float",
                raw=True,
            )

    return df


def nearest_to(
        series: pd.Series,
        pivot: Union[int, float, date, datetime],
        tolerance: Union[int, float, timedelta] = 5,
        lookback: bool = True,
        float_method: str = "fuzzy",
        ) -> Any:
    """
    Sort then search the series for a value which is nearest to the pivot
    value. If an exact match is found, then that match will be returned. All
    values in the series must support subtraction between themselves and the
    other values of the series.

    Can look forwards and backwards for matches, but does so hierarchically.
    For instance, a forward lookup will only return the forward value if the
    distance between it and the pivot value is less than the distance
    between any of the lower values and the pivot value. The same logic holds
    true for lookbacks. Any value above or below the pivot value, whose
    distance from the pivot is greater than the absolute value of the pivot
    plus the tolerance, will be excluded from the search.

    .. note::
       This function can be called directly on a `Series` object.

    Parameters
    ----------
    series : `Series`
        The Pandas series to be searched. When called as a method from the
        `Series` class, this argument is assigned to the class instance.
    pivot : {`int`, `float`, `date`, `datetime`}
        The value on which to match. The search window (as defined by the
        tolerance) "pivots" around this value.
    tolerance : {`int`, `float`, `timedelta`}, default 5
        The maximum distance to search on either side of the pivot. If
        searching a series containing `date` or `datetime` objects, the user is
        responsible for providing the appropriate `timedelta` for computing
        differences between the series values and the pivot value.
    lookback : `bool`, default `True`
        Whether or not to prioritize looking backwards vs. looking forwards
        along the sorted values of the series.
    float_method : `str` {`fuzzy`, `precise`}, default `fuzzy`
        Method for comparing floats when determining whether or not the
        difference between the pivot and a given value exceeds the bounds
        set by the tolerance.

        .. warning::
           Using precise will only increase the likelihood that the value
           returned falls within bounds. Neither of the two methods,
           fuzzy or precise, can guarantee perfect comparison of
           floating-point numbers. See the documentation for ``numpy.isclose``
           for additional information on how this method compares
           floating-point numbers when precise is used. For an array of
           floating-point numbers significantly smaller than zero, precise
           may produce false-positive comparisons. For columns which do not
           contain floating-point numbers, the default (fuzzy) should always be
           used.

    Returns
    -------
    Either a value from the series or ``None`` if no match is found.

    Raises
    ------
    ``TypeError``:
        One or more of the values does not support subtraction between itself
        and the other values in the series, or a comparison between differences
        and the tolerance is considered ambiguous.
    ``ValueError``:
        The 'float_method' argument which was passed to the method is not
        one of the accepted strings.

    Examples
    ^^^^^^^^
    Get the value from the list which is nearest to seven.

    >>> import pdxtra as pdx
    >>> values = pd.Series([1, 2, 3, 4, 8, 9])
    >>> pdx.nearest_to(values, 7)
    8

    Get the value from the list which is nearest to three and use default
    ``lookback=True`` for tie breaking.

    >>> values = pd.Series([1, 2, 4, 5])
    >>> pdx.nearest_to(values, 3)
    2

    Get the value from the list which is nearst to three and look forward to
    break the tie.

    >>> pdx.nearest_to(values, 3, lookback=False)
    4
    """
    values = series.values
    if float_method == "fuzzy":
        filtered = np.sort(
            values[np.abs(values - pivot) <= tolerance],
            kind="mergesort",
        )
    elif float_method == "precise":
        diffs = np.abs(values - pivot)
        filtered = np.sort(
            values[np.nonzero(
                (diffs < tolerance) | (np.isclose(diffs, tolerance))
            )]
        )
    else:
        if not isinstance(float_method, str):
            raise TypeError(
                f"'float_method' must be of type 'str'; "
                f"got {type(float_method)} instead."
            )
        else:
            raise ValueError(
                f"'the value of float_method' must be one of: "
                f"'fuzzy', 'precise'; got {float_method} instead."
            )

    key = lambda x: np.abs(x - pivot)
    if lookback:
        neighbor = min(filtered, key=key, default=None)
    else:
        # Since the `min` function always selects the first of multiple
        # identical values, we need to reverse the list when looking
        # forward because we want the last of the identical differences
        # to come first.
        neighbor = min(filtered[::-1], key=key, default=None)

    return neighbor


def coerce_to_numpy_array(arr: Union[Sequence, NDArray, Series]) -> NDArray:
    """Coerce a non-numpy array to a numpy array."""
    if not isinstance(arr, np.ndarray):
        try:
            # Assume the sequence is a Pandas `Series`
            arr = arr.values
        except AttributeError:
            # Oops, it's not a Pandas `Series`; cast directly instead
            arr = np.array(arr)

    return arr


def _coerce_arrays(func: Callable) -> Callable:
    """
    Takes a function whose only arguments are sequences and coerces each of
    those arguments to ``numpy.ndarrays`` before calling the function.
    """

    @wraps(func)
    def wrapper(*args) -> Callable:
        args = map(coerce_to_numpy_array, args)
        return func(*args)
    return wrapper


def _find_intersects(x: NDArray, y1: NDArray, y2: NDArray) -> NDArray:
    """
    Returns the (x,y) coordinates for all points of intersection of two
    finite curves. Each array should represent the Y values of some curve
    whose X values match the values of the 'x' parameter.
    """

    ydiff = (y1 - y2)
    # Boolean mask of all indicies where intersection occurs
    mask = np.nonzero(np.abs(np.diff(np.sign(ydiff))))
    # Boolean indexed array containing the difference of all consecutive
    # indicies whose intervals they represent contain a point of intersection
    # between the two curves.
    xdiff = np.diff(x)[mask]
    # Interpolation method used to find all x-coordinates for each realized
    # point of intersection.
    # See question https://bit.ly/3WpXZy0 on StackOverflow
    x_coords = x[:-1][mask] + (
        xdiff / (np.abs(ydiff[1:][mask] / ydiff[:-1]) + 1)
    )
    x_coords = x_coords[~np.isnan(x_coords)]
    # Derive the y-coordinates from the x-coordinates using simple, linear
    # interpolation.
    y_coords = np.interp(x_coords, x, y2)
    y_coords = y_coords[~np.isnan(y_coords)]
    return np.array((x_coords, y_coords))


find_intersects = _coerce_arrays(_find_intersects)


def _find_near_intersects(x: NDArray, y1: NDArray, y2: NDArray) -> NDArray:
    """
    Returns the (x,y) coordinates for all points that preceed a point of
    intersection of two finite curves. Each array should represent the Y
    values of some curve whose X values match the values of the 'x' parameter.
    """
    mask = np.argwhere(np.nan_to_num(np.diff(np.sign(y1 - y2)))).flatten()
    x_coords = x[mask]
    y_coords = y1[mask]
    return x_coords, y_coords


find_near_intersects = _coerce_arrays(_find_near_intersects)


def normalize(series, multiplier: Union[int, float] = 1.5):
    """
    Returns a series with outliers removed via the IQR method.

    .. note::
       This function can be called directly on a ``DataFrame`` object.

    Parameters
    ----------
    multiplier : {`int`, `float`} default 1.5
        The value by which to multiply (extend) upper and lower bounds.

    Returns
    -------
    A 1-d Numpy array.

    Examples
    ^^^^^^^^
    >>> import pdxtra as pdx
    >>> s = Series([-30, 1, 2, 3, 30])
    >>> s = normalize(s)
    >>> s
    array([1, 2, 3])
    """
    values = series.values
    q1, q3 = np.percentile(values, [25, 75])
    lim = q3 - q1 * multiplier  # Inter-quartile range

    lower = q1 - lim
    upper = q3 + lim

    normal = values[np.nonzero((values > lower) & (values < upper))]

    # TODO REMINDER: Add the formula for computing the upper and lower
    # bounds using LaTex and add the option to replace removed values with
    # `np.nan` in order to return an array equal to the length of `self`.
    return normal


class Series(pd.Series):

    def __init__(self, *args, **kwargs) -> None:
        super(Series, self).__init__(*args, **kwargs)

    @property
    def _constructor(self) -> Callable[..., Series]:
        return Series

    nearest_to = nearest_to
    normalize = normalize

    @property
    def linearize(self) -> NDArray:
        """Returns the linear regression of a ``Series``."""
        z = np.polyfit(self.index, self, 1) # The (x,y) coordinates and degree
        # Polynomial method for converting an array of coefficients to
        # polynomial expressions.
        p = np.poly1d(z)
        # Evaluate the expressions at each of the indicies
        linreg = p(self.index)
        return linreg

    def true_ema(self, span: int) -> pd.Series:
        """
        Calculate the true N-day, exponential moving average of the ``Series``.

        Calculations for exponential moving averages in Pandas start on the
        last position of the span which means that in order for a moving
        average with a span of N days to be a true N-day moving average, we
        need to add one to the minimum number of periods. This method produces
        an exponential moving average where 'min_periods' for the exponential
        moving window is always 'span + 1'.

        Parameters
        ----------
        span : `int`
            From the Pandas documentation: "Specify decay in terms of span."
            See Pandas documentation on ``pandas.ewm`` for a full explanation.

        Returns
        -------
        A subclass of Pandas ``ExponentialMovingWindow``.
        """
        return self.ewm(span=span, min_periods=span + 1).mean()


class DataFrame(pd.DataFrame):

    def __init__(self, *args, **kwargs) -> None:
        super(DataFrame, self).__init__(*args, **kwargs)

    @property
    def _constructor(self) -> Callable[..., DataFrame]:
        return DataFrame

    _constructor_sliced = Series

    @contextmanager
    def set_temp_index(self, column_name: str) -> None:
        """
        Context manager for temporarily switching the index column. The index
        column is automatically reverted back when the context manager exits.

        Parameters
        ----------
        column_name : `str`
            The name of the column to set as the index column while inside
            the scope of the context manager.
        """
        column_idx = [x for x in self.columns].index(column_name)
        try:
            self.set_index(column_name, inplace=True)
            yield
        finally:
            self.reset_index(inplace=True)
            self.insert(column_idx, column_name, self.pop(column_name))

    def xlookup(
            self,
            row_idx: Union[int, float, complex, date, datetime],
            column_name: str,
            nearest_match: bool = False,
            tolerance: Union[int, timedelta] = 5,
            lookback: bool = True,
            ) -> Any:
        """
        Perform an Excel-style 'xlookup' by extracting the value(s) at the
        intersection of a set of (x,y) coordinates, where the Y coordinate
        is an index value and the X coordinate is a column name. Can perform
        nearest match on numerical and date indexes.

        Parameters
        ----------
        row_idx : {`int`, `float`, `date`, `datetime`}
            The index value specifying which row is to be searched. When using
            'nearest_match' this value becomes the pivot value supplied to the
            'nearest_to' function.
        column_name : `str`
            The name of the column from which to extract the value.
        nearest_match : `bool`, default `False`
            If true, use the 'nearest_to' function to find the value of the
            index column which is closest to the 'row_idx' value.
        tolerance : `int`, default 5
            The maximum distance to search on either side of the 'row_idx'
            value when performing nearest match. If searching a series
            containing ``date`` or ``datetime`` objects, the user is
            responsible for providing the appropriate ``timedelta`` for
            computing differences between the index values and the value
            assigned to 'row_idx'. This argument is ignored when
            'nearest_match' is false.
        lookback : `bool`, default `True`
            Whether or not to prioritize looking back vs. looking forwards
            along the sorted values of the ``Series`` when performing nearest
            match. This argument is ignored when 'nearest_match' is false.

        Returns
        -------
        A value from the column being indexed, or ``None`` if no value is
        returned on nearest match.

        Raises
        ------
        - ``KeyError`` :
            When the dataframe cannot be indexed using the coordinates
            provided.
        - ``TypeError`` :
            When nearest match is performed on a series which contains values
            that do not support subraction between themselves and the other
            values contained in the `Series`, or when a comparison between
            differences and the `tolerance` is considered ambiguous.

        Examples
        ^^^^^^^^
        Find the value in column "integers" at index 2.

        >>> import pdxtra as pdx
        >>> df = pdx.DataFrame({"integers": [1, 2, 3, 4, 5]})
        >>> df.xlookup(2, "integers")
        3

        Find the value in column "integers" where the index equals "d".

        >>> df.index = ["a", "b", "c", "d", "e"]
        >>> df.xlookup("d", "integers")
        4

        Find the value in column "integers" where the index is nearest to 3.

        >>> df.index = [2, 4, 6, 8, 10]
        >>> df.xlookup(3, "integers", nearest_match=True)
        1

        Find the value in column "integers" where the index is nearest to 3,
        but look forwards instead of backwards.

        >>> df.xlookup(3, "integers", nearest_match=True, lookback=False)
        2
        """
        if nearest_match is True:
            row_idx = nearest_to(self.index, row_idx, tolerance, lookback)

        # Although the `nearest_to` function may return none, Pandas dataframe
        # indexes cannot contain Python `NontType` values, so we're
        # safe to attempt indexing the dataframe, even when 'None' is returned.
        # Attempting to index with `.at` using 'None' for the index value
        # will result in a `KeyError` being raised, which is the desired
        # behavior in this case.
        value = self.at[row_idx, column_name]
        return value

    def vlookup(
            self,
            values: Sequence,
            column: str,
            method: Optional[str] = None,
            tolerance: Optional[
                Union[int, float, date, datetime, type(None)]
            ] = None,
            ) -> Series:
        """
        Performs an Excel-like, veritcal lookup. In this case, the "v" in the
        function name has a double meaning. It stands for both "vertical"
        and "vector", because unlike the typical vertical lookup in Excel,
        the function returns a vector of values (``numpy.array``) from the
        specified column, rather than a scalar. Can perform nearest match on
        the index column.

        Parameters
        ----------
        values : `Sequence`
            A sequence of values to search for in the index column.
        column : `str`
            The column name from which we wish to extract values whose indicies
            match the indicies found in the index column.
        method : {`None`, `str`}, default `None`
            Method used to determine whether or not a value is considered a
            match or near-match. From the Pandas documentation:

             - [``None`` (default)]: exact matches only.
             - pad / ffill: find the previous index value if no exact match.
             - backfill / bfill: use the next index value if no exact match.
             - nearest: use the nearest index value if no exact match. Tied
               distances are broken by preferring the larger index value.
        tolerance : {`numeric`, `date`, `datetime`, `None`}, default `None`
            The maximum distance to search on either side of the index value
            when performing nearest match. If searching a series containing
            ``date`` or ``datetime`` objects, the user is responsible for
            providing the appropriate ``timedelta`` for computing differences
            between the index values and the values supplied in the function
            call. This argument is ignored when the method is ``None``. See
            ``pandas.Index.get_indexer`` for further explanation.

        Returns
        -------
        A 1-d Numpy array, which can be empty if no values are found.
        """
        if method is None:
            lookup = self.iloc[values][column]
        else:
            mask = self.index.get_indexer(
                values,
                tolerance=tolerance,
                method=method,
            )
            lookup = self.iloc[mask[np.nonzero(mask >= 0)]][column]

        return lookup


class TimeSeries(Series):

    def __init__(self, *args, **kwargs) -> None:
        super(TimeSeries, self).__init__(*args, **kwargs)

    @property
    def _constructor(self) -> Callable[..., TimeSeries]:
        return TimeSeries

    def rsi(self, span: int = 14) -> Series:
        """
        Converts the ``Series`` to relative strength index.

        Parameters
        ----------
        span : `int`
            The length of the rolling window across the ``Series``.

        Returns
        -------
        A PDXtra ``Series`` object.
        """
        close_delta = self.diff()
        up = close_delta.clip(lower=0)
        down = -1 * close_delta.clip(upper=0)

        return up.true_ema(span) / down.true_ema(span)

    def macd(self, short_span: int = 12, long_span: int = 26) -> Series:
        """
        Converts the ``Series`` to moving average convergence-divergence.

        Parameters
        ----------
        short_span : `int`
            The length of the short rolling window.
        long_span : `int`
            The length of the long rolling window.

        Returns
        -------
        A PDXtra ``TimeSeries`` object.
        """
        return self.true_ema(short_span) - self.true_ema(long_span)

    def intersects(self, other: Sequence) -> NDArray:
        """
        Returns the (x,y) coordinates for each point of intersection between
        the ``Series`` and the sequence supplied to the method. The coordinate
        vectors are returned as a 2-d Numpy array where index [0, :] contains
        the X values and index [1, :] contains the Y values for all points
        of intersection. Each pair for an array of N elements having index
        positions "i" is equal to the index [:, i].

        Parameters
        ----------
        other : `Sequence`
            A sequence of values forming some finite curve that is expected to
            intersect with the curve represented by the series. This sequence
            must be the same length as the series itself.

        Returns
        -------
        A 2-d Numpy array.
        """
        return find_intersects(self.index.values, self.values, other)

    def near_intersects(self, other: Sequence) -> NDArray:
        """
        Returns the (x,y) coordinates for each point of intersection between
        the series and the sequence supplied to the method. The coordinate
        vectors are returned as a 2-d Numpy array where index [0, :] contains
        the X values and index [1, :] contains the Y values for all points
        of intersection. Each coordinate pair for an array of N elements
        having index positions "i" is equal to the index [:, i]. Every pair
        represents the nearest non-interpolated coordinates that preceed a
        point of intersection.

        Parameters
        ----------
        other : `Sequence`
            A sequence of values forming some finite curve that is expected to
            intersect with the curve represented by the series. This sequence
            must be the same length as the series itself.

        Returns
        -------
        A 2-d Numpy array.
        """
        return find_near_intersects(self.index.values, self.values, other)


class TimeSeriesDataFrame(DataFrame):

    def __init__(self, *args, **kwargs) -> None:
        super(TimeSeriesDataFrame, self).__init__(*args, **kwargs)

    @property
    def _constructor(self) -> Callable[..., TimeSeriesDataFrame]:
        return TimeSeriesDataFrame

    _constructor_sliced = TimeSeries

    def obv(self, close: str, volume: str) -> TimeSeries:
        """
        Calculates the on-balance volume of the close and volume columns
        specified. Specifically designed for financial, time-series data
        analysis.

        Parameters
        ----------
        close : `str`
            Name of the column which represents closing prices.
        volume : `str`
            Name of the column which represents the trading volume.

        Returns
        -------
        A PDXtra ``TimeSeries`` object.
        """
        obv_arr = (
            np.sign(self[close].diff()) * self[volume].values
        ).fillna(0).cumsum()
        return obv_arr

    def intersects(
            self,
            column_1: str,
            column_2: str,
            ) -> tuple[NDArray, NDArray]:
        """
        Returns the (x,y) coordinates for each point of intersection of two
        finite curves as a 2-d array where index [0, :] contains the X values
        and index [1, :] contains the Y values for all points of intersection.
        Each pair for an array of N elements having index positions "i" is
        equal to the index [:, i].

        Parameters
        ----------
        column_1 : `str`
            The name of the first ``Series`` representing a finite curve.
        column_2 : `str`
            The name of the second ``Series`` whose curve is expected to
            intersect with the first.

        Returns
        -------
        A 2-d Numpy array.
        """
        return _find_intersects(
            self.index.values,
            self[column_1].values,
            self[column_2].values,
        )

    def near_intersects(
            self,
            column_1: str,
            column_2: str,
            ) -> tuple[NDArray, NDArray]:
        """
        Returns the (x,y) coordinates for each point of intersection of two
        finite curves as a 2-d Numpy array where index [0, :] contains the X
        values and index [1, :] contains the Y values for all points of
        intersection. Each coordinate pair for an array of N elements having
        index positions "i" is equal to the index [:, i]. Every pair represents
        the nearest non-interpolated coordinates that preceed a point of
        intersection.

        Parameters
        ----------
        column_1 : `str`
            The name of the first ``Series`` representing a finite curve.
        column_2 : `str`
            The name of the second ``Series`` whose curve is expected to
            intersect with first.

        Returns
        -------
        A 2-d Numpy array.
        """
        return _find_near_intersects(
            self.index.values,
            self[column_1].values,
            self[column_2].values,
        )
