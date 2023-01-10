from typing import List

from sourcery.conditions.dependency_conditions import DependencyConditions
from sourcery.conditions.type_conditions import TypeConditions
from sourcery.dsl.code_change import CodeChange
from sourcery.dsl.proposals import DSLProposer


class SimplifyDivisionProposer(DSLProposer, DependencyConditions, TypeConditions):
    def create_code_changes(self) -> List[CodeChange]:
        return [
            CodeChange(
                pattern="int(${a | has_int_type}/${b | has_int_type})",
                replacement="${a} // ${b}",
            ),
            # Further option:
            # Recognzie math.floor(a / b)
            CodeChange(
                pattern="""
                    ${quot} = ${a | has_int_type} // ${b | has_int_type}
                    ${statements* | (
                        not self.writes_any_variables(statements, a)
                        and not self.writes_any_variables(statements, b)
                    )}
                    ${remainder |
                        not self.accesses_any_variables(statements, remainder)
                    } = ${a} % ${b}
                """,
                replacement="""
                    ${quot}, ${remainder} = divmod(${a},${b})
                    ${statements}
                """,
            )
            # `divmod` works for any two non-complex numbers.
            # But we can guarantee that the following transformation is correct
            # only if the dividend and the divisor are both integers.
            # https://docs.python.org/3/library/functions.html#divmod
        ]

    def description(self) -> str:
        return "Simplify division expressions"
