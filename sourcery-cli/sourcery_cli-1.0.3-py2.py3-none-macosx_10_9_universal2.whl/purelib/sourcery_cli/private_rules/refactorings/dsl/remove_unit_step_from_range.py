from typing import List

from sourcery.dsl.code_change import CodeChange
from sourcery.dsl.proposals import DSLProposer
from sourcery.rules.private.refactorings.descriptions import RANGE_STEP_DESC


class RemoveUnitStepFromRangeProposer(DSLProposer):
    def create_code_changes(self) -> List[CodeChange]:
        return [
            CodeChange(pattern="range(${a}, ${b}, 1)", replacement="range(${a}, ${b})")
        ]

    def description(self) -> str:
        return RANGE_STEP_DESC
