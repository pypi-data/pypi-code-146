"""Replaces dictionaries created with `for` loops with dictionary comprehensions."""

from sourcery.analysis.contained_nodes import ContainedNodes
from sourcery.ast import Await, NamedExpr, Node, Return, Yield, YieldFrom
from sourcery.conditions.dependency_conditions import DependencyConditions
from sourcery.conditions.variable_usage_conditions import VariableUsageConditions
from sourcery.dsl.code_change import CodeChange
from sourcery.dsl.proposals import DSLProposer
from sourcery.engine.rule_type import RuleType
from sourcery.semantic_equivalence.semantic_types import (
    ExceptionArgsChanged,
    ExceptionTypeChanged,
    LocalChangeOnException,
    LocalValueMissing,
    SemanticDifference,
)


class DictComprehensionProposer(
    DSLProposer, DependencyConditions, VariableUsageConditions
):
    contained_nodes: ContainedNodes

    def create_code_changes(self) -> list[CodeChange]:
        return [
            CodeChange(
                pattern="""
                    ${target} = {}

                    for ${index} in ${coll}:
                        ${target}[${key}] = ${value}
                """,
                replacement="""
                    ${target} = {
                        ${key}: ${value}
                        for ${index} in ${coll}
                    }
                """,
                # TODO: once we move on to interpreted syntax, the condition
                # `self._contains_control_anchor` should be applied only to the
                # top-level `pattern`.
                condition="""
                    (
                        not self.is_accessed_later(index)
                        and not self._contains_control_anchor(index)
                        and not self._contains_control_anchor(target)
                        and not self._contains_control_anchor(key)
                        and not self._contains_control_anchor(value)
                        and not self.accesses_any_variables(
                            (index, coll, key, value),
                            target
                        )
                    )
                """,
            ),
            CodeChange(
                pattern="""
                    ${target} = {}

                    for ${index} in ${coll}:
                        if ${cond}:
                            ${target}[${key}] = ${value}
                """,
                replacement="""
                    ${target} = {
                        ${key}: ${value}
                        for ${index} in ${coll}
                        if ${cond}
                    }
                """,
                # TODO: once we move on to interpreted syntax, the condition
                # `self._contains_control_anchor` should be applied only to the
                # top-level `pattern`.
                condition="""
                    (
                        not self._contains_named_expr(cond)
                        and not self._contains_control_anchor(cond)
                        and not self._contains_control_anchor(index)
                        and not self._contains_control_anchor(target)
                        and not self._contains_control_anchor(key)
                        and not self._contains_control_anchor(value)
                        and not self.is_accessed_later(index)
                        and not self.accesses_any_variables(
                            (index, coll, key, value, cond),
                            target
                        )
                    )
                """,
            ),
        ]

    def _contains_control_anchor(self, node: Node) -> bool:
        control_anchor_types = (Await, Return, Yield, YieldFrom)
        return isinstance(node, control_anchor_types) or not self.contained_nodes[
            node
        ].isdisjoint(control_anchor_types)

    def _contains_named_expr(self, node: Node) -> bool:
        return isinstance(node, NamedExpr) or NamedExpr in self.contained_nodes[node]

    def description(self) -> str:
        return "Convert for loop into dictionary comprehension"

    def kind(self) -> RuleType:
        return RuleType.REFACTORING

    @classmethod
    def expected_semantic_differences(cls) -> set[type[SemanticDifference]]:
        return {
            LocalValueMissing,
            LocalChangeOnException,
            ExceptionTypeChanged,
            ExceptionArgsChanged,
        }
