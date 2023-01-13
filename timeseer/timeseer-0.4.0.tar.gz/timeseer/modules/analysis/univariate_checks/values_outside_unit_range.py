"""For certain units (e.g. pH) there is a limited range values can take.

<p>This check validates whether for a specific set of units, the historical values are
within the expected deterministic range.</p>
<p class="scoring-explanation">The score for this check is based on the amount
of time values are outside of the unit range.</p>
<div class="ts-check-impact">
<p>Mismatches between unit range and measured values are data quality issues.
</p>
</div>
"""

from enum import Enum, auto
from datetime import datetime

import pandas as pd

from pandas.api.types import is_string_dtype

from timeseer import AnalysisInput, AnalysisResult, DataType, EventFrame
from timeseer.analysis.utils import (
    get_dimension,
    get_symbol,
    get_limited_units,
    get_unit_range,
    event_frames_from_dataframe,
    process_open_intervals,
    handle_open_intervals,
)
from timeseer.metadata import fields

_CHECK_NAME = "Values outside unit range"
_EVENT_FRAME_NAME = "Values outside unit range"


META = {
    "checks": [
        {
            "name": _CHECK_NAME,
            "event_frames": [_EVENT_FRAME_NAME],
        },
    ],
    "conditions": [
        {
            "min_series": 1,
            "min_data_points": 1,
            "data_type": [DataType.FLOAT32, DataType.FLOAT64],
        }
    ],
    "signature": "univariate",
}


class LimitType(Enum):
    """Choose whether to use physical or functional limits."""

    PHYSICAL = auto()
    FUNCTIONAL = auto()


def _get_intervals(outliers: pd.Series, df: pd.DataFrame, event_type: str):
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


def _get_active_points(
    df: pd.DataFrame, min_value: float, max_value: float
) -> pd.Series:
    return (df["value"] < min_value) | (df["value"] > max_value)


def _clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    return df[~df.index.duplicated(keep="first")].dropna().sort_index()


def _run_values_outside_unit_range_check(
    unit, analysis_input: AnalysisInput
) -> tuple[list[EventFrame], datetime | None]:
    df = analysis_input.data
    df = _clean_dataframe(df)

    min_value, max_value = get_unit_range(unit)

    active_points = _get_active_points(df, min_value, max_value)
    intervals = _get_intervals(active_points, df, _EVENT_FRAME_NAME)
    intervals = handle_open_intervals(df, intervals)

    frames = event_frames_from_dataframe(process_open_intervals(intervals))

    last_analyzed_point = None
    if len(df) > 1:
        last_analyzed_point = df.index[-2].to_pydatetime()

    return list(frames), last_analyzed_point


def _is_valid_input(analysis_input: AnalysisInput, unit: str) -> tuple[str, bool]:
    if len(_clean_dataframe(analysis_input.data)) == 0:
        return "No data", False
    if is_string_dtype(analysis_input.data["value"]):
        return "Can not be a string", False
    if unit is None:
        return "No unit", False
    units_zero_min, dimensions_zero_min = get_limited_units()
    if (get_dimension(unit) not in dimensions_zero_min) & (
        get_symbol(unit) not in units_zero_min
    ):
        return "Unit range is unknown", False
    return "OK", True


# pylint: disable=missing-function-docstring
def run(
    analysis_input: AnalysisInput,
) -> AnalysisResult:
    unit = analysis_input.metadata.get_field(fields.Unit)

    message, is_ok = _is_valid_input(analysis_input, unit)
    if not is_ok:
        return AnalysisResult(condition_message=message)

    frames, last_analyzed_point = _run_values_outside_unit_range_check(
        unit, analysis_input
    )
    return AnalysisResult(
        event_frames=frames,
        last_analyzed_point=last_analyzed_point,
    )
