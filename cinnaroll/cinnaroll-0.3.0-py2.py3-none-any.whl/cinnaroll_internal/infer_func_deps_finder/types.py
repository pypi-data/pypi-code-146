import ast
from typing import Union

NodeOrStatement = Union[ast.AST, ast.stmt]

FunctionDefType = Union[ast.FunctionDef, ast.AsyncFunctionDef]
FunctionDefOrLambdaType = Union[FunctionDefType, ast.AsyncFunctionDef, ast.Lambda]
FunctionDefOrClassDefType = Union[ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef]
FunctionOrClassDefOrLambdaType = Union[ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef, ast.Lambda]


def is_function_def(node: NodeOrStatement) -> bool:
    return type(node) in (ast.FunctionDef, ast.AsyncFunctionDef)


def is_function_or_class_def(node: NodeOrStatement) -> bool:
    return is_function_def(node) or isinstance(node, ast.ClassDef)


def is_lambda_assignment(node: NodeOrStatement) -> bool:
    if isinstance(node, ast.Assign) or isinstance(node, ast.AnnAssign):
        if isinstance(node.value, ast.Lambda):
            return True
    return False


def is_pasteable_code_node(node: NodeOrStatement) -> bool:
    if is_function_or_class_def(node) or is_lambda_assignment(node):
        return True
    return False
