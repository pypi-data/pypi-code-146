"""Analysis on the variation in the archival time distribution per value range.

<p>Overcompression is a consequence of settings in a compression algorithm that
cause the archived data to no longer represent the real system accurately. Within traditional
historians this is typically caused by setting too high values for exception and/or compression.
A significant difference in median inter-archival time between normal values and extreme could indicate
issues with the compression parameters.</p>
<p><img src='../static/images/reporting/value_archival.svg'></p>
<p class="scoring-explanation">The score for this check is a simple boolean (True / False).</p>
<div class="ts-check-impact">
<p>Badly compressed data, specifically overcompression,
can lead to critical events such as upsets, safety issues and downtime.
</p>
</div>
"""

from typing import Any

import jsonpickle

from ddsketch.ddsketch import DDSketch

import timeseer
from timeseer import (
    AnalysisResult,
    DataType,
    EventFrame,
    ModuleParameterType,
    AnalysisInput,
)
from timeseer.analysis.utils import get_percentile_based_on_sensitivity

_CHECK_NAME = "Compression - value dependent archival rate"
_EVENT_FRAME_NAME = "Compression - value dependent archival rate"

META = {
    "checks": [
        {"name": _CHECK_NAME, "data_type": "bool", "event_frames": [_EVENT_FRAME_NAME]}
    ],
    "conditions": [
        {
            "min_series": 1,
            "min_weeks": 1,
            "min_data_points": 300,
            "data_type": [DataType.FLOAT32, DataType.FLOAT64],
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
            "helpText": "Sensitivity influences the range for the IQR calculation for value dependent archival rate.",
        },
    ],
    "signature": "univariate",
}


def _run_value_dependent_archival_check(
    analysis_input: AnalysisInput, extremes_sketch: DDSketch, base_sketch: DDSketch
) -> bool:
    pct_low = 0.25
    pct_high = 0.75

    if "sensitivity" in analysis_input.parameters:
        pct_high = get_percentile_based_on_sensitivity(
            analysis_input.parameters["sensitivity"]
        )
        pct_low = 1 - pct_high

    extremes_q25, extremes_q75 = [
        extremes_sketch.get_quantile_value(q) for q in [pct_low, pct_high]
    ]
    base_q25, base_q75 = [
        base_sketch.get_quantile_value(q) for q in [pct_low, pct_high]
    ]
    if not (base_q25 > extremes_q75 or extremes_q25 > base_q75):
        return False
    return True


def _get_relevant_statistic(
    analysis_input: timeseer.AnalysisInput, stat_name: str
) -> Any:
    statistics = [
        statistic.result
        for statistic in analysis_input.statistics
        if statistic.name == stat_name
    ]
    if statistics is None or len(statistics) == 0:
        return None
    return jsonpickle.decode(statistics[0])


def _is_valid_input(
    base_sketch: DDSketch,
    extremes_sketch: DDSketch,
) -> tuple[str, bool]:
    if extremes_sketch is None:
        return "No extreme archival sketch", False
    if extremes_sketch.count < 30:
        return "No sufficient statistic (Extremes Archival Sketch)", False
    if base_sketch is None:
        return "No base archival sketch", False
    if base_sketch.count < 30:
        return "No sufficient statistic (Base Archival Sketch)", False
    return "Ok", True


# pylint: disable=missing-function-docstring
def run(
    analysis_input: timeseer.AnalysisInput,
) -> timeseer.AnalysisResult:
    extremes_sketch = _get_relevant_statistic(
        analysis_input, "Extremes Archival Sketch"
    )
    base_sketch = _get_relevant_statistic(analysis_input, "Base Archival Sketch")

    message, is_ok = _is_valid_input(base_sketch, extremes_sketch)
    if not is_ok:
        return AnalysisResult(condition_message=message)

    score = _run_value_dependent_archival_check(
        analysis_input, extremes_sketch, base_sketch
    )
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
