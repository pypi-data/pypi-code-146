from datetime import datetime
from typing import Iterator, cast

import daiquiri
import numpy as np
import pandas as pd
from pandas import DataFrame, DatetimeIndex
from pptx.chart.data import CategoryChartData

from dbnomics_pptx_tools.metadata import ChartSpec
from dbnomics_pptx_tools.repo import SeriesRepo

logger = daiquiri.getLogger(__name__)


def build_category_chart_data(chart_spec: ChartSpec, *, df: DataFrame) -> CategoryChartData:
    chart_spec_series_ids = chart_spec.get_series_ids()
    chart_data = CategoryChartData()

    pivoted_df = df.pivot(index="period", columns="series_id", values="value")
    chart_data.categories = cast(DatetimeIndex, pivoted_df.index).to_pydatetime()

    for series_id in chart_spec_series_ids:
        series_spec = chart_spec.find_series_spec(series_id)
        if series_spec is None:
            raise ValueError(f"Could not find spec for series {series_id!r}")
        series_name = series_spec.name
        if series_id not in pivoted_df:
            continue
        series = pivoted_df[series_id].replace({np.NaN: None})
        for transformer in series_spec.transformers:
            series = transformer(series_spec, series)
        chart_data.add_series(series_name, series.values)

    return chart_data


def filter_df_to_domain(df: DataFrame, *, max_datetime: datetime | None, min_datetime: datetime | None) -> DataFrame:
    if min_datetime is not None:
        df = df.query("period >= @min_datetime")
    if max_datetime is not None:
        df = df.query("period <= @max_datetime")
    return df


def load_chart_df(chart_spec: ChartSpec, *, repo: SeriesRepo) -> DataFrame:
    chart_spec_series_ids = chart_spec.get_series_ids()

    def iter_domain_dfs() -> Iterator[DataFrame]:
        for series_id in chart_spec_series_ids:
            df = repo.load(series_id)
            if df.empty:
                logger.warning("Series %r is empty", series_id)
                continue
            yield df

    return pd.concat(iter_domain_dfs())
