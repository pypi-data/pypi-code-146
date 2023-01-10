from typing import List

from sourcery.conditions.capture_conditions import CaptureConditions
from sourcery.conditions.type_conditions import TypeConditions
from sourcery.dsl.code_change import CodeChange
from sourcery.dsl.proposals import DSLProposer
from sourcery.rules.private.refactorings.descriptions import SIMPLIFY_DICT_UPDATE_DESC


class SimplifyDictionaryUpdateProposer(DSLProposer, CaptureConditions, TypeConditions):
    def create_code_changes(self) -> List[CodeChange]:
        return [
            CodeChange(
                pattern="${d|has_dict_type}.update({${key}: ${value}})",
                replacement="${d}[${key}] = ${value}",
                top_level_condition=self.is_expression_statement,
            )
        ]

    def description(self) -> str:
        return SIMPLIFY_DICT_UPDATE_DESC
