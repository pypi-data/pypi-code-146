from typing import List

from lib.version import PythonVersion
from sourcery.ast import Constant, Expression, Node
from sourcery.ast import Tuple as ASTTuple
from sourcery.ast import get_nodes
from sourcery.conditions.f_string_conditions import FStringConditions
from sourcery.conditions.type_conditions import TypeConditions
from sourcery.dsl.code_change import CodeChange
from sourcery.dsl.proposals import DSLProposer
from sourcery.engine.rule_type import RuleType


class ReplaceInterpolationWithFstringProposer(
    DSLProposer, FStringConditions, TypeConditions
):
    def create_code_changes(self) -> List[CodeChange]:
        return [
            CodeChange(
                pattern="""
                    ${s | self.is_valid_fstring_substring(s)} % ${
                        values | self.is_suitable_values(values, s)
                    }
                """,
                replacement="""
                    ${self._create_fstring(s, values)}
                """,
            )
        ]

    def description(self) -> str:
        return "Replace interpolated string formatting with f-string"

    def kind(self) -> RuleType:
        return RuleType.REFACTORING

    def min_python_version(self) -> PythonVersion:
        return PythonVersion(major=3, minor=6)

    def is_suitable_values(self, values: Node, s: Constant) -> bool:
        value_elts = get_nodes(values)
        return s.value.count("%s") == s.value.count("%") == len(
            value_elts
        ) and self.is_valid_fstring_expression(value_elts)

    def _create_fstring(self, s: Constant, args: Expression):
        value_nodes = args.elts if isinstance(args, ASTTuple) else [args]
        return self.create_fstring(s, value_nodes, "%s")
