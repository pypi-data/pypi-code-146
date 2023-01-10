"""Replaces summed values created with `for` loops with `sum` comprehensions."""

from sourcery.analysis.contained_nodes import ContainedNodes
from sourcery.ast import Await, NamedExpr, Node, Return, Yield, YieldFrom
from sourcery.conditions.dependency_conditions import DependencyConditions
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

# pylint: disable=too-many-ancestors


class SumComprehensionProposer(
    DSLProposer, DependencyConditions, TypeConditions, VariableUsageConditions
):
    contained_nodes: ContainedNodes

    def create_code_changes(self) -> list[CodeChange]:
        return (
            [
                CodeChange(
                    pattern="""
                        ${target} = 0

                        for ${index} in ${coll}:
                            ${target} += ${value}
                    """,
                    replacement="""
                        ${target} = sum(${value} for ${index} in ${coll})
                    """,
                    # TODO: once we move on to interpreted syntax, the condition
                    # `self._contains_control_anchor` should be applied only to the
                    # top-level `pattern`.
                    condition="""
                        (
                            not self.is_in_scope_of("sum", target)
                            and not self._contains_control_anchor(index)
                            and not self._contains_control_anchor(target)
                            and not self._contains_control_anchor(value)
                            and not self.is_accessed_later(index)
                            and not self.accesses_any_variables(
                                (index, coll, value),
                                target
                            )
                        )
                    """,
                ),
                CodeChange(
                    pattern="""
                        ${target} = 0

                        for ${index} in ${coll}:
                            if ${cond}:
                                ${target} += ${value}
                    """,
                    replacement="""
                        ${target} = sum(${value} for ${index} in ${coll} if ${cond})
                    """,
                    # TODO: once we move on to interpreted syntax, the condition
                    # `self._contains_control_anchor` should be applied only to the
                    # top-level `pattern`.
                    condition="""
                        (
                            not self.is_in_scope_of("sum", target)
                            and not self._contains_named_expr(cond)
                            and not self._contains_control_anchor(cond)
                            and not self._contains_control_anchor(index)
                            and not self._contains_control_anchor(target)
                            and not self._contains_control_anchor(value)
                            and not self.is_accessed_later(index)
                            and not self.accesses_any_variables(
                                (index, coll, value, cond),
                                target
                            )
                        )
                    """,
                ),
            ]
            + [
                CodeChange(
                    pattern=f"""
                        ${{target}} = ${{initial}}

                        for ${{index}} in ${{coll}}:
                            ${{target}} {sign}= ${{value}}
                    """,
                    replacement=f"""
                        ${{target}} = ${{initial}} {sign} sum(${{value}} for ${{index}} in ${{coll}})
                    """,
                    # TODO: once we move on to interpreted syntax, the condition
                    # `self._contains_control_anchor` should be applied only to the
                    # top-level `pattern`.
                    condition="""
                        (
                            not self.is_in_scope_of("sum", target)
                            and self.has_int_type(initial)
                            and not self._contains_control_anchor(index)
                            and not self._contains_control_anchor(target)
                            and not self._contains_control_anchor(value)
                            and not self.is_accessed_later(index)
                            and not self.accesses_any_variables(
                                (index, coll, value),
                                target
                            )
                        )
                    """,
                )
                for sign in ("+", "-")
            ]
            + [
                CodeChange(
                    pattern=f"""
                        ${{target}} = ${{initial}}

                        for ${{index}} in ${{coll}}:
                            if ${{cond}}:
                                ${{target}} {sign}= ${{value}}
                    """,
                    replacement=f"""
                        ${{target}} = ${{initial}} {sign} sum(${{value}} for ${{index}} in ${{coll}} if ${{cond}})
                    """,
                    # TODO: once we move on to interpreted syntax, the condition
                    # `self._contains_control_anchor` should be applied only to the
                    # top-level `pattern`.
                    condition="""
                        (
                            not self.is_in_scope_of("sum", target)
                            and self.has_int_type(initial)
                            and not self._contains_named_expr(cond)
                            and not self._contains_control_anchor(cond)
                            and not self._contains_control_anchor(index)
                            and not self._contains_control_anchor(target)
                            and not self._contains_control_anchor(value)
                            and not self.is_accessed_later(index)
                            and not self.accesses_any_variables(
                                (index, coll, value, cond),
                                target
                            )
                        )
                    """,
                )
                for sign in ("+", "-")
            ]
        )

    def _contains_control_anchor(self, node: Node) -> bool:
        control_anchor_types = (Await, Return, Yield, YieldFrom)
        return isinstance(node, control_anchor_types) or not self.contained_nodes[
            node
        ].isdisjoint(control_anchor_types)

    def _contains_named_expr(self, node: Node) -> bool:
        return isinstance(node, NamedExpr) or NamedExpr in self.contained_nodes[node]

    def description(self) -> str:
        return "Convert for loop into call to sum()"

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
