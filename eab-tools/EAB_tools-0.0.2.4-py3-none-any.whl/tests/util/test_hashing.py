"""Tests for hashing"""
from typing import Any

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pytest

import EAB_tools._testing as tm
from EAB_tools.util.hashing import (
    hash_df,
    hash_mpl_fig,
)


class TestHashDf:
    """Tests for EAB_tools.util.io.hashing.hash_df"""

    def test_basic_consistency(self, iris: pd.DataFrame) -> None:
        assert hash_df(iris) == hash_df(iris)

    def test_expected_iris(self, iris: pd.DataFrame) -> None:
        expected = "d7565"
        result = hash_df(df=iris, max_len=5, usedforsecurity=False)
        assert result == expected

    def test_expected_iris_columns(self, iris: pd.DataFrame) -> None:
        hash_df_kwargs: dict[str, Any] = {"max_len": 5, "usedforsecurity": False}
        expected = ["3ce8a", "7e266", "9759d", "2a060", "ea451"]
        result = [hash_df(iris[column], **hash_df_kwargs) for column in iris]
        assert expected == result

    def test_expected_iris_index(self, iris: pd.DataFrame) -> None:
        hash_df_kwargs: dict[str, Any] = {"max_len": 5, "usedforsecurity": False}
        expected = ["4f53f", "5da34", "ca488", "f1607", "5517a"]
        result = [hash_df(pd.Index(iris[column]), **hash_df_kwargs) for column in iris]

        assert expected == result

    def test_series_hash_consistency(self, series: pd.Series) -> None:
        a = hash_df(series)
        b = hash_df(series)
        assert a == b

    def test_columns_affect_hash(self, series: pd.Series) -> None:
        a = pd.DataFrame({"foo": series})
        b = pd.DataFrame({"bar": series})

        assert hash_df(a) != hash_df(b)

    def test_index_hash_consistency(self, series: pd.Series) -> None:
        index = pd.Index(series)
        assert hash_df(index) == hash_df(index)

    def test_multiindex_hash_consistency(self, multiindex: pd.MultiIndex) -> None:
        assert hash_df(multiindex) == hash_df(multiindex)

    def test_styler_consistency(self, iris: pd.DataFrame) -> None:
        iris_style = iris.style.highlight_min().highlight_max().bar()
        assert hash_df(iris, iris_style) == hash_df(iris, iris_style)

    def test_styler_affects_hash(self, iris: pd.DataFrame) -> None:
        style1 = iris.style.highlight_min()
        style2 = iris.style.highlight_max()
        assert hash_df(iris, style1) != hash_df(iris, style2)


@pytest.mark.flaky(rerun_filter=tm._is_tkinter_error, max_runs=5)
class TestHashMPLfig:
    """Tests for EAB_tools.util.io.hashing.hash_mpl_fig"""

    def test_expected_hash(self) -> None:
        expected = "c89d743"

        # Make up some data
        x = np.linspace(0, 4 * np.pi, 10**6)
        y = np.sin(x)

        # Plot made up data
        fig, ax = plt.subplots()
        ax.plot(x, y)

        kwargs: dict[str, Any] = {"max_len": 7, "usedforsecurity": False}
        assert hash_mpl_fig(fig, **kwargs) == expected

    def test_basic_consistency(self, mpl_figs_and_axes: plt.Figure) -> None:
        a = hash_mpl_fig(mpl_figs_and_axes)
        b = hash_mpl_fig(mpl_figs_and_axes)
        assert a == b

    def test_sensitivity(self, mpl_axes: plt.Axes, seed: int = 0) -> None:
        a = hash_mpl_fig(mpl_axes)

        rng = np.random.default_rng(seed=seed)
        xy = rng.random(2)
        color = rng.random(3)
        mpl_axes.scatter(*xy, c=color)
        b = hash_mpl_fig(mpl_axes)
        assert a != b
