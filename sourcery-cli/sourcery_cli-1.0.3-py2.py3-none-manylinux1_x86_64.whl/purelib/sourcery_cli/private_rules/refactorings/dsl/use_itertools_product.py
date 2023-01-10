import typing

from typing_extensions import TypeGuard

from sourcery.ast import Break, Call, Expression, Node, Tuple
from sourcery.ast.ast import contains_node_meeting_condition
from sourcery.conditions import TypeConditions
from sourcery.conditions.dependency_conditions import DependencyConditions
from sourcery.conditions.import_conditions import (
    AddImportPostCondition,
    ImportConditions,
)
from sourcery.conditions.literal_conditions import LiteralConditions
from sourcery.dsl.code_change import CodeChange
from sourcery.dsl.proposals import DSLProposer

# pylint: disable=too-many-ancestors


class UseItertoolsProductProposer(
    DSLProposer,
    DependencyConditions,
    ImportConditions,
    LiteralConditions,
    TypeConditions,
):
    def create_code_changes(self) -> typing.List[CodeChange]:
        introduce_product_code_change = CodeChange(
            pattern="""
                for ${x} in ${xs | _is_allowed_outer_iterable}:
                    for ${y} in ${ys | self._is_allowed_inner_iterable(ys, x)}:
                        ${statements+}
            """,
            replacement="""
                for ${x}, ${y} in ${
                    self._product(xs, ys)
                }:
                    ${statements}
            """,
            add_imports_post_condition=self.itertools_product(),
            top_level_condition=does_not_contain_break,
        )

        merge_inner_loop_into_outer_product = CodeChange(
            pattern="""
                for ${x} in ${xs | _is_allowed_outer_product}:
                    for ${y} in ${ys | self._is_allowed_inner_iterable(ys, x)}:
                        ${statements+}
            """,
            replacement="""
                for ${self._merge_tuple_target(x, y)} in ${
                    self._merge_product_iterable(xs, ys)
                }:
                    ${statements}
            """,
            top_level_condition=lambda node: (
                does_not_contain_break(node)
                and self.has_available_import_name("itertools.product")
            ),
        )

        merge_outer_loop_into_inner_product = CodeChange(
            pattern="""
                for ${x} in ${xs | _is_allowed_outer_iterable}:
                    for ${y} in ${ys | self._is_allowed_inner_product(ys, x)}:
                        ${statements+}
            """,
            replacement="""
                for ${self._merge_target_tuple(x, y)} in ${
                    self._merge_iterable_product(xs, ys)
                }:
                    ${statements}
            """,
            top_level_condition=lambda node: (
                does_not_contain_break(node)
                and self.has_available_import_name("itertools.product")
            ),
        )

        return [
            merge_inner_loop_into_outer_product,
            merge_outer_loop_into_inner_product,
            introduce_product_code_change,
        ]

    def _merge_target_tuple(self, x: Expression, y: Tuple) -> Tuple:
        return Tuple((x, *y.elts))

    def _merge_tuple_target(self, x: Tuple, y: Expression) -> Tuple:
        return Tuple((*x.elts, y))

    def _merge_iterable_product(self, xs: Expression, ys: Call) -> Call:
        ys.args = (xs, *ys.args)
        return ys

    def _merge_product_iterable(self, xs: Call, ys: Expression) -> Call:
        xs.args = (*xs.args, ys)
        return xs

    def _product(self, xs: Expression, ys: Expression) -> Expression:
        return Call(self.itertools_product().node_for_import_name(), (xs, ys))

    def itertools_product(self) -> AddImportPostCondition:
        return self.upsert_import("itertools.product")

    def _is_allowed_outer_product(self, outer_iterable: Node) -> bool:
        return self._is_itertools_product(outer_iterable) and all(
            self._is_allowed_outer_iterable(arg) for arg in outer_iterable.args
        )

    def _is_allowed_outer_iterable(self, outer_iterable: Node) -> bool:
        return self.has_sized_type(outer_iterable) and not self.is_collection_literal(
            outer_iterable
        )

    def _is_allowed_inner_product(
        self, inner_iterable: Node, outer_target: Node
    ) -> bool:
        return self._is_itertools_product(inner_iterable) and all(
            self._is_allowed_inner_iterable(arg, outer_target)
            for arg in inner_iterable.args
        )

    def _is_allowed_inner_iterable(
        self, inner_iterable: Node, outer_target: Node
    ) -> bool:
        return self.has_sized_type(inner_iterable) and not (
            self.is_collection_literal(inner_iterable)
            or self.writes_any_variables(inner_iterable)
            or self.accesses_any_variables(inner_iterable, outer_target)
            or self.writes_any_variables(outer_target.statement(), inner_iterable)
        )

    def _is_itertools_product(self, node: Node) -> TypeGuard[Call]:
        return isinstance(node, Call) and self.is_name_node_for_import_name(
            node.func, "itertools.product"
        )

    def description(self) -> str:
        return "Replaces a nested for loop with a call to `itertools.product`"


def does_not_contain_break(node: Node) -> bool:
    return not contains_node_meeting_condition(node, is_break)


def is_break(node: Node) -> bool:
    return isinstance(node, Break)
