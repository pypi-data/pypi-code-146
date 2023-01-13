"""Identification of outlier based on inter-quartile range (IQR).

<p>This check is a traditional method for outliers where values are flagged
as anomalies if they are outside of a range defined by [q1 - 1.5 * iqr, q3 + 1.5 * iqr].
Here q1, q3 and iqr stand for 25th, 75th percentile and inter-quartile range (=q3-q1) respectively.</p>
<p><img src='../static/images/reporting/iqr.svg'></p>
<p class="scoring-explanation">The score of this check is calculated based on the count of all
points where an IQR outlier occurs. Imagine that 100 points are analyzed in a given time-frame
and there are 7 outliers. The score for this check in that case would be
93% = 1 - 7 / 100. Which means that 93% of all points are not outliers.</p>
<div class="ts-check-impact">
<p>
Outliers in series can cloud downstream analytics and put the burden of removing these without
background knowledge on the algorithms instead of those in the know.
Several calculations are sensitive to these type of sudden changes and process decision chains
based on such an outlier can propagate through the system.
Any type of anomaly detection based on normal behavior of the phyiscal sensor can act as a guide for
prioritization of callibration / maintenance.
</p>
</div>
"""

from datetime import timedelta, datetime

import jsonpickle
import pandas as pd

from timeseer import (
    AnalysisInput,
    AnalysisResult,
    DataType,
    EventFrame,
    ModuleParameterType,
)
from timeseer.analysis.utils import (
    event_frames_from_dataframe,
    process_open_intervals,
    handle_open_intervals,
    get_cutoff_for_sketch,
)

_CHECK_NAME = "IQR Anomaly"

META = {
    "checks": [
        {
            "name": _CHECK_NAME,
            "event_frames": ["IQR Anomaly"],
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
            "name": "percentile",
            "type": ModuleParameterType.FLOAT64,
            "range": {
                "lower": 0,
                "upper": 1,
            },
            "default": 0.75,
            "helpText": "Percentile sets the upper limit of the range for calculating the values IQR.",
        },
        {
            "name": "scale",
            "type": ModuleParameterType.FLOAT64,
            "range": {
                "lower": 0,
            },
            "default": 3,
            "helpText": "Scale sets the factor for considering a value an IQR Anomaly.",
        },
        {
            "name": "sensitivity",
            "type": ModuleParameterType.HIDDEN,
            "range": {
                "lower": 0,
                "upper": 1,
            },
            "default": 0.75,
            "helpText": "Sensitivity influences the range for the IQR calculation.",
        },
    ],
    "signature": "univariate",
}


def _calculate_total_check_active_time(
    frames: pd.DataFrame, median_archival_step: float
) -> timedelta:
    active_time = timedelta(0)
    for _, row in frames.iterrows():
        length = row["end_date"] - row["start_date"]
        if length == timedelta(0):
            length = timedelta(seconds=median_archival_step)
        active_time = active_time + length
    return active_time


def _get_intervals(
    anomalies: pd.Series, df: pd.DataFrame, event_type: str
) -> pd.DataFrame:
    interval_grp = (anomalies != anomalies.shift().bfill()).cumsum()
    intervals = (
        df.assign(interval_grp=interval_grp)[anomalies]
        .reset_index()
        .groupby(["interval_grp"])
        .agg(start_date=("ts", "first"), end_date=("ts", "last"))
    )
    intervals["type"] = event_type
    return intervals


def _clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    return df[~df.index.duplicated(keep="first")].dropna().sort_index()


def _run_iqr_ad(
    analysis_input: AnalysisInput,
    sketch,
) -> tuple[list[EventFrame], datetime | None]:
    df = _clean_dataframe(analysis_input.data)

    cutoff_low = get_cutoff_for_sketch(sketch, analysis_input, direction="lower")
    cutoff_high = get_cutoff_for_sketch(sketch, analysis_input)
    active_points = (df["value"] < cutoff_low) | (df["value"] > cutoff_high)

    intervals = _get_intervals(active_points, df, _CHECK_NAME)
    intervals = handle_open_intervals(df, intervals)

    all_frames = event_frames_from_dataframe(process_open_intervals(intervals))

    last_analyzed_point = None
    if len(df) > 1:
        last_analyzed_point = df.index[-2].to_pydatetime()

    return list(all_frames), last_analyzed_point


def _get_relevant_statistic(analysis_input, stat_name):
    statistics = [
        statistic.result
        for statistic in analysis_input.statistics
        if statistic.name == stat_name
    ]
    if statistics is None or len(statistics) == 0:
        return None
    return statistics[0]


def _is_relevant_open_event_frame(event_frame):
    return (
        event_frame.end_date is None
        and event_frame.type in META["checks"][0]["event_frames"]
    )


def _get_open_event_frames(
    analysis_input: AnalysisInput,
) -> list[EventFrame]:
    return [
        frame
        for frame in analysis_input.event_frames
        if _is_relevant_open_event_frame(frame)
    ]


def _is_valid_input(data: pd.DataFrame, sketch: str) -> tuple[str, bool]:
    if len(_clean_dataframe(data)) == 0:
        return "No clean data", False
    if sketch is None:
        return "No value sketch", False
    if jsonpickle.decode(sketch).count < 30:
        return "No sufficient statistic (Value Sketch)", False
    return "OK", True


# pylint: disable=missing-function-docstring
def run(analysis_input: AnalysisInput) -> AnalysisResult:
    json_value_sketch = _get_relevant_statistic(analysis_input, "Value Sketch")

    message, is_ok = _is_valid_input(analysis_input.data, json_value_sketch)
    if not is_ok:
        return AnalysisResult(condition_message=message)

    value_sketch = jsonpickle.decode(json_value_sketch)

    frames, last_analyzed_point = _run_iqr_ad(analysis_input, value_sketch)
    return AnalysisResult(
        event_frames=frames,
        last_analyzed_point=last_analyzed_point,
    )
