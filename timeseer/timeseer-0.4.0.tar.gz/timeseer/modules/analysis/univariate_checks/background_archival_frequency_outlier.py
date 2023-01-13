"""Frequency of sampling / archival rate should remain (quasi) constant.

<p>In general the variation in most processes remains reasonably stable.
Under stable conditions the inter-archival time should also remain similar.
Sensor issues could cause archival rate to become more fluctuant.</p>
<p><img src='../static/images/reporting/frequency.svg'></p>
<p class="scoring-explanation">The score of this check is calculated based on the sum of time of all
the event-frames in which the archival frequency is considered an outlier compared to the overall mean
time between archivals.
E.g. assume a total period being
analyzed of 1 year and 2 event-frames of 1 month and 2 months respectively. The score of this check
will then be 75% = 1 - 3 / 12. Which means that in 75% of time no variance drift is detected.</p>
<div class="ts-check-impact">
<p>
Frequency changes in archival rate might be caused by changing compression settings which could
lead to an infidel representation of the system. Another possibility is temporary disconnects or outages
of the sensor / network.
This could also be caused by network attacks where data is being manipulated before going to the historian.
</p>
</div>
"""

from datetime import timedelta, datetime

import jsonpickle
import pandas as pd

from ddsketch.ddsketch import DDSketch

from timeseer import AnalysisInput, AnalysisResult, EventFrame, ModuleParameterType

from timeseer.analysis.utils import (
    event_frames_from_dataframe,
    process_open_intervals,
    handle_open_intervals,
    get_cutoff_for_sketch,
)

_CHECK_NAME = "Consistent background archival frequency"

META = {
    "checks": [
        {
            "name": _CHECK_NAME,
            "event_frames": ["Background frequency outlier"],
        }
    ],
    "conditions": [
        {
            "min_series": 1,
            "min_weeks": 4,
            "min_data_points": 300,
        }
    ],
    "parameters": [
        {
            "name": "sensitivity",
            "type": ModuleParameterType.HIDDEN,
            "range": {
                "lower": 0,
                "upper": 1,
            },
            "default": 0.75,
            "helpText": "Sensitivity influences the range for the IQR calculation of the background frequency outlier.",
        },
    ],
    "signature": "univariate",
}


def _get_median_diff_times(df: pd.DataFrame) -> pd.Series:
    # If only one value in a day, we assume 1 sample per day
    if len(df) <= 1:
        return 24 * 60 * 60

    meas_times = df.index.to_series()
    diff_times = meas_times - meas_times.shift()
    diff_times = diff_times.dropna()
    diff_times = diff_times.apply(timedelta.total_seconds)
    return diff_times.median()


def _get_daily_diff_times(df: pd.DataFrame):
    resampled_daily_diff_medians = df.resample("1D").apply(_get_median_diff_times)
    return resampled_daily_diff_medians


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
    outlier_intervals["end_date"] = outlier_intervals["end_date"] + timedelta(days=1)
    outlier_intervals["type"] = event_type
    return outlier_intervals


def _clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    return df[~df.index.duplicated(keep="first")].dropna().sort_index()


def _run_frequency_inconsistency_check(
    analysis_input: AnalysisInput, archival_sketch
) -> tuple[list[EventFrame], datetime]:
    df = _clean_dataframe(analysis_input.data)
    df_daily = df.resample("1D").mean()

    diff_times_resampled = _get_daily_diff_times(df)["value"].values

    outliers = (
        diff_times_resampled > get_cutoff_for_sketch(archival_sketch, analysis_input)
    ) | (
        diff_times_resampled
        < get_cutoff_for_sketch(archival_sketch, analysis_input, "lower")
    )

    intervals = _get_intervals(
        outliers, df.resample("D").asfreq(), "Background frequency outlier"
    )
    intervals = handle_open_intervals(df_daily, intervals)

    all_frames = event_frames_from_dataframe(process_open_intervals(intervals))

    last_analyzed_point = df_daily.index[-1]

    return list(all_frames), last_analyzed_point.to_pydatetime()


def _is_valid_input(
    analysis_input: AnalysisInput, archival_sketch: DDSketch
) -> tuple[str, bool]:
    if len(_clean_dataframe(analysis_input.data)) == 0:
        return "No clean data", False
    if archival_sketch is None:
        return "No archival sketch", False
    if archival_sketch.count < 30:
        return "No sufficient statistic (Archival Sketch)", False
    return "OK", True


def _get_relevant_statistic(analysis_input: AnalysisInput, stat_name: str):
    statistics = [
        statistic.result
        for statistic in analysis_input.statistics
        if statistic.name == stat_name
    ]
    if statistics is None or len(statistics) == 0:
        return None
    if statistics[0] is None:
        return None
    return jsonpickle.decode(statistics[0])


# pylint: disable=missing-function-docstring
def run(
    analysis_input: AnalysisInput,
) -> AnalysisResult:
    archival_sketch = _get_relevant_statistic(analysis_input, "Archival Sketch")
    message, is_ok = _is_valid_input(analysis_input, archival_sketch)
    if not is_ok:
        return AnalysisResult(condition_message=message)

    frames, last_analyzed_point = _run_frequency_inconsistency_check(
        analysis_input, archival_sketch
    )

    return AnalysisResult(event_frames=frames, last_analyzed_point=last_analyzed_point)
