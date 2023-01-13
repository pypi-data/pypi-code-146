"""The unit should match the dimension (or unit) of the property given as input.
input can be given as unit (e.g. 'fahrenheit', 'mm^3/s') or as the name of property
in brackets (e.g. '[temperature]', '[pressure]')

"""


from pint import UnitRegistry
from pint import UndefinedUnitError, DefinitionSyntaxError
from pint.util import UnitsContainer


from timeseer import AnalysisInput, AnalysisResult, DataType, EventFrame
from timeseer.metadata import fields
from timeseer.analysis.utils import get_unit_registry


_CHECK_NAME = "Unit not matching dimension"
_EVENT_FRAME_NAME = "Unit not matching dimension"

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
            "data_type": [DataType.STRING],
        }
    ],
    "signature": "univariate",
}


def _is_valid_input(
    analysis_input: AnalysisInput, ureg: UnitRegistry
) -> tuple[str, bool]:
    if "value" not in analysis_input.parameters:
        return "No value parameter provided", False
    value = analysis_input.parameters["value"]
    try:
        ureg.get_dimensionality(value)
        return "OK", True
    except (
        UndefinedUnitError,
        AttributeError,
        TypeError,
        ValueError,
        KeyError,
        DefinitionSyntaxError,
    ):
        return "invalid reference value", False


def _get_reference_dimension(
    analysis_input: AnalysisInput, ureg: UnitRegistry
) -> UnitsContainer:
    value = analysis_input.parameters["value"]
    return ureg.get_dimensionality(value)


def _get_unit_dimension(
    analysis_input: AnalysisInput, ureg: UnitRegistry
) -> UnitsContainer:
    unit = analysis_input.metadata.get_field(fields.Unit)
    if "%" in unit:
        return ureg.get_dimensionality("[]")
    return ureg.get_dimensionality(unit)


# pylint: disable=missing-function-docstring
def run(
    analysis_input: AnalysisInput,
) -> AnalysisResult:
    ureg = get_unit_registry()
    message, is_ok = _is_valid_input(analysis_input, ureg)
    if not is_ok:
        return AnalysisResult(condition_message=message)
    event_frames = []
    try:
        unit_dimension = _get_unit_dimension(analysis_input, ureg)
        reference_dimension = _get_reference_dimension(analysis_input, ureg)
        check_fail = unit_dimension != reference_dimension
    except (
        UndefinedUnitError,
        AttributeError,
        TypeError,
        ValueError,
        KeyError,
        DefinitionSyntaxError,
    ):
        check_fail = True

    if check_fail:
        event_frames.append(
            EventFrame(
                type=_EVENT_FRAME_NAME,
                start_date=analysis_input.evaluation_time_range.start_date,
                end_date=None,
            )
        )

    return AnalysisResult(event_frames=event_frames)
