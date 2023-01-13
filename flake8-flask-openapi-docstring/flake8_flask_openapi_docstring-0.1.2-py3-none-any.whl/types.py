import ast
from dataclasses import dataclass
from typing import Type


class BaseVisitorResult:
    code: str
    message: str


class MissingOpenAPIFragmentVisitorResult(BaseVisitorResult):
    code = "FO100"
    message = "Missing OpenAPI fragment in docstring"


class InvalidYAMLVisitorResult(BaseVisitorResult):
    code = "FO101"
    message = "Invalid YAML in docstring"


@dataclass
class VisitorResultItem:
    node: ast.AST
    result: Type[BaseVisitorResult]
