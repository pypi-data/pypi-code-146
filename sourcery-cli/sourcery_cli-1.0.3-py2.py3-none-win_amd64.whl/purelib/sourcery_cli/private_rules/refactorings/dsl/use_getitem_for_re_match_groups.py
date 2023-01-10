from typing import List

from lib.version import PythonVersion
from sourcery.conditions.import_conditions import ImportConditions
from sourcery.conditions.type_conditions import TypeConditions
from sourcery.dsl.code_change import CodeChange
from sourcery.dsl.proposals import DSLProposer
from sourcery.engine.rule_type import RuleType


class UseGetitemForReMatchGroupsProposer(DSLProposer, TypeConditions, ImportConditions):
    def create_code_changes(self) -> List[CodeChange]:
        return [
            CodeChange(
                pattern="""
                    ${m|self.has_type(m, 're.Match')}.group(${x})
                """,
                replacement="""
                    ${m}[${x}]
                """,
                top_level_condition=lambda _node: self.has_module_name("re"),
            )
        ]

    def description(self) -> str:
        return "Replace m.group(x) with m[x] for re.Match objects"

    def kind(self) -> RuleType:
        return RuleType.REFACTORING

    def min_python_version(self) -> PythonVersion:
        return PythonVersion(major=3, minor=6)
