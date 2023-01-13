"""Identification of big jumps in consecutive values.

<p>This check identifies how many times over the time-frame of the analysis a sudden spike occurs.
A sudden spike is defined as an outlier wrt historical differences in consecutive values.</p>
<p><img src='../static/images/reporting/big_jumps.svg'></p>
<p class="scoring-explanation">The score of this check is calculated based on the count of all
points where a positive or negative jump occurs. Imagine that 100 points are analyzed in a given time-frame
and there are 2 positive and 1 negative jumps. The score for this check in that case would be
97% = 1 - 3 / 100. Which means that for 90% of all points no jump is present.</p>
<div class="ts-check-impact">
<p>
Big sudden jumps in data often correspond to faults in the data captation chain.
Several calculations are sensitive to these type of sudden changes and process decision chains
based on such an outlier can propagate through the system.
Any type of anomaly detection based on normal behavior of the phyiscal sensor can act as a guide for
prioritization of callibration / maintenance.
</p>
</div>
"""

from typing import Any

import jsonpickle
import pandas as pd

from scipy.ndimage import shift
from ddsketch.ddsketch import DDSketch

from timeseer import AnalysisInput, AnalysisResult, EventFrame, ModuleParameterType

from timeseer import DataType
from timeseer.analysis.utils import (
    event_frames_from_dataframe,
    process_open_intervals,
    handle_open_intervals,
    get_cutoff_for_sketch,
)


META = {
    "checks": [
        {
            "name": "Jumps (upwards)",
            "event_frames": ["Jump outlier (upwards)"],
        },
        {
            "name": "Jumps (downwards)",
            "event_frames": ["Jump outlier (downwards)"],
        },
    ],
    "conditions": [
        {
            "min_series": 1,
            "min_data_points": 2,
            "data_type": [DataType.FLOAT32, DataType.FLOAT64],
        }
    ],
    "parameters": [
        {
            "name": "percentile",
            "type": ModuleParameterType.FLOAT64,
            "range": {
                "lower": 0,
                "upper": 1,
            },
            "default": 0.75,
            "helpText": "Percentile sets the upper limit of the range for calculating the IQR for jumps.",
        },
        {
            "name": "scale",
            "type": ModuleParameterType.FLOAT64,
            "range": {
                "lower": 0,
            },
            "default": 3,
            "helpText": "Scale sets the factor for considering a jump frame an anomaly.",
        },
        {
            "name": "sensitivity",
            "type": ModuleParameterType.HIDDEN,
            "range": {
                "lower": 0,
                "upper": 1,
            },
            "default": 0.75,
            "helpText": "Sensitivity influences the range for the IQR calculation for jumps.",
        },
    ],
    "signature": "univariate",
}


def _get_relevant_jumps(
    values: pd.Series,
    jump_up_sketch: DDSketch,
    jump_down_sketch: DDSketch,
    analysis_input: AnalysisInput,
) -> tuple[pd.Series, pd.Series]:
    cutoff = get_cutoff_for_sketch(jump_up_sketch, analysis_input)
    up_jumps = values > cutoff
    up_jumps = up_jumps | shift(up_jumps, -1, cval=False)

    cutoff = get_cutoff_for_sketch(jump_down_sketch, analysis_input, direction="lower")
    down_jumps = values < cutoff
    down_jumps = down_jumps | shift(down_jumps, -1, cval=False)

    return up_jumps, down_jumps


def _get_intervals(
    outliers: pd.Series, df: pd.DataFrame, event_type: str
) -> pd.DataFrame:
    if outliers is None:
        return pd.DataFrame()
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


def _clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    return df[~df.index.duplicated(keep="first")].dropna().sort_index()


def _run_jump_check(
    analysis_input: AnalysisInput,
    jump_up_sketch: DDSketch,
    jump_down_sketch: DDSketch,
) -> tuple[list[EventFrame], pd.Timestamp | None]:
    df = _clean_dataframe(analysis_input.data)

    value_diff = df["value"].diff()

    active_points_upwards, active_points_downwards = _get_relevant_jumps(
        value_diff, jump_up_sketch, jump_down_sketch, analysis_input
    )

    intervals_downwards = _get_intervals(
        active_points_downwards, df, "Jump outlier (downwards)"
    )
    intervals_downwards = handle_open_intervals(df, intervals_downwards)

    intervals_upwards = _get_intervals(
        active_points_upwards, df, "Jump outlier (upwards)"
    )
    intervals_upwards = handle_open_intervals(df, intervals_upwards)

    all_intervals = pd.concat([intervals_downwards, intervals_upwards])

    frames = event_frames_from_dataframe(process_open_intervals(all_intervals))

    last_analyzed_point = None
    if len(df) > 1:
        last_analyzed_point = df.index[-2].to_pydatetime()

    return list(frames), last_analyzed_point


def _get_relevant_statistic(analysis_input: AnalysisInput, stat_name: str) -> Any:
    statistics = [
        statistic.result
        for statistic in analysis_input.statistics
        if statistic.name == stat_name
    ]
    if statistics is None or len(statistics) == 0:
        return None
    return statistics[0]


def _is_valid_input(
    analysis_input: AnalysisInput, jump_up_sketch: str, jump_down_sketch: str
) -> tuple[str, bool]:
    if len(_clean_dataframe(analysis_input.data)) == 0:
        return "No clean data", False
    if jump_up_sketch is None:
        return "No jump up sketch", False
    if jump_down_sketch is None:
        return "No jump down sketch", False
    if (jsonpickle.decode(jump_up_sketch).count < 30) and (
        jsonpickle.decode(jump_down_sketch).count < 30
    ):
        return "No sufficient statistic (Jump Up Sketch and Jump Down Sketch)", False
    return "OK", True


# pylint: disable=missing-function-docstring
def run(
    analysis_input: AnalysisInput,
) -> AnalysisResult:

    json_jump_up_sketch = _get_relevant_statistic(analysis_input, "Jump Up Sketch")
    json_jump_down_sketch = _get_relevant_statistic(analysis_input, "Jump Down Sketch")

    message, is_ok = _is_valid_input(
        analysis_input, json_jump_up_sketch, json_jump_down_sketch
    )
    if not is_ok:
        return AnalysisResult(condition_message=message)

    jump_up_sketch = jsonpickle.decode(json_jump_up_sketch)
    jump_down_sketch = jsonpickle.decode(json_jump_down_sketch)

    event_frames, last_analyzed_point = _run_jump_check(
        analysis_input,
        jump_up_sketch,
        jump_down_sketch,
    )

    return AnalysisResult(
        event_frames=event_frames,
        last_analyzed_point=last_analyzed_point,
    )
