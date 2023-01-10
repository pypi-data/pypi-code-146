"""Replaces cases where deletions are made via `for` loops with comprehensions."""

from sourcery.analysis.contained_nodes import ContainedNodes
from sourcery.ast import Await, NamedExpr, Node, Return, Yield, YieldFrom
from sourcery.ast.ast import invert_condition  # pylint: disable=unused-import
from sourcery.conditions.type_conditions import TypeConditions
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


class DelComprehensionProposer(DSLProposer, TypeConditions, VariableUsageConditions):
    contained_nodes: ContainedNodes

    def create_code_changes(self) -> list[CodeChange]:
        return [
            CodeChange(
                pattern="""
                    for ${key} in ${d}.copy():
                        if ${cond}:
                            del ${d}[${key}]
                """,
                replacement="""
                    ${d} = {
                        ${key}: value
                        for ${key}, value in ${d}.items()
                        if ${invert_condition(cond)}
                    }
                """,
                # TODO: once we move on to interpreted syntax, the condition
                # `self._contains_control_anchor` should be applied only to the
                # top-level `pattern`
                condition="""
                    (
                        self.has_dict_type(d)
                        and not self._contains_control_anchor(key)
                        and not self._contains_control_anchor(cond)
                        and not self.is_accessed_later(key)
                    )
                """,
            ),
            CodeChange(
                pattern="""
                    for ${key}, ${value} in ${d}.copy().items():
                        if ${cond}:
                            del ${d}[${key}]
                """,
                replacement="""
                    ${d} = {
                        ${key}: ${value}
                        for ${key}, ${value} in ${d}.items()
                        if ${invert_condition(cond)}
                    }
                """,
                # TODO: once we move on to interpreted syntax, the condition
                # `self._contains_control_anchor` should be applied only to the
                # top-level `pattern`.
                condition="""
                    (
                        self.has_dict_type(d)
                        and not self._contains_named_expr(cond)
                        and not self._contains_control_anchor(key)
                        and not self._contains_control_anchor(value)
                        and not self._contains_control_anchor(cond)
                        and not self.is_accessed_later(key)
                        and not self.is_accessed_later(value)
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
        return "Use comprehension instead of loop using del"

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
