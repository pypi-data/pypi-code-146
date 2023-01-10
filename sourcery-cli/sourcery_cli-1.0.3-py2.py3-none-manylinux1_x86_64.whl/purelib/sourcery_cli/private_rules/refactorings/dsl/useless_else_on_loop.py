from typing import List

from sourcery.ast import For, Node, While
from sourcery.conditions.dependency_conditions import DependencyConditions
from sourcery.dsl.code_change import CodeChange
from sourcery.dsl.proposals import DSLProposer
from sourcery.rules.private.refactorings.descriptions import ELSE_ON_LOOP_DESC


class UselessElseOnLoopProposer(DSLProposer, DependencyConditions):
    def create_code_changes(self) -> List[CodeChange]:
        return [
            CodeChange(
                pattern="""
                    for ${item} in ${collection}:
                      ${statements+}
                    else:
                      ${else_statements+}
                """,
                replacement="""
                    for ${item} in ${collection}:
                      ${statements}
                    ${else_statements}
                """,
                top_level_condition=lambda node: not self.loop_with_break(node),
            ),
            CodeChange(
                pattern="""
                    while ${test}:
                      ${statements+}
                    else:
                      ${else_statements+}
                """,
                replacement="""
                    while ${test}:
                      ${statements}
                    ${else_statements}
                """,
                top_level_condition=lambda node: not self.loop_with_break(node),
            ),
        ]

    def loop_with_break(self, node: Node):
        return isinstance(
            node, (For, While)
        ) and self.contains_break_loop_control_anchor(node)

    def description(self) -> str:
        return ELSE_ON_LOOP_DESC
