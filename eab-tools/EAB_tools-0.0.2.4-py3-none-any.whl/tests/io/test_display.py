# pylint: disable=C0114, C0116
from collections.abc import Sequence
from contextlib import nullcontext as does_not_raise
import itertools
import os
from pathlib import Path
import re
from typing import (
    Any,
    ContextManager,
    Optional,
    Union,
)

from matplotlib import pyplot as plt
import pandas as pd
import pytest

import EAB_tools as eab
from EAB_tools import (
    display_and_save_df,
    display_and_save_fig,
    sanitize_filename,
)
import EAB_tools._testing as tm

try:
    import openpyxl as _openpyxl  # noqa: F401 # 'openpyxl ... imported but unused

    _HAS_OPENPYXL = True
except ImportError:
    _HAS_OPENPYXL = False


@pytest.fixture(autouse=True)
def _init(tmp_path: Path) -> None:
    os.chdir(tmp_path)


SaveImageTrueParam = pytest.param(True, marks=pytest.mark.slow)
SaveExcelTrueParam = pytest.param(
    True, marks=pytest.mark.skipif(not _HAS_OPENPYXL, reason="openpyxl required")
)


@pytest.mark.parametrize(
    "save_image",
    [SaveImageTrueParam, False],
    ids="save_image={}".format,
)
@pytest.mark.parametrize(
    "save_excel",
    [SaveExcelTrueParam, False],
    ids="save_excel={}".format,
)
class TestDisplayAndSaveDf:
    def test_doesnt_fail(
        self, iris: pd.DataFrame, save_image: bool, save_excel: bool
    ) -> None:
        display_and_save_df(iris, save_image=save_image, save_excel=save_excel)

    def test_series_doesnt_fail(
        self, series: pd.Series, save_image: bool, save_excel: bool
    ) -> None:
        display_and_save_df(series, save_image=save_image, save_excel=save_excel)

    def test_multiindex_index(
        self, iris: pd.DataFrame, save_image: bool, save_excel: bool
    ) -> None:
        iris_mi = iris.set_index("Name", append=True)
        display_and_save_df(iris_mi, save_image=save_image, save_excel=save_excel)
        display_and_save_df(iris_mi.T, save_image=save_image, save_excel=save_excel)

    @staticmethod
    def col_name_from_iris_single_col_subset(col_name: Union[str, pd.Index]) -> str:
        return col_name if isinstance(col_name, str) else col_name[0]

    @pytest.mark.parametrize(
        "kwargs",
        [
            pytest.param(
                {
                    "format": "{:,}",
                    "display_and_save_kw": "thousands_format_subset",
                    "need_large_numbers": True,
                },
                id="thousands subset",
            ),
            pytest.param(
                {
                    "format": "{:.1%}",
                    "display_and_save_kw": "percentage_format_subset",
                    "percentage_format_precision": 1,
                },
                id="percentage subset",
            ),
            pytest.param(
                {
                    "format": "{:.0f}",
                    "display_and_save_kw": "float_format_subset",
                    "float_format_precision": 0,
                },
                id="float.0f",
            ),
            pytest.param(
                {
                    "format": "{:.1f}",
                    "display_and_save_kw": "float_format_subset",
                    "float_format_precision": 1,
                },
                id="float.1f",
            ),
            pytest.param(
                {
                    "format": "{:.2f}",
                    "display_and_save_kw": "float_format_subset",
                    "float_format_precision": 2,
                },
                id="float.2f",
            ),
        ],
    )
    def test_styler_expected_text(
        self,
        iris: pd.DataFrame,
        iris_single_col_subset: Union[str, pd.Index],
        kwargs: dict[str, Any],
        save_image: bool,
        save_excel: bool,
    ) -> None:
        """Test for expected text in Stylers"""
        iris, kwargs = iris.copy(), kwargs.copy()
        col_name = self.col_name_from_iris_single_col_subset(iris_single_col_subset)

        if kwargs.pop("need_large_numbers", False):
            # Need large numbers to test thousands seperator
            large_iris = iris.copy()
            numeric_cols = large_iris.select_dtypes("number").columns
            large_iris[numeric_cols] = (large_iris[numeric_cols] * 10**6).astype(int)
            iris = large_iris

        col = iris[col_name]
        an_expected_value = col.iloc[0]
        try:
            an_expected_value = kwargs.pop("format").format(an_expected_value)
        except ValueError:
            # Number formatting can't be applied to str
            # Just make sure everything goes ok
            an_expected_value = ""

        if pd.api.types.is_string_dtype(col):
            context: ContextManager[Optional[object]] = pytest.raises(ValueError)
        else:
            context = does_not_raise()
        with context:
            # str columns with incorrect format code should
            # throw a ValueError

            # d is really dict[str, Union[str, pd.Index]], but mypy complains
            d: dict[str, Any] = {
                kwargs.pop("display_and_save_kw"): iris_single_col_subset
            }
            styler = display_and_save_df(
                iris, save_image=save_image, save_excel=save_excel, **d, **kwargs
            )
            styler.to_html()
            html = styler.to_html()
            assert an_expected_value in html

    def test_auto_percentage_format(
        self,
        iris: pd.DataFrame,
        iris_cols: pd.Series,
        save_image: bool,
        save_excel: bool,
    ) -> None:
        col = iris_cols.name
        new_col = f"{col} %"
        df_w_pcnt_sign_col = iris.rename(columns={col: new_col})
        try:
            an_expected_value = f"{df_w_pcnt_sign_col[new_col].iloc[0]:.0%}"
        except ValueError:
            # Can't format str as percent
            # Just make sure nothing fails
            an_expected_value = ""
        styler = display_and_save_df(
            df_w_pcnt_sign_col,
            percentage_format_subset="auto",
            percentage_format_precision=0,
            save_image=save_image,
            save_excel=save_excel,
        )

        html = styler.to_html()
        assert an_expected_value in html

    def test_auto_thousands_format(
        self,
        iris: pd.DataFrame,
        iris_cols: pd.Series,
        save_image: bool,
        save_excel: bool,
    ) -> None:
        iris, iris_cols = iris.copy(), iris_cols.copy()
        col = iris_cols.name

        if pd.api.types.is_numeric_dtype(iris_cols):
            # Make thousands-formattable values
            iris[col] = (iris_cols * 10**6).astype(int)
            an_expected_value = f"{iris[col].iloc[0]:,}"
        else:
            # Can't .astype(int) to str column
            # Just make sure nothing fails
            an_expected_value = ""

        styler = display_and_save_df(
            iris,
            thousands_format_subset="auto",
            save_image=save_image,
            save_excel=save_excel,
        )

        assert an_expected_value in styler.to_html()

    @pytest.mark.parametrize("precision", range(3))
    def test_auto_float_format(
        self,
        iris: pd.DataFrame,
        iris_cols: pd.Series,
        precision: int,
        save_image: bool,
        save_excel: bool,
    ) -> None:
        iris, iris_cols = iris.copy(), iris_cols.copy()

        if pd.api.types.is_numeric_dtype(iris_cols):
            an_expected_value = f"{iris_cols.iloc[0]:.{precision}f}"
        else:
            # Can't format str as float
            # Just make sure nothing fails
            an_expected_value = ""

        styler = display_and_save_df(
            iris,
            float_format_subset="auto",
            float_format_precision=precision,
            save_image=save_image,
            save_excel=save_excel,
        )

        assert an_expected_value in styler.to_html()

    combos = [
        list(combo) for r in range(4) for combo in itertools.combinations("ABC", r)
    ]

    @pytest.mark.parametrize("subset", combos, ids=map(repr, combos))  # noqa
    def test_datetime_format(
        self,
        datetime_df: pd.DataFrame,
        subset: Sequence[str],
        strftime: str,
        save_image: bool,
        save_excel: bool,
    ) -> None:
        if len(subset) > 0:
            an_expected_value = datetime_df[subset[0]].iloc[0]
            an_expected_value = f"{an_expected_value:{strftime}}"
        else:
            # If no subset is given, it's hard to say how exactly
            # the dates will be formatted. For now, just make sure
            # that nothing fails.
            an_expected_value = ""

        styler = display_and_save_df(
            datetime_df,
            date_format_subset=subset,
            date_format=strftime,
            save_image=save_image,
            save_excel=save_excel,
        )
        html = styler.to_html()
        assert an_expected_value in html

    def test_auto_datetime_format(
        self,
        datetime_and_float_df: pd.DataFrame,
        strftime: str,
        save_image: bool,
        save_excel: bool,
    ) -> None:
        expected_values = [
            f"{datetime_and_float_df[col].iloc[-1]:{strftime}}" for col in "ABC"
        ]

        styler = display_and_save_df(
            datetime_and_float_df,
            date_format_subset="auto",
            date_format=strftime,
            save_image=save_image,
            save_excel=save_excel,
        )

        html = styler.to_html()
        assert all(expected_value in html for expected_value in expected_values)

    def test_hide_index(
        self, iris: pd.DataFrame, save_image: bool, save_excel: bool
    ) -> None:
        iris = iris.copy().set_index("Name")
        styler = display_and_save_df(
            iris, hide_index=True, save_image=save_image, save_excel=save_excel
        )
        html = styler.to_html()

        assert all(name not in html for name in iris.index.unique())

        styler_with_index = display_and_save_df(
            iris, hide_index=False, save_image=save_image, save_excel=save_excel
        )
        html_with_index = styler_with_index.to_html()

        assert all(name in html_with_index for name in iris.index.unique())

    def test_ryg_background_gradient(
        self,
        iris: pd.DataFrame,
        iris_single_col_subset: Union[str, pd.Index],
        save_image: bool,
        save_excel: bool,
    ) -> None:
        col_name = self.col_name_from_iris_single_col_subset(iris_single_col_subset)

        # Should get ValueError on string dtypes
        if pd.api.types.is_string_dtype(iris[col_name]):
            context: ContextManager[Optional[object]] = pytest.raises(
                ValueError, match="could not convert string to float"
            )
        else:
            context = does_not_raise()

        with context:
            styler = display_and_save_df(
                iris,
                ryg_bg_subset=iris_single_col_subset,
                save_image=save_image,
                save_excel=save_excel,
            )
            html = styler.to_html()
            expected_min_color = "background-color: #f8696b"
            expected_max_color = "background-color: #63be7b"
            assert expected_min_color.casefold() in html.casefold()
            assert expected_max_color.casefold() in html.casefold()

    def test_ryg_background_vmin(
        self,
        iris: pd.DataFrame,
        iris_single_col_subset: Union[str, pd.Index],
        save_image: bool,
        save_excel: bool,
    ) -> None:

        col_name = self.col_name_from_iris_single_col_subset(iris_single_col_subset)

        if pd.api.types.is_string_dtype(iris[col_name]):
            return

        # All iris columns should have min > 0
        assert all(iris.select_dtypes("number").min() > 0)

        # By setting vmin=0, the bottom red color should not appear.
        styler = display_and_save_df(
            iris,
            ryg_bg_subset=iris_single_col_subset,
            ryg_bg_vmin=0,
            save_image=save_image,
            save_excel=save_excel,
        )

        expected_min_color = "background-color: #f8696b"
        expected_max_color = "background-color: #63be7b"
        html = styler.to_html()

        assert expected_min_color.casefold() not in html
        assert expected_max_color.casefold() in html

    def test_ryg_background_vmax(
        self,
        iris: pd.DataFrame,
        iris_single_col_subset: Union[str, pd.Index],
        save_image: bool,
        save_excel: bool,
    ) -> None:

        col_name = self.col_name_from_iris_single_col_subset(iris_single_col_subset)

        if pd.api.types.is_string_dtype(iris[col_name]):
            return
        # a vmax larger than any value:
        vmax = iris.max(numeric_only=True).max() + 1
        # By settings a large vmax, the top red color should not appear
        styler = display_and_save_df(
            iris,
            ryg_bg_subset=iris_single_col_subset,
            ryg_bg_vmax=vmax,
            save_image=save_image,
            save_excel=save_excel,
        )

        expected_min_color = "background-color: #f8696b"
        expected_max_color = "background-color: #63be7b"
        html = styler.to_html()

        assert expected_min_color.casefold() in html
        assert expected_max_color.casefold() not in html

    def test_gyr_background_vmin(
        self,
        iris: pd.DataFrame,
        iris_single_col_subset: Union[str, pd.Index],
        save_image: bool,
        save_excel: bool,
    ) -> None:
        col_name = self.col_name_from_iris_single_col_subset(iris_single_col_subset)

        if pd.api.types.is_string_dtype(iris[col_name]):
            return

        # All iris columns should have min > 0
        assert all(iris.select_dtypes("number").min() > 0)

        # By setting vmin=0, the bottom green color should not appear.
        styler = display_and_save_df(
            iris,
            gyr_bg_subset=iris_single_col_subset,
            gyr_bg_vmin=0,
            save_image=save_image,
            save_excel=save_excel,
        )

        expected_max_color = "background-color: #f8696b"
        expected_min_color = "background-color: #63be7b"
        html = styler.to_html()

        assert expected_min_color.casefold() not in html
        assert expected_max_color.casefold() in html

    def test_gyr_background_vmax(
        self,
        iris: pd.DataFrame,
        iris_single_col_subset: Union[str, pd.Index],
        save_image: bool,
        save_excel: bool,
    ) -> None:
        col_name = self.col_name_from_iris_single_col_subset(iris_single_col_subset)

        if pd.api.types.is_string_dtype(iris[col_name]):
            return
        # a vmax larger than any value:
        vmax = iris.max(numeric_only=True).max() + 1
        # By settings a large vmax, the top red color should not appear
        styler = display_and_save_df(
            iris,
            gyr_bg_subset=iris_single_col_subset,
            gyr_bg_vmax=vmax,
            save_image=save_image,
            save_excel=save_excel,
        )

        expected_max_color = "background-color: #f8696b"
        expected_min_color = "background-color: #63be7b"
        html = styler.to_html()

        assert expected_min_color.casefold() in html
        assert expected_max_color.casefold() not in html

    def test_bar_style(
        self,
        iris: pd.DataFrame,
        iris_single_col_subset: Union[str, pd.Index],
        save_image: bool,
        save_excel: bool,
    ) -> None:
        col_name = self.col_name_from_iris_single_col_subset(iris_single_col_subset)

        if pd.api.types.is_string_dtype(iris[col_name]):
            # Can't apply bar format to string dtype columns
            return
        styler = display_and_save_df(
            iris,
            bar_subset=iris_single_col_subset,
            save_image=save_image,
            save_excel=save_excel,
        )
        html = styler.to_html()
        expected_max_bar = (
            "background: linear-gradient" "(90deg, #638ec6 90.0%, transparent 90.0%);"
        ).casefold()

        assert expected_max_bar in html.casefold()

    @staticmethod
    def bar_pcnt_from_html(html: str) -> pd.Series:
        regexp = (
            r"background: linear\-gradient\(90deg,.* #638ec6 "
            r"(?P<percentage>\d{1,2}\.\d)\%"
        )
        pcnts = re.findall(regexp, html)
        series = pd.Series(pcnts, dtype=float)
        return series

    def test_bar_vmin(
        self,
        iris: pd.DataFrame,
        iris_single_col_subset: Union[str, pd.Index],
        save_image: bool,
        save_excel: bool,
    ) -> None:
        col_name = self.col_name_from_iris_single_col_subset(iris_single_col_subset)

        if pd.api.types.is_string_dtype(iris[col_name]):
            return

        regular_styler = display_and_save_df(
            iris,
            bar_subset=iris_single_col_subset,
            save_image=save_image,
            save_excel=save_excel,
        )
        vmin_styler = display_and_save_df(
            iris,
            bar_subset=iris_single_col_subset,
            bar_vmin=-1,
            save_image=save_image,
            save_excel=save_excel,
        )

        # By setting a vmin smaller than the column min, the bars should get larger
        # Except for the maximum
        regular_pcnts = self.bar_pcnt_from_html(regular_styler.to_html())
        vmin_pcnts = self.bar_pcnt_from_html(vmin_styler.to_html())
        assert (vmin_pcnts >= regular_pcnts).all()

    def test_bar_vmax(
        self,
        iris: pd.DataFrame,
        iris_single_col_subset: Union[str, pd.Index],
        save_image: bool,
        save_excel: bool,
    ) -> None:
        col_name = self.col_name_from_iris_single_col_subset(iris_single_col_subset)

        if pd.api.types.is_string_dtype(iris[col_name]):
            return

        regular_styler = display_and_save_df(
            iris,
            bar_subset=iris_single_col_subset,
            save_image=save_image,
            save_excel=save_excel,
        )
        vmax_styler = display_and_save_df(
            iris,
            bar_subset=iris_single_col_subset,
            bar_vmax=10,
            save_image=save_image,
            save_excel=save_excel,
        )

        # By setting a vmax larger than the global max, the bars should get shorter
        regular_pcnts = self.bar_pcnt_from_html(regular_styler.to_html())
        vmax_pcnts = self.bar_pcnt_from_html(vmax_styler.to_html())
        assert (vmax_pcnts < regular_pcnts).all()

    # TODO: tests of additional *_kwargs. Should somehow parameterize all the tests
    #  above, if possible...


@pytest.mark.flaky(rerun_filter=tm._is_tkinter_error, max_runs=5)
@pytest.mark.parametrize("save_image", [True, False], ids="save_image={}".format)
class TestDisplayAndSaveFig:
    def display_and_save_fig(self, *args: Any, **kwargs: Any) -> None:
        from EAB_tools.io.display import display_and_save_fig as display_and_save_fig_og

        display_and_save_fig_og(*args, **kwargs)
        tm._minimize_tkagg()

    def test_doesnt_fail(
        self, mpl_figs_and_axes: Union[plt.Figure, plt.Axes], save_image: bool
    ) -> None:
        display_and_save_fig(mpl_figs_and_axes, save_image=save_image)

    def test_expected_output(
        self,
        save_image: bool,
        iris: pd.DataFrame,
        tmp_path: Path,
    ) -> None:
        fig, ax = plt.subplots(
            subplot_kw={
                "xlabel": "SepalLength",
                "ylabel": "SepalWidth",
                "title": self.test_expected_output.__name__,
            },
            facecolor="white",
        )

        for iris_type in iris["Name"].unique():
            subset: pd.DataFrame = iris[iris["Name"] == iris_type]
            ax.plot("SepalLength", "SepalWidth", "o", data=subset, label=iris_type)
        ax.legend()

        display_and_save_fig(fig, save_image=True, filename="foo.png")
        assert tm._test_photos_are_equal(
            tmp_path / "foo.png",
            Path(__file__).parent / "data" / "test_expected_output.png",
        )
        plt.close(fig)

    def test_infer_filename_from_fig_suptitle(
        self,
        save_image: bool,
        mpl_figs_and_axes: Union[plt.Figure, plt.Axes],
    ) -> None:
        fig: plt.Figure
        if isinstance(mpl_figs_and_axes, plt.Axes):
            fig = mpl_figs_and_axes.get_figure()
        else:
            fig = mpl_figs_and_axes

        name = sanitize_filename(str(fig))
        fig.suptitle(name)

        display_and_save_fig(mpl_figs_and_axes, save_image=True)
        assert Path(f"{name}.png").exists()

    def test_infer_filename_from_axis(
        self, save_image: bool, mpl_figs_and_axes: Union[plt.Figure, plt.Axes]
    ) -> None:
        if isinstance(mpl_figs_and_axes, plt.Figure):
            axes: plt.Axes = mpl_figs_and_axes.axes[0]
        else:
            axes = mpl_figs_and_axes

        # Pretty random name
        name = sanitize_filename(str(mpl_figs_and_axes))
        axes.set_title(name)

        display_and_save_fig(mpl_figs_and_axes, save_image=True)
        assert Path(f"{name}.png").exists()

    def test_filename_from_hash(
        self,
        save_image: bool,
        mpl_figs_and_axes: Union[plt.Figure, plt.Axes],
    ) -> None:
        expected_hash = eab.util.hash_mpl_fig(mpl_figs_and_axes)
        display_and_save_fig(mpl_figs_and_axes, save_image=True)

        assert Path(f"{expected_hash}.png").exists()
