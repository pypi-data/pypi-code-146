"""Analysis on the variation in the archival time distribution.

<p>Overcompression is a consequence of settings in a compression algorithm that
cause the archived data to no longer represent the real system accurately. Within traditional
historians this is typically caused by setting the values for exception and/or compression too high.
Low variation in inter-archival time could indicate that the max-time for archival
is often reached.</p>
<p><img src='../static/images/reporting/flat_archival.svg'></p>
<p class="scoring-explanation">The score for this check is a simple boolean (True / False).</p>
<div class="ts-check-impact">
<p>Badly compressed data, specifically overcompression,
can lead to critical events such as upsets, safety issues and downtime.
</p>
</div>
"""

import numpy as np

import jsonpickle

from timeseer import AnalysisInput, AnalysisResult, EventFrame, ModuleParameterType
from timeseer.analysis.utils import get_percentile_based_on_sensitivity

_CHECK_NAME = "Compression - flat archival rate"
_EVENT_FRAME_NAME = "Compression - flat archival rate"

META = {
    "checks": [
        {
            "name": _CHECK_NAME,
            "event_frames": [_EVENT_FRAME_NAME],
            "data_type": "bool",
        }
    ],
    "conditions": [{"min_series": 1, "min_data_points": 1}],
    "parameters": [
        {
            "name": "sensitivity",
            "type": ModuleParameterType.HIDDEN,
            "range": {
                "lower": 0,
                "upper": 1,
            },
            "default": 0.75,
            "helpText": "Sensitivity influences the range for the IQR calculation for flat archival rate",
        },
    ],
    "signature": "univariate",
}


def _run_flat_check(analysis_input: AnalysisInput, archival_sketch) -> float:
    pct_low = 0.25
    pct_high = 0.75

    if "sensitivity" in analysis_input.parameters:
        pct_high = get_percentile_based_on_sensitivity(
            analysis_input.parameters["sensitivity"]
        )
        pct_low = 1 - pct_high

    q_low, q_high = [archival_sketch.get_quantile_value(q) for q in [pct_low, pct_high]]
    if np.isnan(q_low) or np.isnan(q_high):
        return 0
    if q_low == q_high:
        return 1
    return 0


def _get_relevant_statistic(analysis_input: AnalysisInput, stat_name: str):
    statistics = [
        statistic.result
        for statistic in analysis_input.statistics
        if statistic.name == stat_name
    ]
    if statistics is None or len(statistics) == 0:
        return None
    return statistics[0]


def _is_valid_input(archival_sketch: str) -> tuple[str, bool]:
    if archival_sketch is None:
        return "No archival sketch", False
    if jsonpickle.decode(archival_sketch).count < 30:
        return "No sufficient statistic (Archival Sketch)", False
    return "OK", True


# pylint: disable=missing-function-docstring
def run(
    analysis_input: AnalysisInput,
) -> AnalysisResult:
    json_archival_sketch = _get_relevant_statistic(analysis_input, "Archival Sketch")

    message, is_ok = _is_valid_input(json_archival_sketch)
    if not is_ok:
        return AnalysisResult(condition_message=message)

    archival_sketch = jsonpickle.decode(json_archival_sketch)

    score = _run_flat_check(analysis_input, archival_sketch)
    event_frames = []
    if score == 1:
        event_frames.append(
            EventFrame(
                type=_EVENT_FRAME_NAME,
                start_date=analysis_input.evaluation_time_range.start_date,
                end_date=None,
            )
        )

    last_analyzed_point = None
    if len(analysis_input.data) > 1:
        last_analyzed_point = analysis_input.data.index[-2].to_pydatetime()
    return AnalysisResult(
        event_frames=event_frames,
        last_analyzed_point=last_analyzed_point,
    )
