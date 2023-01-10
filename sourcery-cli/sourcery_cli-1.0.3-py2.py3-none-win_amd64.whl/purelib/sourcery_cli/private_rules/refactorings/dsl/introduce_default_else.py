from typing import List, Set, Type

from sourcery.ast import Assign, If, Node
from sourcery.conditions.dependency_conditions import DependencyConditions
from sourcery.conditions.variable_usage_conditions import VariableUsageConditions
from sourcery.dsl.code_change import CodeChange
from sourcery.dsl.proposals import DSLProposer
from sourcery.semantic_equivalence.semantic_types import (
    LocalChangeOnException,
    NewException,
    SemanticDifference,
)


class IntroduceDefaultElseProposer(
    DSLProposer, DependencyConditions, VariableUsageConditions
):
    def create_code_changes(self) -> List[CodeChange]:
        return [
            CodeChange(
                pattern="""
                    ${variable} = ${default|not self.writes_any_variables(default)}
                    if ${condition}:
                        ${variable} = ${
                            value|not self.accesses_any_variables(value, variable)
                        }
                """,
                replacement="""
                    if ${condition}:
                        ${variable} = ${value}
                    else:
                        ${variable} = ${default}
                """,
                top_level_condition=self.can_move_assign_into_if,
            )
        ]

    def description(self) -> str:
        return "Move setting of default value for variable into `else` branch"

    def expected_semantic_differences(self) -> Set[Type[SemanticDifference]]:
        return {LocalChangeOnException, NewException}

    def transient(self, _node: Node) -> bool:
        return True

    def can_move_assign_into_if(self, node: Node) -> bool:
        assert isinstance(node, Assign)
        target = node.targets[0]
        if_node = node.next_sibling()
        assert isinstance(if_node, If)

        return (
            not self.reads_any_variables(if_node.body[0], target)
            and self.can_be_moved_ahead_of(node, if_node.body[0])
            and not self.is_written_later(target, if_node)
        )
