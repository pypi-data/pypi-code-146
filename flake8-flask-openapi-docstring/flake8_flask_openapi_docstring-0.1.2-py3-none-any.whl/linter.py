from __future__ import annotations

import ast
from typing import Iterable, Tuple, Type

from flake8_flask_openapi_docstring.__version__ import __version__
from flake8_flask_openapi_docstring.visitor import FlaskOpenAPIDocStringVisitor

LinterErrorResult = Tuple[int, int, str, Type["FlaskOpenAPIDocStringLinter"]]


class FlaskOpenAPIDocStringLinter:
    name = "flake8_openapi_docstring"
    version = __version__

    def __init__(self, tree: ast.Module) -> None:
        self.tree = tree

    @classmethod
    def error(cls, lineno: int, offset: int, code: str, message: str) -> LinterErrorResult:
        return (lineno, offset, f"{code} {message}", cls)

    def run(self) -> Iterable[LinterErrorResult]:
        visitor = FlaskOpenAPIDocStringVisitor()
        visitor.visit(self.tree)

        for error_item in visitor.results:
            yield self.error(
                error_item.node.lineno,
                error_item.node.col_offset,
                error_item.result.code,
                error_item.result.message,
            )
