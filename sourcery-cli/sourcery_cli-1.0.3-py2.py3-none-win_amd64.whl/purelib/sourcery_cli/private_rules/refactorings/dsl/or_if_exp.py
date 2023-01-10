from typing import List

from sourcery.dsl.code_change import CodeChange
from sourcery.dsl.proposals import DSLProposer
from sourcery.rules.private.refactorings.descriptions import OR_IFEXP_DESC


class OrIfExpIdentityProposer(DSLProposer):
    def create_code_changes(self) -> List[CodeChange]:
        return [
            CodeChange(pattern="${b} if ${b} else ${c}", replacement="${b} or ${c}")
        ]

    def description(self) -> str:
        return OR_IFEXP_DESC
