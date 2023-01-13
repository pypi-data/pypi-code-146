"""
Manual Untracked
"""

import pandas as pd

from timeseer import AnalysisInput, AnalysisResult, EventFrame
from timeseer.analysis.utils import (
    event_frames_from_dataframe,
    process_open_intervals,
    handle_open_intervals,
)
from timeseer.metadata import fields

_CHECK_NAME = "Manual untracked state"
_EVENT_FRAME_NAME = "Manual untracked state"


META = {
    "checks": [
        {
            "name": _CHECK_NAME,
            "event_frames": [_EVENT_FRAME_NAME],
        }
    ],
    "conditions": [{"min_series": 1, "min_data_points": 1}],
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


def _get_correct_key(analysis_input, target_value):
    dictionary = analysis_input.metadata.get_field(fields.Dictionary)
    value_dict = dictionary.mapping
    return list(value_dict.keys())[list(value_dict.values()).index(target_value)]


def _get_active_points(df: pd.DataFrame, target) -> pd.Series:
    return df["value"] == target


def _get_intervals(
    outliers: pd.Series, df: pd.DataFrame, event_type: str
) -> pd.DataFrame:
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


def _run_manual_untracked_check(df: pd.DataFrame, target) -> list[EventFrame]:
    df = _clean_dataframe(df)
    active_points = _get_active_points(df, target)
    intervals = _get_intervals(active_points, df, _EVENT_FRAME_NAME)
    intervals = handle_open_intervals(df, intervals)
    intervals = process_open_intervals(intervals)

    frames = event_frames_from_dataframe(intervals)
    last_analyzed_point = df.index[-1]

    return list(frames), last_analyzed_point


# pylint: disable=missing-function-docstring
def run(analysis_input: AnalysisInput) -> AnalysisResult:

    message, is_ok = _is_valid_input(analysis_input)
    if not is_ok:
        return AnalysisResult(condition_message=message)
    try:
        target_key = _get_correct_key(analysis_input, "Manual")
    except AttributeError:
        return AnalysisResult(condition_message="Undefined Manual State")

    frames, last_analyzed_point = _run_manual_untracked_check(
        analysis_input.data, target_key
    )

    return AnalysisResult(
        event_frames=frames, last_analyzed_point=last_analyzed_point.to_pydatetime()
    )
