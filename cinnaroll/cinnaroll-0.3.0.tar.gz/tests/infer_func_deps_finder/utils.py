# asserts that got contains every non-empty line from expect and only them, groups assertion errors into one
from copy import copy
from typing import List


def assert_lines_of_string_in_string(expect: str, got: str) -> None:
    expected_lines = get_non_empty_lines_from_string(expect)
    got_lines = get_non_empty_lines_from_string(got)
    not_found_lines: List[str] = []
    extra_lines = copy(got_lines)

    for line in expected_lines:
        if line in got_lines:
            extra_lines.remove(line)
        else:
            not_found_lines.append(line)

    error_msg = (
        f"The following expected lines were not found in resulting string: {not_found_lines}\n"
        f"The following unexpected lines were found in resulting string: {extra_lines}"
    )
    if len(not_found_lines) or len(extra_lines):
        raise AssertionError(error_msg)


def get_non_empty_lines_from_string(s: str) -> List[str]:
    result_lines: List[str] = []
    for line in s.split("\n"):
        if line.strip():
            result_lines.append(line)
    return result_lines
