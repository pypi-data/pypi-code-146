from typing import List

from sourcery.ast.ast import invert_condition  # pylint: disable=unused-import
from sourcery.dsl.code_change import CodeChange
from sourcery.dsl.proposals import DSLProposer
from sourcery.rules.private.refactorings.descriptions import REMOVE_PASS_BODY_DESC


class RemovePassBodyProposer(DSLProposer):
    def create_code_changes(self) -> List[CodeChange]:
        return [
            CodeChange(
                pattern="""
                    if ${test}:
                        pass
                    else:
                        ${statements+}
                """,
                replacement="""
                    if ${invert_condition(test)}:
                        ${statements}
                """,
            )
        ]

    def description(self) -> str:
        return REMOVE_PASS_BODY_DESC
