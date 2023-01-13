"""There is no change in the non-zero data for a period longer than expected based on history.

<p> This check identifies periods time where the
exact same value has been consistently recorded for a sensor. These could be indications of issues with
connectivity or offline sensors.</p>
<p><img src='../static/images/reporting/stale_data.svg'></p>
<p class="scoring-explanation">The score for this check is based on the total amount of time
where there seems to be staleness relative to the total time range of the analysis.</p>
<div class="ts-check-impact">
<p>
A series that does not put out any new measurements might be faulty or could indicate a network failure.
Failing to detect this could lead to wrong process operation when attempting to obtain a particular
interval of operation.
</p>
</div>
"""

from datetime import timedelta, datetime

import jsonpickle
import pandas as pd

from timeseer import AnalysisInput, AnalysisResult, EventFrame, ModuleParameterType

from timeseer.analysis.utils import (
    event_frames_from_dataframe,
    process_open_intervals,
    handle_open_intervals,
    get_cutoff_for_sketch,
    get_separate_active_intervals,
)

_CHECK_NAME = "Stale non-zero data (distribution)"

META = {
    "checks": [
        {
            "name": _CHECK_NAME,
            "event_frames": [_CHECK_NAME],
        }
    ],
    "conditions": [
        {
            "min_series": 1,
            "min_data_points": 2,
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
            "helpText": "Percentile sets the upper limit of the range for calculating the IQR for stale non-zero data.",
        },
        {
            "name": "scale",
            "type": ModuleParameterType.FLOAT64,
            "range": {
                "lower": 0,
            },
            "default": 3,
            "helpText": "Scale sets the factor for considering a stale non-zero data frame an anomaly.",
        },
        {
            "name": "sensitivity",
            "type": ModuleParameterType.HIDDEN,
            "range": {
                "lower": 0,
                "upper": 1,
            },
            "default": 0.75,
            "helpText": "Sensitivity influences the range for the IQR calculation for stale non-zero data.",
        },
    ],
    "signature": "univariate",
}


def _get_last_analyzed_point(
    df: pd.DataFrame, intervals: pd.DataFrame
) -> datetime | None:
    if len(df) <= 1:
        return None

    if len(intervals) == 0:
        return df.index[-2].to_pydatetime()

    if intervals.iloc[-1]["end_date"] < df.index[-2]:
        return df.index[-2].to_pydatetime()

    return intervals.iloc[-1]["start_date"].to_pydatetime()


def _is_frame_long_enough(frame, df: pd.DataFrame, delta: float) -> bool:
    end_date = frame.end_date
    if frame.end_date is None:
        end_date = df.index[-1]

    return (
        end_date.replace(tzinfo=None) - frame.start_date.replace(tzinfo=None)
    ) > timedelta(seconds=delta)


def _filter_stale_event_frames(
    all_frames: pd.DataFrame, df: pd.DataFrame, delta: float
):
    filter_iterator = filter(lambda x: _is_frame_long_enough(x, df, delta), all_frames)
    return filter_iterator


def _clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    return df[~df.index.duplicated(keep="first")].sort_index()


def _run_stale_data_check(
    analysis_input, stale_sketch
) -> tuple[list[EventFrame], datetime | None]:
    df = _clean_dataframe(analysis_input.data)

    df_copy = df.copy()
    df_copy["shifted_forward"] = df_copy["value"].shift()
    active_points = (df_copy["shifted_forward"] == df_copy["value"]) & (
        df_copy["value"] != 0
    )

    intervals = get_separate_active_intervals(df, active_points, _CHECK_NAME)
    intervals = handle_open_intervals(df, intervals)

    delta = get_cutoff_for_sketch(stale_sketch, analysis_input)
    frames = _filter_stale_event_frames(
        event_frames_from_dataframe(process_open_intervals(intervals)), df, delta
    )
    last_analyzed_point = _get_last_analyzed_point(df, intervals)

    return frames, last_analyzed_point


def _get_relevant_statistic(analysis_input: AnalysisInput, stat_name: str):
    statistics = [
        statistic.result
        for statistic in analysis_input.statistics
        if statistic.name == stat_name
    ]
    if statistics is None or len(statistics) == 0:
        return None
    return statistics[0]


def _is_valid_input(analysis_input: AnalysisInput, sketch: str) -> tuple[str, bool]:
    if len(_clean_dataframe(analysis_input.data)) < 2:
        return "No clean data", False
    if sketch is None:
        return "No stale sketch", False
    if jsonpickle.decode(sketch).count < 30:
        return "No sufficient statistic (Stale Non-zero Sketch)", False
    return "OK", True


# pylint: disable=missing-function-docstring
def run(analysis_input: AnalysisInput) -> AnalysisResult:
    json_stale_nonzero_sketch = _get_relevant_statistic(
        analysis_input, "Stale Non-zero Sketch"
    )

    message, is_ok = _is_valid_input(analysis_input, json_stale_nonzero_sketch)
    if not is_ok:
        return AnalysisResult(condition_message=message)

    stale_sketch = jsonpickle.decode(json_stale_nonzero_sketch)

    frames, last_analyzed_point = _run_stale_data_check(analysis_input, stale_sketch)
    return AnalysisResult(
        event_frames=list(frames),
        last_analyzed_point=last_analyzed_point,
    )
