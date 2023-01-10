from typing import List

from sourcery.ast import FormattedValue, Node
from sourcery.conditions.type_conditions import TypeConditions
from sourcery.dsl.code_change import CodeChange
from sourcery.dsl.proposals import DSLProposer


class RemoveStrFromFstringProposer(DSLProposer, TypeConditions):
    def create_code_changes(self) -> List[CodeChange]:
        return [
            CodeChange(
                pattern="""
                    str(${value|has_built_in_type})
                """,
                replacement="""
                    ${value}
                """,
                top_level_condition=self._in_suitable_formatted_value,
            )
        ]

    def _in_suitable_formatted_value(self, node: Node) -> bool:
        return (
            isinstance(node.parent, FormattedValue)
            and not self._conversion_specifier(node.parent)
            and node.parent.format_spec is None
        )

    def _conversion_specifier(self, node: FormattedValue) -> bool:
        return node.conversion not in {-1, None}

    def description(self) -> str:
        return "Remove unnecessary calls to `str()` from formatted values in f-strings"
