from typing import List

from sourcery.dsl.code_change import CodeChange
from sourcery.dsl.proposals import DSLProposer
from sourcery.engine.rule_type import RuleType


class RaiseSpecificErrorProposer(DSLProposer):
    def create_code_changes(self) -> List[CodeChange]:
        return [
            CodeChange(pattern="raise Exception from ${cause?}"),
            CodeChange(pattern="raise Exception(${error_msg?}) from ${cause?}"),
            CodeChange(pattern="raise BaseException from ${cause?}"),
            CodeChange(pattern="raise BaseException(${error_msg?}) from ${cause?}"),
        ]

    def description(self) -> str:
        return "Raise a specific error instead of the general Exception"

    def kind(self) -> RuleType:
        return RuleType.COMMENT

    def explanation(self) -> str:
        return """
            If a piece of code raises a specific exception type
            rather than the generic BaseException or Exception,
            the calling code can:

            - get more information about what type of error it is
            - define specific exception handling for it

            How can you solve this?

            - Use one of the built-in exceptions of the standard library.
            - Define your own error class that subclasses `Exception`.
        """
