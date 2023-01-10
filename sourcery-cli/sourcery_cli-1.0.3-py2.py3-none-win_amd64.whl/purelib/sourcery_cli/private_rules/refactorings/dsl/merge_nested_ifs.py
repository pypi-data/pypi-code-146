from typing import List

from sourcery.ast import NamedExpr, Node, contains_types
from sourcery.dsl.code_change import CodeChange
from sourcery.dsl.proposals import DSLProposer


class MergeNestedIfsProposer(DSLProposer):
    def create_code_changes(self) -> List[CodeChange]:
        return [
            CodeChange(
                pattern="""
                    if ${condition|not self.has_walrus(condition)}:
                        if ${inner_condition|not self.has_walrus(inner_condition)}:
                            ${statements+}
                """,
                replacement="""
                    if ${condition} and ${inner_condition}:
                        ${statements}
                """,
            )
        ]

    def has_walrus(self, node: Node) -> bool:
        return contains_types(node, (NamedExpr,))

    def description(self) -> str:
        return "Merge nested if conditions"
