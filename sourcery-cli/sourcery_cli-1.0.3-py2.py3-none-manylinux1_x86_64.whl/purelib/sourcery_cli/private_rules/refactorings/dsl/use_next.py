import typing

from sourcery.conditions.dependency_conditions import DependencyConditions
from sourcery.conditions.variable_usage_conditions import VariableUsageConditions
from sourcery.dsl.code_change import CodeChange
from sourcery.dsl.proposals import DSLProposer
from sourcery.semantic_equivalence.semantic_types import (
    LocalChangeOnException,
    LocalValueMissing,
    SemanticDifference,
)


class UseNextProposer(DSLProposer, DependencyConditions, VariableUsageConditions):
    def create_code_changes(self) -> typing.List[CodeChange]:
        return_code_change = CodeChange(
            pattern="""
                for ${item} in ${items}:
                    if ${cond |
                        not self.contains_type_disallowed_in_generator(cond.parent)
                    }:
                        return ${result}
                return ${default | (
                    not self.writes_any_variables(default)
                    and not self.accesses_any_variables(default, item)
                )}
            """,
            replacement="""
                return next(
                    (
                        ${result}
                        for ${item} in ${items}
                        if ${cond}
                    ),
                    ${default}
                )
            """,
        )

        assign_to_default_first_code_change = CodeChange(
            pattern="""
                ${result}: ${ann?} = ${default}
                for ${item | not self.is_accessed_later(item)} in ${items}:
                    if ${cond | (
                        not self.contains_type_disallowed_in_generator(cond.parent)
                        and not self.accesses_any_variables(cond, result)
                    )}:
                        ${result} = ${
                            value | not self.accesses_any_variables(value, result)
                        }
                        break
            """,
            replacement="""
                ${result}: ${ann} = next(
                    (
                        ${value}
                        for ${item} in ${items}
                        if ${cond}
                    ),
                    ${default}
                )
            """,
        )

        assign_to_default_in_for_else_code_change = CodeChange(
            pattern="""
                for ${item | not self.is_accessed_later(item)} in ${items}:
                    if ${cond |
                        not self.contains_type_disallowed_in_generator(cond.parent)
                    }:
                        ${result} = ${value}
                        break
                else:
                    ${result} = ${default | (
                        not self.writes_any_variables(default)
                        and not self.accesses_any_variables(default, [item, result])
                        and not (
                            self.writes_any_variables(items)
                            and self.accesses_any_variables(default, items)
                        )
                    )}
            """,
            replacement="""
                ${result} = next(
                    (
                        ${value}
                        for ${item} in ${items}
                        if ${cond}
                    ),
                    ${default}
                )
            """,
        )

        return [
            return_code_change,
            assign_to_default_first_code_change,
            assign_to_default_in_for_else_code_change,
        ]

    def description(self) -> str:
        return "Use the built-in function `next` instead of a for-loop"

    def expected_semantic_differences(
        self,
    ) -> typing.Set[typing.Type[SemanticDifference]]:
        return {
            # after converting things to generators, `item` is not available anymore
            LocalValueMissing,
            # if `next` raises, the variable `result` is never assigned to anything
            LocalChangeOnException,
        }
