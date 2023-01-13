"""There is a much longer period between data being recorded than expected based on history.

<p>This check identifies periods of time where no data
has been archived. These could be indications of issues with
connectivity or offline sensors.</p>
<p class="scoring-explanation">The score for this check is based on the total amount of time
where there seems to be gaps relative to the total time range of the analysis.</p>
<div class="ts-check-impact">
<p>
A series that does not put out any data might be faulty or could indicate a network failure.
Failing to detect this could lead to wrong process operation when attempting to obtain a particular
interval of operation.
</p>
</div>
"""

from datetime import datetime

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

_CHECK_NAME = "Increased archival step size"

META = {
    "checks": [
        {
            "name": _CHECK_NAME,
            "event_frames": ["Increased archival step size"],
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
            "helpText": "Percentile sets the upper limit of the range for calculating the IQR of the archival steps.",
        },
        {
            "name": "scale",
            "type": ModuleParameterType.FLOAT64,
            "range": {
                "lower": 0,
            },
            "default": 3,
            "helpText": "Scale sets the factor for considering an archival step frame an anomaly.",
        },
        {
            "name": "sensitivity",
            "type": ModuleParameterType.HIDDEN,
            "range": {
                "lower": 0,
                "upper": 1,
            },
            "default": 0.75,
            "helpText": "Sensitivity influences the range for the IQR calculation of the archival steps.",
        },
    ],
    "signature": "univariate",
}


def _clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    return df[~df.index.duplicated(keep="first")].sort_index()


def _run_gap_check(
    analysis_input: AnalysisInput, stale_sketch
) -> tuple[list[EventFrame], datetime | None]:
    df = _clean_dataframe(analysis_input.data)
    delta = get_cutoff_for_sketch(stale_sketch, analysis_input)

    active_points = (df.index.to_series().diff()).dt.total_seconds() > delta

    intervals = get_separate_active_intervals(df, active_points, _CHECK_NAME)
    intervals = handle_open_intervals(df, intervals)

    frames = event_frames_from_dataframe(process_open_intervals(intervals))

    last_analyzed_point = None
    if len(df) > 1:
        last_analyzed_point = df.index[-2].to_pydatetime()

    return list(frames), last_analyzed_point


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
        return "No archival sketch", False
    if jsonpickle.decode(sketch).count < 30:
        return "No sufficient statistic (Archival Sketch)", False
    return "OK", True


# pylint: disable=missing-function-docstring
def run(
    analysis_input: AnalysisInput,
) -> AnalysisResult:
    json_archival_sketch = _get_relevant_statistic(analysis_input, "Archival Sketch")

    message, is_ok = _is_valid_input(analysis_input, json_archival_sketch)
    if not is_ok:
        return AnalysisResult(condition_message=message)

    archival_sketch = jsonpickle.decode(json_archival_sketch)

    frames, last_analyzed_point = _run_gap_check(analysis_input, archival_sketch)

    return AnalysisResult(
        event_frames=frames,
        last_analyzed_point=last_analyzed_point,
    )
