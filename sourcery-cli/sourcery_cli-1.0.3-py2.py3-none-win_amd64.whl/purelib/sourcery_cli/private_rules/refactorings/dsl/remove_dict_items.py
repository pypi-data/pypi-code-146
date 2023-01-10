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
    ExceptionRemoved,
    ExceptionTypeChanged,
    FunctionCallsChanged,
    LocalChangeOnException,
    LocalValueMissing,
    ReturnValuesChangedOnException,
    SemanticDifference,
    StdOutChangedOnException,
)


class RemoveDictItemsProposer(  # pylint: disable=too-many-ancestors
    DSLProposer, DependencyConditions, TypeConditions, VariableUsageConditions
):
    """Remove unnecessary calls to `dict.items` when the values are not used.

    For instance,
    ```py
    for key, value in d.items():
      print(key)
    ```
    can be simplified to
    ```py
    for key in d:
      print(key)
    ```
    since the variable `value` is never used.
    """

    def description(self) -> str:
        return "Remove unnecessary calls to `dict.items` when the values are not used"

    def create_code_changes(self) -> List[CodeChange]:
        for_code_changes = [
            CodeChange(
                pattern="""
                    for ${key}, ${value | is_valid_value} in ${d | has_dict_type}.items():
                        ${statements+ |
                            not self.accesses_any_variables(statements, value)
                        }
                """,
                replacement="""
                    for ${key} in ${d}:
                        ${statements}
                """,
            )
        ]

        comprehension_pattern = """
            ${expression | not self.accesses_any_variables(expression, value)}
            for ${key}, ${value | is_valid_value} in ${d | has_dict_type}.items()
            if ${condition? | not self.accesses_any_variables(condition, value)}
        """
        comprehension_replacement = """
            ${expression}
            for ${key} in ${d}
            if ${condition}
        """
        comprehension_code_changes = [
            CodeChange(
                pattern=f"{left} {comprehension_pattern} {right}",
                replacement=f"{left} {comprehension_replacement} {right}",
            )
            for left, right in (
                ("(", ")"),  # generators
                ("{", "}"),  # set comprehensions
                ("[", "]"),  # list comprehensions
            )
        ]

        dict_comprehension_code_changes = [
            CodeChange(
                pattern="""
                    {
                        ${new_key | not self.accesses_any_variables(new_key, value)}:
                        ${new_value | not self.accesses_any_variables(new_value, value)}
                        for ${key}, ${value | is_valid_value} in ${d | has_dict_type}.items()
                        if ${condition? |
                            not self.accesses_any_variables(condition, value)
                        }
                    }
                """,
                replacement="""
                    {
                        ${new_key}: ${new_value}
                        for ${key} in ${d}
                        if ${condition}
                    }
                """,
            )
        ]

        return (
            for_code_changes
            + comprehension_code_changes
            + dict_comprehension_code_changes
        )

    def is_valid_value(self, value: Node) -> bool:
        # TODO: when `value` is not a name, we may still want to apply this change - we
        # just have to check that every name in the unstructed value is also not used:
        # for key, (value_a, value_b) in d.items():
        #   print(key)
        # However, the user may want to check for an exact structure of `d` - and hence
        # we would break their code by removing `(value_a, value_b)`.
        # The most conservative approach here would be to propose this as a suggestion
        # rather than a refactoring.

        # TODO: move `isinstance(value, NameNode)` into a typeguard function
        # `is_name_node`, possibly in a new conditions class `NodeConditions`
        return isinstance(value, NameNode) and not self.is_accessed_later(value)

    def expected_semantic_differences(self) -> Set[Type[SemanticDifference]]:
        return {
            LocalValueMissing,
            LocalChangeOnException,
            ExceptionRemoved,
            ExceptionTypeChanged,
            ExceptionArgsChanged,
            ReturnValuesChangedOnException,
            StdOutChangedOnException,
            # TODO: FunctionCallChanged was introduced as a workaround to the following
            # error:
            # Found unexpected semantic differences:
            # {<class
            # 'sourcery.semantic_equivalence.semantic_types.FunctionCallsChanged'>}
            # Full results:
            # Differences:
            # [
            #     FunctionCallsChanged(
            #         input_variables={
            #             'hat.lower': <function hat.lower at 0x7ff019aed670>,
            #             'list_of_hats': {'abc': 1},
            #             'buy_all': <function buy_all at 0x7ff019aed4c0>
            #         },
            #         function_calls_before=[
            #             FunctionCall(
            #                 function='buy_all',
            #                 args=(<generator object <genexpr> at 0x7ff017b02e40>,)
            #             )
            #         ],
            #         function_calls_after=[
            #             FunctionCall(
            #                 function='buy_all',
            #                 args=(<generator object <genexpr> at 0x7ff017b02f90>,)
            #             )
            #         ]
            #     )
            # ]
            # This is caused because we currently don't have a good way to compare
            # the arguments passed to functions when they are non-comparable objects
            # such as generators or lambdas.
            # The task for the future here is to come up with a good way of comparing
            # such objects.
            # A possible solution is running `_transform` on the function arguments
            FunctionCallsChanged,
        }
