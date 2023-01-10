from typing import List

from sourcery.dsl.code_change import CodeChange
from sourcery.dsl.proposals import DSLProposer
from sourcery.rules.private.refactorings.descriptions import RANGE_ZERO_DESC


class RemoveZeroFromRangeProposer(DSLProposer):
    def create_code_changes(self) -> List[CodeChange]:
        return [CodeChange(pattern="range(0, ${x})", replacement="range(${x})")]

    def description(self) -> str:
        return RANGE_ZERO_DESC
