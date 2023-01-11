import ast
from typing import Set

import cinnaroll_internal.infer_func_deps_finder.types as types


def get_shadowed_names(node: types.FunctionOrClassDefOrLambdaType) -> Set[str]:
    shadowed_names: Set[str] = set()
    if types.is_function_def(node) or isinstance(node, ast.Lambda):
        shadowed_names = shadowed_names.union(_get_argument_names_from_function_definition(node))  # type: ignore
    if types.is_function_or_class_def(node):
        shadowed_names = shadowed_names.union(_get_names_introduced_in_function_or_class(node))  # type: ignore
    return shadowed_names


def _get_argument_names_from_function_definition(
        func: types.FunctionDefOrLambdaType
) -> Set[str]:
    arg_names: Set[str] = set()
    function_args = func.args
    for arg in function_args.args:
        arg_names.add(arg.arg)
    for arg in function_args.kwonlyargs:
        arg_names.add(arg.arg)
    if function_args.vararg:
        arg_names.add(function_args.vararg.arg)
    if function_args.kwarg:
        arg_names.add(function_args.kwarg.arg)
    return arg_names


def _get_names_introduced_in_function_or_class(
        node: types.FunctionDefOrClassDefType
) -> Set[str]:
    names: Set[str] = set()
    for statement in node.body:
        if types.is_function_or_class_def(statement):
            names.add(statement.name)  # type: ignore
        else:
            for child_node in ast.walk(statement):
                if isinstance(child_node, ast.Name):
                    if isinstance(child_node.ctx, ast.Store):
                        names.add(child_node.id)
    return names
