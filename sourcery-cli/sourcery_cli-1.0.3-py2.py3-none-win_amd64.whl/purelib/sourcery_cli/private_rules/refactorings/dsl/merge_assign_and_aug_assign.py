from enum import Enum
from typing import List

from sourcery.ast.ast import is_multiline
from sourcery.ast.nodes import Node
from sourcery.conditions.type_conditions import TypeConditions
from sourcery.dsl.code_change import CodeChange
from sourcery.dsl.proposals import DSLProposer


class Operator(Enum):
    PLUS = "+"
    MINUS = "-"
    ASTERISK = "*"
    SLASH = "/"


class MergeAssignAndAugAssignProposer(DSLProposer, TypeConditions):
    def create_code_changes(self) -> List[CodeChange]:
        return [
            # +=
            CodeChange(
                pattern="""
                    ${var_name} = ${initial_value |
                        self.valid_type(initial_value, Operator.PLUS)
                    }
                    ${var_name} += ${added_value | (
                        not self.same_var(var_name, added_value)
                        and self.have_same_types(initial_value, added_value)
                    )}
                """,
                replacement="${var_name} = ${initial_value} + ${added_value}",
            ),
            # -=
            CodeChange(
                pattern="""
                    ${var_name} = ${initial_value |
                        self.valid_type(initial_value, Operator.MINUS)
                    }
                    ${var_name} -= ${subtracted_value | (
                        not self.same_var(var_name, subtracted_value)
                        and self.have_same_types(initial_value, subtracted_value)
                    )}
                """,
                replacement="${var_name} = ${initial_value} - ${subtracted_value}",
            ),
            # *=
            CodeChange(
                pattern="""
                    ${var_name} = ${initial_value |
                        self.valid_type(initial_value, Operator.ASTERISK)
                    }
                    ${var_name} *= ${multiplied_value | (
                        not self.same_var(var_name, multiplied_value)
                        and self.have_same_types(initial_value, multiplied_value)
                    )}
                """,
                replacement="${var_name} = ${initial_value} * ${multiplied_value}",
            ),
            # /=
            CodeChange(
                pattern="""
                    ${var_name} = ${initial_value |
                        self.valid_type(initial_value, Operator.SLASH)
                    }
                    ${var_name} /= ${divisor | (
                        not self.same_var(var_name, divisor)
                        and self.have_same_types(initial_value, divisor)
                    )}
                """,
                replacement="${var_name} = ${initial_value} / ${divisor}",
            ),
        ]

    def description(self) -> str:
        return "Replace assignment and augmented assignment with single assignment"

    def valid_type(self, node: Node, operation: Operator) -> bool:
        # This can look messy and cause issues if we combine multi-line constants
        if is_multiline(node):
            return False
        allowed_types = ["int", "float"]
        if operation == Operator.PLUS:
            allowed_types.append("str")
        return self.has_type(node, *allowed_types)

    def same_var(self, node: Node, other_node: Node) -> bool:
        return hash(node) == hash(other_node)
