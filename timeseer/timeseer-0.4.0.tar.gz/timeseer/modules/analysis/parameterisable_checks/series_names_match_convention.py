"""Check if series names match the provided conventions.
"""

import re

from timeseer import AnalysisInput, AnalysisResult, EventFrame, ModuleParameterType


_CHECK_NAME = "Series names match convention"

META = {
    "checks": [
        {
            "name": _CHECK_NAME,
            "event_frames": ["Series names match convention"],
            "data_type": "bool",
        }
    ],
    "conditions": [
        {
            "min_series": 1,
        }
    ],
    "parameters": [
        {
            "name": "convention",
            "type": ModuleParameterType.STRINGLIST,
            "helpText": """The series names will be validated against each regex.
                           If a series name does not adhere to any regex it will be flagged as an issue.""",
        }
    ],
    "signature": "univariate",
}


def _convention_fails(name, convention) -> bool:
    patterns = [re.compile(pattern) for pattern in convention]
    if any(re.fullmatch(pattern, name) for pattern in patterns):
        return False
    return True


def _run_series_names_match_convention(
    analysis_input: AnalysisInput,
) -> list[EventFrame]:
    name = analysis_input.metadata.series.name
    convention = analysis_input.parameters["convention"]

    event_frames: list[EventFrame] = []
    if _convention_fails(name, convention):
        event_frames.append(
            EventFrame(
                type=_CHECK_NAME,
                start_date=analysis_input.evaluation_time_range.start_date,
                end_date=None,
            )
        )
    return event_frames


def _convention_is_regex_list(convention: list[str]) -> bool:
    try:
        [re.compile(pattern) for pattern in convention]
    except re.error:
        return False
    return True


def _is_valid_input(analysis_input: AnalysisInput) -> tuple[str, bool]:
    if "convention" not in analysis_input.parameters:
        return "No convention parameter provided", False
    if not _convention_is_regex_list(analysis_input.parameters["convention"]):
        return "Convention is not a valid regex list", False
    return "OK", True


# pylint: disable=missing-function-docstring
def run(analysis_input: AnalysisInput) -> AnalysisResult:
    message, is_ok = _is_valid_input(analysis_input)
    if not is_ok:
        return AnalysisResult(condition_message=message)

    event_frames = _run_series_names_match_convention(analysis_input)

    return AnalysisResult(event_frames=event_frames)
