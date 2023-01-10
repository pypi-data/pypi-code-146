from typing import List

from sourcery.analysis.node_statements import NodeStatements
from sourcery.ast import If, Node
from sourcery.ast.ast import breaks_flow  # pylint: disable=unused-import
from sourcery.dsl.code_change import CodeChange
from sourcery.dsl.proposals import DSLProposer
from sourcery.rules.private.refactorings.descriptions import REMOVE_ELSE_AFTER_GUARD


class RemoveUnnecessaryElseProposer(DSLProposer):
    node_statements: NodeStatements

    def create_code_changes(self) -> List[CodeChange]:
        return [
            CodeChange(
                pattern="""
                    if ${condition}:
                      ${stmt|breaks_flow(stmt)}
                    else:
                      ${orelse+}
                """,
                replacement="""
                    if ${condition}:
                      ${stmt}
                    ${orelse}
                """,
                # This ensures it is not the direct opposite of reintroduce-else
                top_level_condition=self.multiple_statements,
            )
        ]

    def description(self) -> str:
        return REMOVE_ELSE_AFTER_GUARD

    def multiple_statements(self, node: Node) -> bool:
        return isinstance(node, If) and self.node_statements[node.orelse] > 1
