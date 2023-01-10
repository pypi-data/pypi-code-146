import typing

from sourcery.analysis.typing.exception_types import parents_of_exception
from sourcery.ast.ast import get_nodes
from sourcery.ast.nodes import ExceptHandler, Name
from sourcery.dsl.code_change import CodeChange
from sourcery.dsl.proposals import DSLProposer
from sourcery.engine.rule_type import RuleType


class RemoveRedundantExceptHandlerProposer(DSLProposer):
    def create_code_changes(self) -> typing.List[CodeChange]:
        return [
            CodeChange(
                pattern="""
                    try:
                        ${statements+}
                    $except{excepts*|self.contains_unreachable(excepts)}
                    else:
                        ${else_statements*}
                    finally:
                        ${finally_statements*}
                """,
                replacement="""
                    try:
                        ${statements}
                    $except{self.cleaned_excepts(excepts)}
                    else:
                        ${else_statements}
                    finally:
                        ${finally_statements}
                """,
            )
        ]

    def contains_unreachable(self, except_handlers: typing.Tuple[ExceptHandler, ...]):
        if len(except_handlers) <= 1:
            return False
        return len(self.cleaned_excepts(except_handlers)) < len(except_handlers)

    def cleaned_excepts(
        self, except_handlers: typing.Tuple[ExceptHandler, ...]
    ) -> typing.Tuple[ExceptHandler, ...]:
        cleaned_except_handlers = []
        handled_exceptions: typing.List[str] = []
        for handler in except_handlers:
            current = self._exception_class_names(handler)
            if not all(
                self._parent_already_handled(c, handled_exceptions) for c in current
            ):
                cleaned_except_handlers.append(handler)
                handled_exceptions.extend(current)
        return tuple(cleaned_except_handlers)

    def _parent_already_handled(
        self, exc_name: str, handled_exceptions: typing.List[str]
    ) -> bool:
        return bool(
            set(parents_of_exception(exc_name)).intersection(handled_exceptions)
        )

    def _exception_class_names(self, except_handler: ExceptHandler) -> typing.List[str]:
        if isinstance(except_handler.type, Name):
            return [except_handler.type.id]
        if except_handler.type is None:
            return [""]
        return [n.unparse() for n in get_nodes(except_handler.type)]

    def description(self) -> str:
        return "Remove unreachable except block"

    def kind(self) -> RuleType:
        return RuleType.REFACTORING
