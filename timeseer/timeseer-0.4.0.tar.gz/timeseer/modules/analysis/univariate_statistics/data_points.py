""" Calculates the number of data points and the data points per day and per hour in a time series. """

from datetime import timedelta

from typing import Optional, Tuple

from timeseer import AnalysisInput, AnalysisResult, Statistic

_STATISTIC_NAME = "Data points"

META = {
    "statistics": [{"name": _STATISTIC_NAME}, {"name": "Total timespan"}],
    "run": "before",
    "conditions": [
        {
            "min_series": 1,
        }
    ],
    "signature": "univariate",
}


def _get_timespan(analysis_input: AnalysisInput) -> timedelta:
    first_timestamp = analysis_input.data.index.to_series()[0].to_pydatetime()
    last_timestamp = analysis_input.data.index.to_series()[-1].to_pydatetime()
    return last_timestamp - first_timestamp


def _get_relevant_statistic(analysis_input: AnalysisInput, stat_name: str):
    statistics = [
        statistic.result
        for statistic in analysis_input.statistics
        if statistic.name == stat_name
    ]
    if statistics is None or len(statistics) == 0:
        return None
    return statistics[0]


def _get_previous_values(
    analysis_input: AnalysisInput,
) -> tuple[list[Tuple[str, int]] | None, float | None]:
    data_points = _get_relevant_statistic(analysis_input, "Data points")
    total_timespan = _get_relevant_statistic(analysis_input, "Total timespan")
    return (data_points, total_timespan)


def _get_point_count(
    data_points: list[Tuple[str, int]] | None, name: str
) -> Optional[int]:
    if data_points is None:
        return None

    for k, v in data_points:
        if k == name:
            return v
    return None


def _update_bad_quality_points(
    analysis_input: AnalysisInput, data_points: list[tuple[str, int]] | None
) -> int:
    bad_quality_points = 0
    prev_count = _get_point_count(data_points, "Total flagged")
    if prev_count is not None:
        bad_quality_points = prev_count

    if "quality" in analysis_input.data.columns:
        bad_quality_points = bad_quality_points + sum(
            analysis_input.data["quality"].isin([0])
        )
    return bad_quality_points


def _update_nan_points(
    analysis_input: AnalysisInput, data_points: list[tuple[str, int]] | None
) -> int:
    nan_points = 0
    prev_count = _get_point_count(data_points, "Total NaNs")
    if prev_count is not None:
        nan_points = prev_count
    nan_points = nan_points + analysis_input.data["value"].isna().sum()
    return nan_points


def _update_valid_points(
    analysis_input: AnalysisInput,
    data_points: list[Tuple[str, int]] | None,
    nan_points: int,
    bad_quality_points: int,
) -> int:
    total_points = 0
    prev_count = _get_point_count(data_points, "Total valid")
    if prev_count is not None:
        total_points = prev_count

    prev_nan = _get_point_count(data_points, "Total NaNs")
    if prev_nan is not None:
        total_points = total_points + prev_nan
    prev_flag = _get_point_count(data_points, "Total flagged")
    if prev_flag is not None:
        total_points = total_points + prev_flag

    valid_points = total_points + int(
        len(analysis_input.data) - nan_points - bad_quality_points
    )
    return valid_points


def _update_timespan(
    analysis_input: AnalysisInput, prev_timespan: float | None
) -> timedelta:
    if prev_timespan is not None:
        return _get_timespan(analysis_input) + timedelta(seconds=prev_timespan)
    return _get_timespan(analysis_input)


# pylint: disable=missing-function-docstring
def run(
    analysis_input: AnalysisInput,
) -> AnalysisResult:

    (data_points, prev_timespan) = _get_previous_values(analysis_input)

    bad_quality_points = _update_bad_quality_points(analysis_input, data_points)
    nan_points = _update_nan_points(analysis_input, data_points)
    valid_points = _update_valid_points(
        analysis_input, data_points, nan_points, bad_quality_points
    )

    result = [("Total valid", int(valid_points))]
    result.append(("Total NaNs", int(nan_points)))
    result.append(("Total flagged", int(bad_quality_points)))

    if len(analysis_input.data) == 0:
        return AnalysisResult(statistics=[Statistic(_STATISTIC_NAME, "table", result)])

    timespan = _update_timespan(analysis_input, prev_timespan)

    if timespan.days > 0:
        result.append(
            (
                "Avg valid / day",
                int(valid_points / (timespan.total_seconds() / 60 / 60 / 24)),
            )
        )

    if timespan.total_seconds() > 0:
        result.append(
            (
                "Avg valid / hour",
                int(valid_points / (timespan.total_seconds() / 60 / 60)),
            )
        )

    statistics = [Statistic(_STATISTIC_NAME, "table", result)]
    statistics.append(Statistic("Total timespan", "hidden", timespan.total_seconds()))

    return AnalysisResult(
        statistics=statistics,
        last_analyzed_point=analysis_input.data.index[-1].to_pydatetime(),
    )
