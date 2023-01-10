from typing import List, Set, Type

from sourcery.conditions.dependency_conditions import DependencyConditions
from sourcery.conditions.variable_usage_conditions import VariableUsageConditions
from sourcery.dsl.code_change import CodeChange
from sourcery.dsl.proposals import DSLProposer
from sourcery.rules.private.refactorings.descriptions import (
    REMOVE_UNUSED_ENUMERATE_INDEX,
)
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


class RemoveUnusedEnumerateProposer(
    DSLProposer, DependencyConditions, VariableUsageConditions
):
    """Remove unnecessary calls to `enumerate` when the index variable is not used.

    For instance,
    ```py
    for index, value in enumerate(range(10)):
      print(value)
    ```
    can be simplified to
    ```py
    for value in range(10):
      print(value)
    ```
    since the variable `index` is never used.
    """

    def create_code_changes(self) -> List[CodeChange]:
        basic_code_changes = [
            CodeChange(
                pattern="""
                    for ${index|not self.is_accessed_later(index)}, ${item} in enumerate(${collection}):
                        ${statements+|not self.accesses_any_variables(statements, index)}
                """,
                replacement="""
                    for ${item} in ${collection}:
                        ${statements}
                """,
            )
        ]

        comprehension_pattern = """
            ${expression|not self.accesses_any_variables(expression, index)}
            for ${index}, ${item} in enumerate(${collection})
            if ${condition?|not self.accesses_any_variables(condition, index)}
        """
        comprehension_replacement = """
            ${expression}
            for ${item} in ${collection}
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
                        ${key|not self.accesses_any_variables(key, index)}:
                        ${value|not self.accesses_any_variables(value, index)}
                        for ${index}, ${item} in enumerate(${collection})
                        if ${condition?|not self.accesses_any_variables(condition, index)}
                    }
                """,
                replacement="""
                    {
                        ${key}: ${value}
                        for ${item} in ${collection}
                        if ${condition}
                    }
                """,
            )
        ]

        return (
            basic_code_changes
            + comprehension_code_changes
            + dict_comprehension_code_changes
        )

    def description(self) -> str:
        return REMOVE_UNUSED_ENUMERATE_INDEX

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
