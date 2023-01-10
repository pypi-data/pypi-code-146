from typing import List

from sourcery.ast import Node, Raise
from sourcery.dsl.code_change import CodeChange
from sourcery.dsl.proposals import DSLProposer
from sourcery.engine.rule_type import RuleType


class DoNotUseBareExceptProposer(DSLProposer):
    def create_code_changes(self) -> List[CodeChange]:
        return [
            CodeChange(
                pattern="""
                    try:
                        ${statements+}
                    $except{excepts*}
                    except:
                        ${handler_statements+ |
                            not self.ends_with_raise(handler_statements)
                        }
                    else:
                        ${else_statements*}
                    finally:
                        ${finally_statements*}
                """,
                replacement="""
                    try:
                        ${statements}
                    $except{excepts}
                    except Exception:
                        ${handler_statements}
                    else:
                        ${else_statements}
                    finally:
                        ${finally_statements}
                """,
            )
        ]

    def description(self) -> str:
        return "Use `except Exception:` rather than bare `except:`"

    def kind(self) -> RuleType:
        return RuleType.SUGGESTION

    def ends_with_raise(self, nodes: List[Node]) -> bool:
        return isinstance(nodes[-1], Raise)
