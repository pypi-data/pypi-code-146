"""For certain units (e.g. pH) there is a limited range values can take.

<p>This check validates whether for a specific set of units, the configured limits fall
within the expected deterministic range.</p>
<p class="scoring-explanation">The score for this checks is a simple boolean (True / False).</p>
<div class="ts-check-impact">
<p>Mismatches between unit range and physical limits are data hygiene bugs.
</p>
</div>
"""

from enum import Enum, auto
from typing import Optional

from timeseer import AnalysisInput, AnalysisResult, DataType, EventFrame
from timeseer.analysis.utils import (
    get_dimension,
    get_symbol,
    get_limited_units,
    get_unit_range,
)
from timeseer.metadata import fields

_FUNCTIONAL_CHECK_NAME = "Limits inconsistent with unit (functional)"
_PHYSICAL_CHECK_NAME = "Limits inconsistent with unit (physical)"
_FUNCTIONAL_EVENT_FRAME_NAME = "Limits inconsistent with unit (functional)"
_PHYSICAL_EVENT_FRAME_NAME = "Limits inconsistent with unit (physical)"

META = {
    "checks": [
        {
            "name": _FUNCTIONAL_CHECK_NAME,
            "group": "Unit - Functional",
            "event_frames": [_FUNCTIONAL_EVENT_FRAME_NAME],
            "data_type": "bool",
        },
        {
            "name": _PHYSICAL_CHECK_NAME,
            "group": "Unit - Physical",
            "event_frames": [_PHYSICAL_EVENT_FRAME_NAME],
            "data_type": "bool",
        },
    ],
    "conditions": [
        {
            "min_series": 1,
            "min_weeks": 1,
            "min_data_points": 300,
            "data_type": [DataType.FLOAT32, DataType.FLOAT64],
        }
    ],
    "signature": "univariate",
}


class LimitType(Enum):
    """Choose whether to use physical or functional limits."""

    PHYSICAL = auto()
    FUNCTIONAL = auto()


def _limit_settings_outside_range(
    analysis_input: AnalysisInput,
    limit_type: LimitType,
    min_value: float,
    max_value: float,
) -> Optional[bool]:
    if limit_type == LimitType.PHYSICAL:
        limit_low = analysis_input.metadata.get_field(fields.LimitLowPhysical)
        limit_high = analysis_input.metadata.get_field(fields.LimitHighPhysical)
    else:
        limit_low = analysis_input.metadata.get_field(fields.LimitLowFunctional)
        limit_high = analysis_input.metadata.get_field(fields.LimitHighFunctional)
    if limit_low and limit_low < min_value:
        return True
    if limit_high and limit_high > max_value:
        return True
    if not (limit_low or limit_high):
        return None
    return False


def _run_values_outside_unit_range_check(
    unit, analysis_input: AnalysisInput, limit_type: LimitType
) -> Optional[bool]:
    min_value, max_value = get_unit_range(unit)
    return _limit_settings_outside_range(
        analysis_input, limit_type, min_value=min_value, max_value=max_value
    )


def _is_valid_input(unit: str) -> tuple[str, bool]:
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
    message, is_ok = _is_valid_input(unit)
    if not is_ok:
        return AnalysisResult(condition_message=message)

    event_frames = []
    functional_score = _run_values_outside_unit_range_check(
        unit, analysis_input, LimitType.FUNCTIONAL
    )
    if functional_score is not None and functional_score is True:
        event_frames.append(
            EventFrame(
                type=_FUNCTIONAL_EVENT_FRAME_NAME,
                start_date=analysis_input.evaluation_time_range.start_date,
                end_date=None,
            )
        )

    physical_score = _run_values_outside_unit_range_check(
        unit, analysis_input, LimitType.PHYSICAL
    )

    if physical_score is not None and physical_score is True:
        event_frames.append(
            EventFrame(
                type=_PHYSICAL_EVENT_FRAME_NAME,
                start_date=analysis_input.evaluation_time_range.start_date,
                end_date=None,
            )
        )

    return AnalysisResult(event_frames=event_frames)
