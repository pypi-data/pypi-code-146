from typing import List

from sourcery.conditions.scope_conditions import ScopeConditions
from sourcery.dsl.code_change import CodeChange
from sourcery.dsl.proposals import DSLProposer
from sourcery.engine.rule_type import RuleType


class AvoidBuiltinShadowProposer(DSLProposer, ScopeConditions):
    def create_code_changes(self) -> List[CodeChange]:
        return [
            CodeChange(
                pattern="""
                    ${var | var.unparse() in __builtins__ and not self.in_class_scope(var)} = ${anything}
                """,
                description="Don't assign to builtin variable `${var}`",
            )
        ]

    def kind(self) -> RuleType:
        return RuleType.COMMENT

    def explanation(self) -> str:
        return """
            Python has a number of `builtin` variables: functions and constants that
            form a part of the language, such as `list`, `getattr`, and `type`
            (See https://docs.python.org/3/library/functions.html).
            It is valid, in the language, to re-bind such variables:

            ```python
            list = [1, 2, 3]
            ```
            However, this is considered poor practice.
            - It will confuse other developers.
            - It will confuse syntax highlighters and linters.
            - It means you can no longer use that builtin for its original purpose.

            How can you solve this?

            Rename the variable something more specific, such as `integers`.
            In a pinch, `my_list` and similar names are colloquially-recognized
            placeholders.
        """
