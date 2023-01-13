"""The last archived timestamp of a series."""

from datetime import datetime

import pandas as pd

import timeseer

_STATISTIC_NAME = "Archival time: latest"

META = {
    "statistics": [{"name": _STATISTIC_NAME}],
    "run": "before",
    "conditions": [
        {
            "min_series": 1,
            "min_data_points": 1,
        }
    ],
    "signature": "univariate",
}


def _get_relevant_statistic(
    analysis_input: timeseer.AnalysisInput, stat_name: str
) -> datetime | None:
    statistics = [
        statistic.result
        for statistic in analysis_input.statistics
        if statistic.name == stat_name
    ]
    if statistics is None or len(statistics) == 0:
        return None
    return statistics[0]


def _get_previous_values(analysis_input: timeseer.AnalysisInput) -> datetime | None:
    return _get_relevant_statistic(analysis_input, _STATISTIC_NAME)


def _clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    return df[~df.index.duplicated(keep="first")].sort_index()


# pylint: disable=missing-function-docstring
def run(
    analysis_input: timeseer.AnalysisInput,
) -> timeseer.AnalysisResult:

    old_timestamp = _get_previous_values(analysis_input)
    new_timestamp = (
        _clean_dataframe(analysis_input.data).index.to_series()[-1].to_pydatetime()
    )
    if old_timestamp is not None:
        new_timestamp = max(old_timestamp, new_timestamp)

    return timeseer.AnalysisResult(
        statistics=[timeseer.Statistic(_STATISTIC_NAME, "datetime", new_timestamp)],
        last_analyzed_point=new_timestamp,
    )
