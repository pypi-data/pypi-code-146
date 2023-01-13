"""Timeseer score module to generate scores for metadata checks.

Scores for metadata checks are calculated based on their metadata group.
If one score indicates a failure, the total score will be a failure.
"""

from collections import defaultdict
from typing import List

from timeseer import CheckResult, ScoreInput, ScoreOutput, ScoreResult

META = {
    "scores": [
        dict(
            name="Description",
            data_type="bool",
            checks=[
                dict(group="Description"),
            ],
        ),
        dict(
            name="Interpolation type",
            data_type="bool",
            checks=[
                dict(group="Interpolation type"),
            ],
        ),
        dict(
            name="Limits - Physical",
            data_type="bool",
            checks=[
                dict(group="Limits - Physical"),
            ],
        ),
        dict(
            name="Limits - Functional",
            data_type="bool",
            checks=[
                dict(group="Limits - Functional"),
            ],
        ),
        dict(
            name="Unit - Physical",
            data_type="bool",
            checks=[
                dict(group="Unit - Physical"),
            ],
        ),
        dict(
            name="Unit - Functional",
            data_type="bool",
            checks=[
                dict(group="Unit - Functional"),
            ],
        ),
        dict(
            name="Data types",
            data_type="bool",
            checks=[
                dict(group="Data types"),
            ],
        ),
        dict(
            name="Accuracy",
            data_type="bool",
            checks=[
                dict(group="Accuracy"),
            ],
        ),
        dict(
            name="Dictionary",
            data_type="bool",
            checks=[
                dict(group="Dictionary"),
            ],
        ),
    ],
}


def _calculate_score(results: List[CheckResult]) -> float:
    return max(result.result for result in results)


# pylint: disable=missing-function-docstring
def score(
    score_input: ScoreInput,
) -> ScoreOutput:
    metadata_lookup = {meta.name: meta for meta in score_input.check_metadata}

    by_group = defaultdict(list)
    for result in score_input.check_results:
        metadata = metadata_lookup[result.name]
        if metadata.group is None:
            continue
        by_group[metadata.group].append(result)
    scores = []
    for group_name, group_results in by_group.items():
        scores.append(ScoreResult(group_name, _calculate_score(group_results)))
    return ScoreOutput(scores)
