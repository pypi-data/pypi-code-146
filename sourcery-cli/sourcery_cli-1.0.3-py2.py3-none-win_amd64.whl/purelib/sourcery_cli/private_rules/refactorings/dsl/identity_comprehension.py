from typing import List, Set, Type

from sourcery.ast import Name, Node
from sourcery.conditions.type_conditions import TypeConditions
from sourcery.dsl.code_change import CodeChange
from sourcery.dsl.proposals import DSLProposer
from sourcery.semantic_equivalence.semantic_types import (
    ExceptionArgsChanged,
    ExceptionRemoved,
    LocalChangeOnException,
    SemanticDifference,
)


class IdentityComprehensionProposer(DSLProposer, TypeConditions):
    def create_code_changes(self) -> List[CodeChange]:
        list_code_changes = [
            CodeChange(
                pattern="[${item} for ${item} in ${coll | not self.is_self(coll)}]",
                replacement="list(${coll})",
            )
        ]

        dict_code_changes = [
            CodeChange(
                pattern="dict(${coll | has_dict_type}.items())",
                replacement="dict(${coll})",
            ),
            CodeChange(
                pattern="""
                    {
                      ${key}: ${value}
                      for ${key}, ${value}
                      in ${coll | has_dict_type}.items()
                    }
                """,
                replacement="dict(${coll})",
            ),
            CodeChange(
                pattern="""
                    {
                      ${key}: ${value}
                      for ${key}, ${value}
                      in ${coll}
                    }
                """,
                replacement="dict(${coll})",
            ),
        ]

        set_code_change = [
            CodeChange(
                pattern="{${item} for ${item} in ${coll}}",
                replacement="set(${coll})",
            ),
        ]

        return list_code_changes + dict_code_changes + set_code_change

    def is_self(self, node: Node) -> bool:
        return isinstance(node, Name) and node.id == "self"

    def description(self) -> str:
        return "Replace identity comprehension with call to collection constructor"

    def expected_semantic_differences(self) -> Set[Type[SemanticDifference]]:
        return {
            ExceptionRemoved,
            ExceptionArgsChanged,
            LocalChangeOnException,
        }
