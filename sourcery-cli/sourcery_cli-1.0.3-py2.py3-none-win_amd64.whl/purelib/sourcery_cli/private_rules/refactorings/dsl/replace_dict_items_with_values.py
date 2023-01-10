from typing import List, Set, Type

from sourcery.ast import Name as NameNode
from sourcery.ast import Node
from sourcery.conditions.dependency_conditions import DependencyConditions
from sourcery.conditions.type_conditions import TypeConditions
from sourcery.conditions.variable_usage_conditions import VariableUsageConditions
from sourcery.dsl.code_change import CodeChange
from sourcery.dsl.proposals import DSLProposer
from sourcery.semantic_equivalence.semantic_types import (
    ExceptionArgsChanged,
    ExceptionTypeChanged,
    LocalValueMissing,
    SemanticDifference,
)


class ReplaceDictItemsWithValuesProposer(  # pylint: disable=too-many-ancestors
    DSLProposer, DependencyConditions, TypeConditions, VariableUsageConditions
):
    """Replace calls to `dict.items` with `dict.values` when the keys are not used.

    For instance,
    ```py
    for key, value in d.items():
      print(value)
    ```
    can be simplified to
    ```py
    for value in d.values():
      print(value)
    ```
    since the variable `key` is never used.
    """

    def create_code_changes(self) -> List[CodeChange]:
        basic_code_change = CodeChange(
            pattern="""
                for ${k|is_valid_key}, ${v} in ${d|has_dict_type}.items():
                  ${statements+|not self.accesses_any_variables(statements, k)}
            """,
            replacement="""
                for ${v} in ${d}.values():
                  ${statements}
            """,
        )

        # TODO: remove items if used inside comprehensions as well

        return [basic_code_change]

    def description(self) -> str:
        return (
            "Replace calls to `dict.items` with `dict.values` when the keys are "
            "not used"
        )

    def is_valid_key(self, key: Node) -> bool:
        return isinstance(key, NameNode) and not self.is_accessed_later(key)

    def expected_semantic_differences(self) -> Set[Type[SemanticDifference]]:
        return {LocalValueMissing, ExceptionArgsChanged, ExceptionTypeChanged}
