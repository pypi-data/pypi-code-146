from collections.abc import (
    Iterable,
    Iterator,
)
import itertools
import os
from pathlib import Path
from typing import (
    Any,
    Callable,
    Literal,
    Union,
)

from _pytest.fixtures import SubRequest as PytestFixtureRequest
import dateutil.tz
import matplotlib.pyplot as plt
import numpy as np
import numpy.typing as npt
import pandas as pd
from pandas._testing import makeDateIndex
import pytest

Numeric = np.number[Any]

iris_df: pd.DataFrame = pd.read_csv(Path(__file__).parent / "tests/io/data/iris.csv")


@pytest.fixture
def iris() -> pd.DataFrame:
    """The iris dataset as a pandas DataFrame."""
    return iris_df


@pytest.fixture(params=iris_df.columns)
def iris_cols(request: PytestFixtureRequest) -> pd.Series:
    """Return iris dataframe columns, one after the next"""
    return iris_df[request.param]


@pytest.fixture(
    params=[str, pytest.param(lambda col_name: pd.Index([col_name]), id="pd.Index")]
)
def iris_single_col_subset(
    iris_cols: pd.Series, request: PytestFixtureRequest
) -> Union[str, pd.Index]:
    """Return a col name as a str or pd.Index"""
    func = request.param
    col = iris_cols.name
    return func(col)


@pytest.fixture(
    params=[
        pytest.param(pd.Series([1, 2, 3] * 3, dtype="int32"), id="int32series"),
        pytest.param(
            pd.Series([None, 2.5, 3.5] * 3, dtype="float32"), id="float32series"
        ),
        pytest.param(
            pd.Series(["a", "b", "c"] * 3, dtype="category"), id="category_series"
        ),
        pytest.param(pd.Series(["d", "e", "f"] * 3), id="object_series"),
        pytest.param(pd.Series([True, False, True] * 3), id="bool_series"),
        pytest.param(
            pd.Series(pd.date_range("20130101", periods=9)), id="datetime_series"
        ),
        pytest.param(
            pd.Series(pd.date_range("20130101", periods=9, tz="US/Eastern")),
            id="datetime_tz_series",
        ),
        pytest.param(
            pd.Series(pd.timedelta_range("2000", periods=9)), id="timedelta_series"
        ),
    ]
)
def series(request: PytestFixtureRequest) -> pd.Series:
    """Return several series with unique dtypes"""
    # Fixture borrowed from pandas from
    # https://github.com/pandas-dev/pandas/blob/5b2fb093f6abd6f5022fe5459af8327c216c5808/pandas/tests/util/test_hashing.py
    return request.param


pairs = list(itertools.permutations(iris_df.columns, 2))


@pytest.fixture(params=pairs, ids=list(map(str, pairs)))
def multiindex(iris: pd.DataFrame, request: PytestFixtureRequest) -> pd.MultiIndex:
    """Return MultiIndexes created from pairs of iris cols"""
    a_col, b_col = request.param
    a, b = iris[a_col], iris[b_col]
    return pd.MultiIndex.from_arrays([a, b])


@pytest.fixture(
    params=[
        np.sin,  # any -> float
        pytest.param(lambda arr: np.exp(-arr), id="exp(-x)"),  # any -> float
        pytest.param(
            lambda x: x**2, id="lambda squared"
        ),  # int -> int and float -> float
        pytest.param(lambda arr: np.rint(arr).astype(int), id="rint"),  # any -> int
    ],
    name="func",
)
def plot_func(
    request: PytestFixtureRequest,
) -> Callable[[npt.ArrayLike], npt.NDArray[Numeric]]:
    """A variety of mathematical funcs callable on numeric numpy ndarrays"""
    return request.param


@pytest.fixture(
    params=[
        np.linspace(0, 10**-5, dtype=float),
        np.linspace(0, 499, num=500, dtype="int32"),
        np.linspace(0, 2**33, 2**10 + 1, dtype="int64"),
    ],
    ids=lambda arr: str(arr.dtype),
)
def x_values(request: PytestFixtureRequest) -> npt.NDArray[Numeric]:
    """func inputs of different dtypes"""
    return request.param


@pytest.fixture(params=["fig", "ax"])
def _fig_or_ax(request: PytestFixtureRequest) -> Literal["fig", "ax"]:
    """Either returns 'fig' or 'ax'"""
    return request.param


@pytest.fixture
def mpl_plots(
    func: Callable[[npt.ArrayLike], npt.NDArray[Numeric]],
    x_values: npt.NDArray[Numeric],
) -> Iterable[dict[str, Union[plt.Figure, plt.Axes]]]:
    """Returns dict of {fix, ax}, for various funcs and domains"""
    x = x_values
    y = func(x)
    fig, ax = plt.subplots()
    ax.plot(x, y)

    yield {"fig": fig, "ax": ax}
    plt.close(fig)


@pytest.fixture
def mpl_axes(mpl_plots: dict[str, Union[plt.Figure, plt.Axes]]) -> plt.Axes:
    """Returns a variety of `plt.Axes` objects"""
    return mpl_plots["ax"]


@pytest.fixture
def mpl_figs(mpl_plots: dict[str, Union[plt.Figure, plt.Axes]]) -> plt.Figure:
    """Returns a variety of `plt.Figure` objects"""
    return mpl_plots["fig"]


@pytest.fixture
def mpl_figs_and_axes(
    mpl_plots: dict[str, Union[plt.Figure, plt.Axes]], _fig_or_ax: Literal["fig", "ax"]
) -> Union[plt.Figure, plt.Axes]:
    """Returns either the figure or the axis of various plots"""
    return mpl_plots[_fig_or_ax]


today = pd.Timestamp.today(dateutil.tz.tzlocal())
strftime_codes = [
    "%B %d, %Y",  # June 12, 2022
    "%Y-%m-%d",  # 2022-06-12
    "%B %e, %Y",  # June 12, 2022
    "%a, %b %e",  # Sun, Jun 12
    "%e %b %Y",  # 12 Jun 2022
    "%A, %B %e, %Y",  # Sunday, June 12, 2022
    "%H:%M:%S",  # 16:51:45
    "%Y-%m-%dT%H:%M:%S.%f%z",  # 2022-06-12T16:51:45.576846-0500
    "%I:%M %p",  # 04:51 PM
]


@pytest.fixture(
    params=iter(strftime_codes),
    ids=[f"{today:{strftime}}" for strftime in strftime_codes],
)  # noqa
def strftime(request: PytestFixtureRequest) -> str:
    """Various different strftime format codes"""
    return request.param


@pytest.fixture(
    params=[
        pd.to_timedelta(0),
        pd.Timedelta(hours=15),
        pd.DataFrame(
            (pd.to_timedelta(row, unit="hours") for row in np.random.rand(10, 3) * 24),
            columns=list("ABC"),
        ),
    ]
)
def datetime_df(request: PytestFixtureRequest) -> pd.DataFrame:
    """DataFrame with datetime data, integer index, and str column names.
                   A          B          C
    0 2000-01-03 2000-01-02 2000-12-31
    1 2000-01-04 2000-01-09 2001-12-31
    2 2000-01-05 2000-01-16 2002-12-31
    3 2000-01-06 2000-01-23 2003-12-31
    4 2000-01-07 2000-01-30 2004-12-31
    5 2000-01-10 2000-02-06 2005-12-31
    6 2000-01-11 2000-02-13 2006-12-31
    7 2000-01-12 2000-02-20 2007-12-31
    8 2000-01-13 2000-02-27 2008-12-31
    9 2000-01-14 2000-03-05 2009-12-31"""
    df = pd.DataFrame(
        {
            "A": makeDateIndex(freq="b"),
            "B": makeDateIndex(freq="w"),
            "C": makeDateIndex(freq="y"),
        }
    )
    time_offset = request.param
    return df + time_offset


@pytest.fixture
def datetime_and_float_df(datetime_df: pd.DataFrame) -> pd.DataFrame:
    """datetime_df with additional columns of random positive and negative floats"""
    datetime_df[list("DE")] = np.random.uniform(-1, 1, (10, 2))
    return datetime_df


@pytest.fixture(autouse=True)
def _docstring_tmp_path(request: PytestFixtureRequest) -> Iterator[None]:
    # Almost completely adapted from a kind soul at https://stackoverflow.com/a/46991331
    # Trigger ONLY for the doctests.
    doctest_plugin = request.config.pluginmanager.getplugin("doctest")
    if isinstance(request.node, doctest_plugin.DoctestItem):
        # Get the fixture dynamically by its name.
        tmp_path: Path = request.getfixturevalue("tmp_path")
        # Chdir only for the duration of the test.
        og_dir = os.getcwd()
        try:
            os.chdir(tmp_path)
            yield
        finally:
            os.chdir(og_dir)
    else:
        # For normal tests, we have to yield, since this is a yield-fixture.
        yield
