import typing

from sourcery import ast
from sourcery.dsl.code_change import CodeChange
from sourcery.dsl.proposals import DSLProposer
from sourcery.engine.rule_type import RuleType


class UnwrapIterableConstructionProposer(DSLProposer):
    def create_code_changes(self) -> typing.List[CodeChange]:
        return [
            CodeChange(
                pattern="""
                    ${constructor | is_valid_constructor}(${
                        const_iterable
                        | self.is_valid_const_iterable(constructor, const_iterable)
                    })
                """,
                replacement="""
                    ${make_const_iterable(constructor, const_iterable)}
                """,
            )
        ]

    def description(self) -> str:
        return "Unwrap a constant iterable constructor"

    def kind(self) -> RuleType:
        return RuleType.REFACTORING

    def is_valid_constructor(self, constructor: ast.Name) -> bool:
        return constructor.unparse() in {"list", "tuple", "set"}

    def is_valid_const_iterable(
        self, constructor: ast.Name, const_iterable: ast.Expression
    ) -> bool:
        if not isinstance(const_iterable, (ast.List, ast.Set, ast.Tuple)):
            return False
        constructor_is_list_or_tuple = constructor.unparse() in {"list", "tuple"}
        constructor_is_set = constructor.unparse() == "set"
        iterable_is_list_or_tuple = isinstance(const_iterable, (ast.List, ast.Tuple))
        iterable_is_set = isinstance(const_iterable, ast.Set)
        iterable_is_empty = not const_iterable.elts

        return (constructor_is_list_or_tuple and iterable_is_list_or_tuple) or (
            constructor_is_set
            and (iterable_is_set or iterable_is_list_or_tuple)
            and not iterable_is_empty
        )


def make_const_iterable(
    constructor: ast.Name, const_iterable: typing.Union[ast.List, ast.Tuple]
) -> typing.Union[ast.List, ast.Tuple, ast.Set]:
    name = constructor.unparse()
    if name == "list":
        return ast.List(elts=const_iterable.elts)
    if name == "set":
        return ast.Set(elts=const_iterable.elts)
    if name == "tuple":
        return ast.Tuple(elts=const_iterable.elts)
    raise NotImplementedError
