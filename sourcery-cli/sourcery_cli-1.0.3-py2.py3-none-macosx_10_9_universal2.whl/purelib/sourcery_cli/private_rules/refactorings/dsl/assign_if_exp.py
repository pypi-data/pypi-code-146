from typing import List

from sourcery.ast import IfExp  # pylint: disable=unused-import
from sourcery.dsl.code_change import CodeChange
from sourcery.dsl.proposals import DSLProposer

IF_EXP_CHARS = 13


class AssignIfExpProposer(DSLProposer):
    def create_code_changes(self) -> List[CodeChange]:
        code_changes = [
            CodeChange(
                pattern=f"""
                    if ${{condition}}:
                        {target} ${{first_value|not isinstance(first_value, IfExp)}}
                    else:
                        {target} ${{default|not isinstance(default, IfExp)}}
                """,
                replacement=f"""
                    {target} ${{
                        first_value
                    }} if ${{condition}} else ${{default}}
                """,
            )
            for target in [
                "${target} +=",
                "${target} -=",
                "return ",
            ]
        ]
        code_changes.append(
            CodeChange(
                pattern="""
                    if ${condition}:
                        ${target} = ${
                            first_value|not isinstance(first_value, IfExp)
                        }
                    else:
                        ${target} = ${default|not isinstance(default, IfExp)}
                """,
                replacement="""
                    ${target} = ${
                        first_value
                    } if ${condition} else ${default}
                """,
            )
        )

        return code_changes

    def description(self) -> str:
        return "Replace if statement with if expression"

    def should_produce_1_line(self) -> bool:
        return True
