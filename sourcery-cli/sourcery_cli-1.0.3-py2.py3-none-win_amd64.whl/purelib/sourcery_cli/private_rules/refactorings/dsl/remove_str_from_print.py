from typing import List

from sourcery.dsl.code_change import CodeChange
from sourcery.dsl.proposals import DSLProposer

# pylint: disable=line-too-long


class RemoveStrFromPrintProposer(DSLProposer):
    # TODO once possible within the dsl this should cover the following cases:
    #
    # print(str(value1), value2)  # multiple args
    # print(str(value1), str(value2), value3, str(value4))  # multiple `str` args
    # print(str(value1), sep=my_sep)  # with keyword
    # print(value1, str(value2), str(value3))  # no `str` applied to the first argument
    # print(str(value1), str(value2), value3, str(value4), end='\n\t')  # multiple `str` args + keyword
    #
    # At the moment this is very difficult - we cannot match multiple arguments

    def create_code_changes(self) -> List[CodeChange]:
        return [
            CodeChange(
                pattern="""
                    print(${args1*}, str(${arg}), ${args2*})
                """,
                replacement="""
                    print(${args1}, ${arg}, ${args2})
                """,
            )
        ]

    def description(self) -> str:
        return "Remove unnecessary call to `str()` within `print()`"
