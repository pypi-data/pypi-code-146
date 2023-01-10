"""Converts a `for` loop into a list comprehension."""

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


class ListComprehensionProposer(
    DSLProposer, DependencyConditions, VariableUsageConditions
):
    contained_nodes: ContainedNodes

    def create_code_changes(self) -> list[CodeChange]:
        # TODO: add case where ${target} is assigned to a non-empty literal list:
        #
        # my_set = [1, 2, 3]
        #
        # for i in range(10):
        #     my_set.append(i)
        #
        # This can probably be done by replacing `${target} = []` in the pattern with
        # `${target} = [${initial_values*}]`, and updating the replacement to be
        # `${target} = [${initial_values*}] + [${value} for ${index} in ${coll}]`
        #
        # The case `L = []` would then result in `L = [] + [...]` - getting rid of the
        # first empty list can either be done here or in a specialized refactoring.
        return (
            [
                CodeChange(
                    pattern=f"""
                        ${{target}} = []

                        for ${{index}} in ${{coll}}:
                            {append_method}
                    """,
                    replacement="""
                        ${target} = [${value} for ${index} in ${coll}]
                    """,
                    # TODO: once we move on to interpreted syntax, the condition
                    # `self._contains_control_anchor` should be applied only to the
                    # top-level `pattern`.
                    condition="""
                        (
                            not self.is_accessed_later(index)
                            and not self._contains_control_anchor(index)
                            and not self._contains_control_anchor(target)
                            and not self._contains_control_anchor(value)
                            and not self.accesses_any_variables(
                                (index, coll, value),
                                target
                            )
                        )
                    """,
                )
                for append_method in (
                    "${target}.append(${value})",
                    # TODO: the following two cases can be simplified to
                    # `${target}.append(${value})` in a separate refactoring:
                    #
                    # ${L | is_list}.extend([${x}]) -> ${L}.append(${x})
                    # ${L | is_list}.extend({${x}}) -> ${L}.append(${x})
                    # ${L | is_list}.extend((${x},)) -> ${L}.append(${x})
                    # ${L | is_list} += [${x}] -> ${L}.append(${x})
                    # ${L | is_list} += {${x}} -> ${L}.append(${x})
                    # ${L | is_list} += (${x},) -> ${L}.append(${x})
                    "${target}.extend([${value}])",
                    "${target} += [${value}]",
                )
            ]
            + [
                CodeChange(
                    pattern=f"""
                        ${{target}} = []

                        for ${{index}} in ${{coll}}:
                            if ${{cond}}:
                                {append_method}
                    """,
                    replacement="""
                        ${target} = [${value} for ${index} in ${coll} if ${cond}]
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
                            and not self._contains_control_anchor(value)
                            and not self.is_accessed_later(index)
                            and not self.accesses_any_variables(
                                (index, coll, value, cond),
                                target
                            )
                        )
                    """,
                )
                for append_method in (
                    "${target}.append(${value})",
                    "${target}.extend([${value}])",
                    "${target} += [${value}]",
                )
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
        return "Convert for loop into list comprehension"

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
