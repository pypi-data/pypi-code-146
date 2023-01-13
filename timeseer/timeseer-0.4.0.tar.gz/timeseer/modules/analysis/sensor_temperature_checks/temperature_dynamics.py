""" Check if the dynamics of a temperature is normal based on
behavior of all temperatures in a serie set.
"""

import pandas as pd

from timeseer import (
    AnalysisInput,
    AnalysisResult,
    EventFrame,
    DataType,
    ModuleParameterType,
)
from timeseer.analysis.utils import (
    event_frames_from_dataframe,
    process_open_intervals,
    handle_open_intervals,
    get_separate_active_intervals,
)


_CHECK_NAME = "Temperature dynamics outlier"
_EVENT_FRAME_NAME = "Temperature dynamics outlier"

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
            "range": {
                "lower": 0,
            },
            "default": 0.03,
            "helpText": "Threshold sets the absolute in-/decrease per second of a sensor.",
        },
    ],
    "signature": "univariate",
}


def _get_active_points(df: pd.DataFrame, change_over_time: float) -> pd.Series:
    diff_values = abs(df["value"].diff())
    diff_times = df.index.to_series().diff().dt.total_seconds()
    return (diff_values / diff_times) >= change_over_time


def _clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    return df[~df.index.duplicated(keep="first")].dropna().sort_index()


def _run_temperature_dynamics(analysis_input: AnalysisInput) -> list[EventFrame]:
    change_over_time = 0.03  # degree per second
    if "threshold" in analysis_input.parameters:
        change_over_time = analysis_input.parameters["threshold"]

    df = _clean_dataframe(analysis_input.data)
    active_points = _get_active_points(df, change_over_time)

    intervals = get_separate_active_intervals(df, active_points, _CHECK_NAME)
    intervals = handle_open_intervals(df, intervals)

    event_frames = event_frames_from_dataframe(process_open_intervals(intervals))

    return list(event_frames)


def _is_temperature_series(analysis_input: AnalysisInput) -> bool:
    temp_units = ["celcius", "kelvin", "c", "k", "f", "fahrenheit"]
    series_unit = analysis_input.metadata.get_field_by_name("unit")
    if not series_unit:
        return False
    if any(series_unit.upper() == unit.upper() for unit in temp_units):
        return True
    return False


# pylint: disable=missing-function-docstring
def run(analysis_input: AnalysisInput) -> AnalysisResult:
    if not _is_temperature_series(analysis_input):
        return AnalysisResult(condition_message="Not a temperature series")
    event_frames = _run_temperature_dynamics(analysis_input)
    return AnalysisResult(
        event_frames=event_frames,
        last_analyzed_point=analysis_input.data.index[-1].to_pydatetime(),
    )
