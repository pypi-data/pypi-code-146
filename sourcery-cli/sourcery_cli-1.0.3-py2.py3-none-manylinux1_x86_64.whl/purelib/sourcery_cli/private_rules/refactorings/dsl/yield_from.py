from typing import List, Set, Type

from sourcery.ast import FunctionDef, Node
from sourcery.dsl.code_change import CodeChange
from sourcery.dsl.proposals import DSLProposer
from sourcery.rules.private.refactorings.descriptions import YIELD_FROM_DESC
from sourcery.semantic_equivalence.semantic_types import (
    ExceptionArgsChanged,
    ExceptionTypeChanged,
    SemanticDifference,
)


class YieldFromProposer(DSLProposer):
    def create_code_changes(self) -> List[CodeChange]:
        return [
            CodeChange(
                pattern="""
                    for ${item} in ${collection}:
                      yield ${item}
                """,
                replacement="""
                    yield from ${collection}
                """,
                top_level_condition=not_in_async_function,
            )
        ]

    def description(self) -> str:
        return YIELD_FROM_DESC

    def expected_semantic_differences(self) -> Set[Type[SemanticDifference]]:
        return {ExceptionArgsChanged, ExceptionTypeChanged}


def not_in_async_function(node: Node):
    scope = node.scope()
    return not (isinstance(scope, FunctionDef) and scope.is_async)
