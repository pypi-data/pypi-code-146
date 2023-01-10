from typing import List

from lib.version import PythonVersion
from sourcery.ast import Keyword, Node
from sourcery.conditions.capture_conditions import CaptureConditions
from sourcery.conditions.dependency_conditions import DependencyConditions
from sourcery.conditions.type_conditions import TypeConditions
from sourcery.conditions.variable_usage_conditions import VariableUsageConditions
from sourcery.dsl.code_change import CodeChange
from sourcery.dsl.proposals import DSLProposer
from sourcery.engine.rule_type import RuleType


class DictAssignUpdateToUnionProposer(  # pylint: disable=too-many-ancestors
    DSLProposer,
    DependencyConditions,
    TypeConditions,
    CaptureConditions,
    VariableUsageConditions,
):
    def create_code_changes(self) -> List[CodeChange]:
        return [
            # Convert assign to augassign
            # x = x | y => x |= y
            CodeChange(
                pattern="""
                    ${target | has_dict_type} = ${target} | ${other}
                """,
                replacement="""
                    ${target} |= ${other}
                """,
            ),
            # Convert update to augassign
            # x.update(y) => x |= y
            CodeChange(
                pattern="""
                    ${target | is_assignable_dict}.update(${updater | is_positional_arg})
                """,
                replacement="""
                    ${target} |= ${updater}
                """,
            ),
            # Convert assign then augassign to union
            # x = y; x |= z => x = y | z
            CodeChange(
                pattern="""
                    ${target} = ${initial | has_dict_type}
                    ${target} |= ${other | (
                        self.has_dict_type(other)
                            and not self.directly_accesses_variable(other, target)
                    )}
                """,
                replacement="""
                    ${target} = ${initial} | ${other}
                """,
            ),
            # Convert empty union to dict constructor
            # x = {} | y => x = dict(y)
            CodeChange(
                pattern="""
                    {} | ${other | has_dict_type}
                """,
                replacement="""
                    dict(${other})
                """,
            ),
        ]

    def min_python_version(self) -> PythonVersion:
        return PythonVersion(major=3, minor=9)

    def description(self) -> str:
        return "Merge dictionary updates via the union operator"

    def kind(self) -> RuleType:
        return RuleType.REFACTORING

    def is_assignable_dict(self, node: Node):
        return (
            self.has_dict_type(node)
            and self.is_assignable(node)
            and not self.writes_to_global_state(node)
        )

    def is_positional_arg(self, node: Node):
        return not isinstance(node, Keyword)
