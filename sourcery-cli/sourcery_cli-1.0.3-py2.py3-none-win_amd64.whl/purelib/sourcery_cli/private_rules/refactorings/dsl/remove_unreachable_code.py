from typing import List

from sourcery.ast.ast import breaks_flow  # pylint: disable=unused-import
from sourcery.dsl.code_change import CodeChange
from sourcery.dsl.proposals import DSLProposer
from sourcery.rules.private.refactorings.descriptions import REMOVE_UNREACHABLE_DESC


class RemoveUnreachableCodeProposer(DSLProposer):
    # TODO Think about performance impact of these:
    #  - previously this would only do anything when entering
    #    raise/continue/etc nodes
    #  - now it calls breaks_flow on every node
    def create_code_changes(self) -> List[CodeChange]:
        return [
            CodeChange(
                pattern="""
                    ${a|breaks_flow(a)}
                    ${unreachable+}
                """,
                replacement="""
                    ${a}
                """,
            )
        ]

    def description(self) -> str:
        return REMOVE_UNREACHABLE_DESC
