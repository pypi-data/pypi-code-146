import typing

from sourcery import ast
from sourcery.conditions.capture_conditions import CaptureConditions
from sourcery.conditions.dependency_conditions import DependencyConditions
from sourcery.conditions.type_conditions import TypeConditions
from sourcery.dsl.code_change import CodeChange
from sourcery.dsl.proposals import DSLProposer
from sourcery.semantic_equivalence.semantic_types import (
    ExceptionArgsChanged,
    FunctionCallsChanged,
    SemanticDifference,
)

_BuiltInListOrTuple = typing.TypeVar("_BuiltInListOrTuple", ast.List, ast.Tuple)


# pylint: disable=too-many-ancestors
class MergeListAppendsIntoExtendProposer(
    DSLProposer, CaptureConditions, DependencyConditions, TypeConditions
):
    """Merge consecutive appends to list as a single extend."""

    def create_code_changes(self) -> typing.List[CodeChange]:
        merge_appends_code_change = CodeChange(
            pattern="""
                ${L|is_named_list}.append(${first})
                ${L}.append(${second|not self.accesses_any_variables(second, L)})
            """,
            replacement="""
                ${L}.extend((${first}, ${second}))
            """,
        )

        add_appends_to_extend_code_change = CodeChange(
            pattern="""
                ${L|is_named_list}.extend(${coll|is_const_list_or_tuple})
                ${L}.append(${last|not self.accesses_any_variables(last, L)})
            """,
            replacement="""
                ${L}.extend(${self.append_to_collection(coll, last)})
            """,
        )

        merge_extends_code_change = CodeChange(
            pattern="""
                ${L|is_named_list}.extend(${coll1|is_const_list_or_tuple})
                ${L}.extend(
                    ${coll2|self.is_suitable_second_collection(coll2, L)}
                )
            """,
            replacement="""
                ${L}.extend(${self.extend_collection(coll1, coll2)})
            """,
        )

        return [
            merge_appends_code_change,
            add_appends_to_extend_code_change,
            merge_extends_code_change,
        ]

    def description(self) -> str:
        return "Merge consecutive list appends into a single extend"

    def is_suitable_second_collection(
        self, coll2: ast.Node, list_node: ast.Node
    ) -> bool:
        return self.is_const_list_or_tuple(coll2) and not self.accesses_any_variables(
            coll2, list_node
        )

    def is_named_list(self, list_node: ast.Node) -> bool:
        """Check that `list_node` is a name with the `list` type.

        We do this to disallow this refactoring from triggering with the following
        snippet:
        ```python
        [1, 2, 3].append(4)
        [1, 2, 3].append(5)
        ```
        Or, in a more realistic example,
        ```python
        self.get_most_empty_box().append(new_item)
        self.get_most_empty_box().append(other_item)
        ```
        """
        return self.is_name(list_node) and self.has_list_type(list_node)

    def extend_collection(
        self, coll1: _BuiltInListOrTuple, coll2: _BuiltInListOrTuple
    ) -> _BuiltInListOrTuple:
        return _extend_list_or_tuple_with_items(coll1, coll2.elts)

    def append_to_collection(
        self, coll: _BuiltInListOrTuple, item: ast.Expression
    ) -> _BuiltInListOrTuple:
        return _extend_list_or_tuple_with_items(coll, (item,))

    def is_const_list_or_tuple(self, coll: ast.Node) -> bool:
        # TODO: lift this method into a `NodeConditions` mixin
        return isinstance(coll, (ast.List, ast.Tuple))

    def expected_semantic_differences(
        self,
    ) -> typing.Set[typing.Type[SemanticDifference]]:
        return {ExceptionArgsChanged, FunctionCallsChanged}


def _extend_list_or_tuple_with_items(
    coll: _BuiltInListOrTuple, items: typing.Tuple[ast.Expression, ...]
) -> _BuiltInListOrTuple:
    for item in items:
        item.parent = coll

    coll.edit_tuple("elts", lambda elts: elts.extend(items))

    return coll
