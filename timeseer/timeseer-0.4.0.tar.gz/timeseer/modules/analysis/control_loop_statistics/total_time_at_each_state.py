"""
Total time at each state
"""

import pandas as pd


import timeseer
from timeseer import AnalysisInput, AnalysisResult
from timeseer.metadata import fields


META: dict = {
    "statistics": [
        {"name": "Total time at each state"},
    ],
    "conditions": [
        {
            "min_series": 1,
            "min_data_points": 2,
        }
    ],
    "signature": "univariate",
}


def _clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    return df[~df.index.duplicated(keep="first")].dropna().sort_index()


def _is_valid_input(analysis_input: AnalysisInput) -> tuple[str, bool]:
    if len(_clean_dataframe(analysis_input.data)) == 0:
        return "No clean data", False
    position = analysis_input.metadata.get_field_by_name("control loop")
    if position != "State":
        return "Only applicable to State", False
    return "OK", True


def _total_time_at_state(df: pd.DataFrame, values_dict: dict) -> pd.DataFrame:
    df = _clean_dataframe(df)
    meas_times = df.index.to_series()
    df["duration"] = meas_times.shift(-1) - meas_times
    times = df.groupby("value").sum()
    if values_dict:
        times.index = [values_dict.get(value) for value in times.index]
    times = times.groupby(times.index).sum()
    total_duration = times["duration"].sum()
    times["%"] = (times["duration"] / total_duration) * 100
    return times


def _get_statistics(times_table):
    stats = []
    values = []
    for ind, row in times_table.iterrows():
        values.append((ind, str(row["duration"])))
        stats.append(
            timeseer.Statistic(
                "total time at " + str(ind) + " state", "hidden", str(row["duration"])
            )
        )
    stat_table = timeseer.Statistic("Total time at each state", "table", values)
    stats.append(stat_table)
    return stats


# pylint: disable=missing-function-docstring
def run(
    analysis_input: timeseer.AnalysisInput,
) -> timeseer.AnalysisResult:
    message, is_ok = _is_valid_input(analysis_input)
    if not is_ok:
        return AnalysisResult(condition_message=message)
    try:
        dictionary = analysis_input.metadata.get_field(fields.Dictionary)
        value_dict = dictionary.mapping
    except AttributeError:
        value_dict = None
    times_table = _total_time_at_state(analysis_input.data, value_dict)
    statistics = _get_statistics(times_table)
    return timeseer.AnalysisResult(statistics=statistics)
