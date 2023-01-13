""" Calculate the distributed non-zero staleness sketch of the time series. """

import jsonpickle
import pandas as pd
from ddsketch.ddsketch import DDSketch

import timeseer
from timeseer.analysis.utils import get_separate_active_intervals


META: dict = {
    "statistics": [
        {"name": "Stale Non-zero Sketch"},
    ],
    "run": "before",
    "conditions": [
        {
            "min_series": 1,
            "min_data_points": 2,
        }
    ],
    "signature": "univariate",
}


def _get_repeated_lengths(df: pd.DataFrame) -> pd.DataFrame:
    df_copy = df.copy()
    df_copy["shifted"] = df_copy["value"].shift()
    active_points = (df_copy["shifted"] == df_copy["value"]) & (df_copy["value"] != 0)
    return get_separate_active_intervals(df, active_points, "foo")


def _clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    return df[~df.index.duplicated(keep="first")].sort_index()


def _run_get_sketch(
    analysis_input: timeseer.AnalysisInput, sketch: DDSketch
) -> DDSketch:
    df = _clean_dataframe(analysis_input.data)
    if len(df) == 0:
        return sketch

    if sketch is None:
        sketch = DDSketch(0.001)

    repeated_lengths = _get_repeated_lengths(df)
    for _, row in repeated_lengths.iterrows():
        sketch.add((row["end_date"] - row["start_date"]).total_seconds())

    return sketch


def _get_relevant_statistic(
    analysis_input: timeseer.AnalysisInput, stat_name: str
) -> DDSketch | None:
    statistics = [
        statistic.result
        for statistic in analysis_input.statistics
        if statistic.name == stat_name
    ]
    if statistics is None or len(statistics) == 0:
        return None
    return jsonpickle.decode(statistics[0])


# pylint: disable=missing-function-docstring
def run(
    analysis_input: timeseer.AnalysisInput,
) -> timeseer.AnalysisResult:
    previous_sketch = _get_relevant_statistic(analysis_input, "Stale Non-zero Sketch")

    sketch = _run_get_sketch(analysis_input, previous_sketch)
    if sketch is None:
        return timeseer.AnalysisResult(condition_message="No stale non-zero sketch")

    sketch_statistic = timeseer.Statistic(
        META["statistics"][0]["name"], "sketch", jsonpickle.encode(sketch)
    )
    return timeseer.AnalysisResult(
        statistics=[sketch_statistic],
        last_analyzed_point=analysis_input.data.index[-2].to_pydatetime(),
    )
