from typing import List, Set, Type

from sourcery.ast import Break, Call, Comprehension, GeneratorExp, If, Name, Node
from sourcery.ast.ast import invert_condition
from sourcery.conditions.dependency_conditions import DependencyConditions
from sourcery.conditions.literal_conditions import LiteralConditions
from sourcery.conditions.variable_usage_conditions import VariableUsageConditions
from sourcery.dsl.code_change import CodeChange
from sourcery.dsl.proposals import DSLProposer
from sourcery.rules.private.refactorings.descriptions import USE_ANY_DESC
from sourcery.semantic_equivalence.semantic_types import (
    ExceptionArgsChanged,
    ExceptionTypeChanged,
    LocalChangeOnException,
    LocalValueMissing,
    SemanticDifference,
)


class UseAnyProposer(  # pylint: disable=too-many-ancestors
    DSLProposer, DependencyConditions, LiteralConditions, VariableUsageConditions
):
    """Use `any(...)` instead of a broken for loop for checking truthiness.

    Skipped if the target variable(s) of the for loop are used later
    """

    def create_code_changes(self) -> List[CodeChange]:
        return [
            CodeChange(
                pattern="""
                    ${found}: ${ann?} = ${default|self.is_boolean_literal(default)}
                    for ${item|not self.is_accessed_later(item)} in ${items}:
                        if ${condition | (
                            self.allowable_writes(condition)
                            and not self.accesses_any_variables(condition, found)
                        )}:
                            ${found} = ${other | (
                                self.is_boolean_literal(other)
                                and other.value is not default.value
                            )}
                            ${break_statement?|isinstance(break_statement, Break)}
                """,
                replacement="""
                    ${found}: ${ann} = ${
                        self.create_any(condition, item, items, default)
                    }
                """,
            ),
            CodeChange(
                pattern="""
                    for ${item|not self.is_accessed_later(item)} in ${items}:
                        if ${condition |
                            not self.contains_type_disallowed_in_generator(condition)
                        }:
                            return ${other|self.is_boolean_literal(other)}
                    return ${default | (
                        self.is_boolean_literal(default)
                        and default.value is not other.value)
                    }
                """,
                replacement="""
                    return ${self.create_any(condition, item, items, default)}
                """,
            ),
        ]

    def allowable_writes(self, node: Node) -> bool:
        assert isinstance(node.parent, If)

        if self.contains_type_disallowed_in_generator(node):
            return False

        if isinstance(node.parent.body[-1], Break):
            return True

        return not self.writes_any_variables(node)

    def create_any(self, condition, item, items, default) -> Node:
        iterator = items
        iterator.clear_original_source()
        comp = Comprehension(item, iterator, ())
        generator = GeneratorExp((comp,), condition)
        call = Call(Name("any"), (generator,))
        return invert_condition(call) if default.value else call

    def description(self) -> str:
        return USE_ANY_DESC

    def expected_semantic_differences(self) -> Set[Type[SemanticDifference]]:
        return {
            ExceptionArgsChanged,
            ExceptionTypeChanged,
            LocalChangeOnException,
            LocalValueMissing,
        }
