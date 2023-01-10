from typing import List

from lib.version import PythonVersion
from sourcery.ast import (
    Await,
    If,
    IfExp,
    NamedExpr,
    Node,
    Yield,
    YieldFrom,
    contains_types,
)
from sourcery.conditions.capture_conditions import CaptureConditions
from sourcery.conditions.dependency_conditions import DependencyConditions
from sourcery.conditions.variable_usage_conditions import VariableUsageConditions
from sourcery.dsl.code_change import CodeChange
from sourcery.dsl.proposals import DSLProposer


class UseNamedExpressionProposer(  # pylint: disable=too-many-ancestors
    DSLProposer, CaptureConditions, DependencyConditions, VariableUsageConditions
):
    def create_code_changes(self) -> List[CodeChange]:
        return [
            CodeChange(
                pattern="""
                    ${target | is_name} = ${
                        value|self._suitable_value(value)
                    }
                    if ${target|self._only_used_in_if(target)}:
                        ${statements+}
                    $elif{elifs*}
                    else:
                        ${else_statements*}
                """,
                replacement="""
                    if ${target} := ${value}:
                        ${statements}
                    $elif{elifs}
                    else:
                        ${else_statements}
                """,
            ),
            CodeChange(
                pattern="""
                    ${target | is_name} = ${
                        value|self._suitable_value(value)
                    }
                    while ${target|not self.is_accessed_later(target)}:
                        ${statements+}
                        ${target} = ${value}
                    else:
                        ${else_statements*}
                """,
                replacement="""
                    while ${target} := ${value}:
                        ${statements}
                    else:
                        ${else_statements}
                """,
            ),
        ]

    def _only_used_in_if(self, node: Node) -> bool:
        assert isinstance(node.parent, If)
        return self.accesses_any_variables(
            node.parent.body, node
        ) and not self.is_accessed_later(node)

    def _suitable_value(self, node: Node) -> bool:
        return not contains_types(node, (Await, IfExp, NamedExpr, Yield, YieldFrom))

    def description(self) -> str:
        return "Use named expression to simplify assignment and conditional"

    def min_python_version(self) -> PythonVersion:
        return PythonVersion(major=3, minor=8)
