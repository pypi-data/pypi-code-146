""" Check if the unit has a dimension that matches flow"""


from timeseer import AnalysisInput, AnalysisResult, EventFrame
from timeseer.analysis.utils.unit_dimension_match import unit_not_matching_dimension


_CHECK_NAME = "flow unit dimension"
_EVENT_FRAME_NAME = "Unit not matching flow"

META = {
    "checks": [
        {
            "name": _CHECK_NAME,
            "event_frames": [_EVENT_FRAME_NAME],
            "data_type": "bool",
        }
    ],
    "conditions": [
        {
            "min_series": 1,
            "min_data_points": 1,
        }
    ],
    "signature": "univariate",
}


# pylint: disable=missing-function-docstring
def run(
    analysis_input: AnalysisInput,
) -> AnalysisResult:

    parameters = {}
    parameters["value"] = "[mass]/[time]"
    analysis_input.parameters = parameters
    mass_results = unit_not_matching_dimension.run(analysis_input)
    parameters["value"] = "[volume]/[time]"
    analysis_input.parameters = parameters
    volume_results = unit_not_matching_dimension.run(analysis_input)
    check_fail = bool(len(mass_results.event_frames) * len(volume_results.event_frames))
    event_frames = []
    if check_fail:
        event_frames.append(
            EventFrame(
                type=_EVENT_FRAME_NAME,
                start_date=analysis_input.evaluation_time_range.start_date,
                end_date=None,
            )
        )

    return AnalysisResult(event_frames=event_frames)
