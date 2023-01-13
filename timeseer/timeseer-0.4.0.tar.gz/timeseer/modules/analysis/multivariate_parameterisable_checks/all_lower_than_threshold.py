"""A check that evaluates whether all series are lower than a specific user-specified threshold.
"""

from datetime import datetime

import pandas as pd

from pandas.api.types import is_string_dtype

from timeseer import (
    AnalysisInput,
    AnalysisResult,
    DataType,
    EventFrame,
    ModuleParameterType,
    MultivariateAnalysisInput,
)
from timeseer.analysis.utils import (
    event_frames_from_dataframe,
    process_open_intervals,
    handle_open_intervals,
)


_CHECK_NAME = "All lower than threshold"
_EVENT_FRAME_NAME = "All lower than threshold"

META = {
    "checks": [
        {
            "name": _CHECK_NAME,
            "event_frames": [_EVENT_FRAME_NAME],
        }
    ],
    "conditions": [
        {
            "min_series": 1,
            "min_data_points": 1,
            "data_type": [DataType.FLOAT32, DataType.FLOAT64],
        }
    ],
    "parameters": [
        {
            "name": "threshold",
            "type": ModuleParameterType.FLOAT64,
            "helpText": "All values lower than this parameter will be considerd anomalous.",
        },
    ],
    "signature": "multivariate",
}


def _by_date(frame: EventFrame) -> datetime:
    return frame.start_date


def _drop_event_frames_before(
    event_frames: list[EventFrame], max_end_date: datetime
) -> list[EventFrame]:
    return [
        frame
        for frame in event_frames
        if frame.end_date is None or frame.end_date >= max_end_date
    ]


def _get_earliest_end_date(event_frames: list[EventFrame]) -> datetime | None:
    earliest = None
    for event_frame in event_frames:
        if earliest is None or earliest > event_frame.end_date:
            earliest = event_frame.end_date
    return earliest


def _detect_event_frames(
    event_frames: list[EventFrame], active_count: int
) -> list[EventFrame]:
    active_event_frames: list[EventFrame] = []
    results = []
    active_frame = None
    for event_frame in sorted(event_frames, key=_by_date):
        active_event_frames = _drop_event_frames_before(
            active_event_frames, event_frame.start_date
        )

        if len(active_event_frames) != active_count:
            if active_frame is not None:
                results.append(active_frame)
                active_frame = None

        active_event_frames.append(event_frame)

        if len(active_event_frames) == active_count:
            if active_frame is None:
                active_frame = EventFrame(_EVENT_FRAME_NAME, event_frame.start_date)
            active_frame.end_date = _get_earliest_end_date(active_event_frames)
        else:
            if active_frame is not None:
                results.append(active_frame)
                active_frame = None

    if active_frame is not None:
        results.append(active_frame)

    return results


def _get_intervals(outliers, df, event_type):
    outliers = pd.Series(data=outliers, index=df.index).fillna(False)
    outlier_grp = (outliers != outliers.shift().bfill()).cumsum()
    outlier_intervals = (
        df.assign(outlier_grp=outlier_grp)[outliers]
        .reset_index()
        .groupby(["outlier_grp"])
        .agg(start_date=("ts", "first"), end_date=("ts", "last"))
    )
    outlier_intervals["type"] = event_type
    return outlier_intervals


def _get_active_points(df: pd.DataFrame, threshold: float):
    return df["value"] < threshold


def _clean_dataframe(df: pd.DataFrame):
    return df[~df.index.duplicated(keep="first")].dropna().sort_index()


def _run_univariate_limit_check(
    analysis_input: AnalysisInput, threshold: float
) -> tuple[list[EventFrame], datetime | None]:
    df = analysis_input.data
    df = _clean_dataframe(df)

    active_points = _get_active_points(df, threshold)
    intervals = _get_intervals(active_points, df, _EVENT_FRAME_NAME)
    intervals = handle_open_intervals(df, intervals)

    frames = event_frames_from_dataframe(process_open_intervals(intervals))

    last_analyzed_point = None
    if len(df) > 1:
        last_analyzed_point = df.index[-2].to_pydatetime()

    return list(frames), last_analyzed_point


def _run_limit_check(
    inputs: list[AnalysisInput], threshold: float
) -> tuple[list[EventFrame], datetime | None]:
    event_frames = []
    last_analyzed_point = None

    for analyis_input in inputs:
        input_event_frames, input_last_analyzed_point = _run_univariate_limit_check(
            analyis_input, threshold
        )
        event_frames.extend(input_event_frames)
        if (
            last_analyzed_point is None
            or input_last_analyzed_point is None
            or input_last_analyzed_point < last_analyzed_point
        ):
            last_analyzed_point = input_last_analyzed_point

    return _detect_event_frames(event_frames, len(inputs)), last_analyzed_point


def _is_valid_input(analysis_input: AnalysisInput) -> bool:
    if is_string_dtype(analysis_input.data["value"]):
        return False
    if len(_clean_dataframe(analysis_input.data)) == 0:
        return False
    return True


def _filter_invalid_inputs(inputs: list[AnalysisInput]) -> list[AnalysisInput]:
    return [
        analysis_input for analysis_input in inputs if _is_valid_input(analysis_input)
    ]


# pylint: disable=missing-function-docstring
def run(analysis_input: MultivariateAnalysisInput) -> AnalysisResult:
    if "threshold" not in analysis_input.parameters:
        return AnalysisResult(condition_message="No threshold parameter provided")

    valid_inputs = _filter_invalid_inputs(analysis_input.inputs)
    if len(valid_inputs) == 0:
        return AnalysisResult(
            condition_message="At least 1 series with values is required."
        )

    frames, last_analyzed_point = _run_limit_check(
        valid_inputs, analysis_input.parameters["threshold"]
    )
    return AnalysisResult(
        event_frames=frames,
        last_analyzed_point=last_analyzed_point,
    )
