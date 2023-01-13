"""The compression ratio based on sampling ratio."""

from typing import Tuple

from timeseer.metadata import fields
from timeseer import AnalysisInput, AnalysisResult, Statistic

_STATISTIC_NAME = "Compression ratio"

META = {
    "statistics": [{"name": _STATISTIC_NAME}],
    "run": "before",
    "conditions": [
        {
            "min_series": 1,
            "min_data_points": 2,
        }
    ],
    "signature": "univariate",
}


def _get_relevant_statistic(analysis_input: AnalysisInput, stat_name: str):
    statistics = [
        statistic.result
        for statistic in analysis_input.statistics
        if statistic.name == stat_name
    ]
    if statistics is None or len(statistics) == 0:
        return 0
    return statistics[0]


def _get_point_count(data_points: list[Tuple[str, float]], name: str) -> float:
    if data_points is None:
        return 0

    for k, v in data_points:
        if k == name:
            return v
    return 0


def _get_previous_values(analysis_input: AnalysisInput) -> tuple[float, float]:
    prev_timespan = _get_relevant_statistic(analysis_input, "Total timespan")
    prev_data_points = _get_relevant_statistic(analysis_input, "Data points")
    if prev_data_points == 0:
        return 0, 0

    prev_compressed_count = (
        _get_point_count(prev_data_points, "Total valid")
        + _get_point_count(prev_data_points, "Total NaNs")
        + _get_point_count(prev_data_points, "Total flagged")
    )

    return prev_timespan, prev_compressed_count


# pylint: disable=missing-function-docstring
def run(
    analysis_input: AnalysisInput,
) -> AnalysisResult:
    sampling_rate = analysis_input.metadata.get_field(fields.SamplingRate)
    if sampling_rate is None:
        return AnalysisResult(condition_message="No sampling rate")

    (prev_timespan, prev_compressed_count) = _get_previous_values(analysis_input)

    meas_times = analysis_input.data.index.to_series()
    diff = meas_times[-1] - meas_times[0]
    range_seconds = diff.total_seconds()
    range_seconds = range_seconds + prev_timespan

    if range_seconds < sampling_rate:
        return AnalysisResult(
            statistics=[Statistic(_STATISTIC_NAME, "pct", 0)],
            last_analyzed_point=analysis_input.data.index[-1].to_pydatetime(),
        )
    original_count = int(range_seconds / sampling_rate) + 1
    compressed_count = len(analysis_input.data) + prev_compressed_count
    compression_ratio = 100 * (1 - compressed_count / original_count)

    return AnalysisResult(
        statistics=[Statistic(_STATISTIC_NAME, "pct", compression_ratio)],
        last_analyzed_point=analysis_input.data.index[-1].to_pydatetime(),
    )
