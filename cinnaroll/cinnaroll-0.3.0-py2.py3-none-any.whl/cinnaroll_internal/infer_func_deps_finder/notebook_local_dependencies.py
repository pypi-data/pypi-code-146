import ast
from typing import Set, List, Dict

from cinnaroll_internal import rollout_config
from cinnaroll_internal.infer_func_deps_finder import types, shadowed_names, ast_utils

# atm these are only used by notebook deps finder but this could be reused for getting main local deps from scripts too


def is_rollout_config_subclass_def(node: types.NodeOrStatement) -> bool:
    if not isinstance(node, ast.ClassDef):
        return False
    for base in node.bases:
        if isinstance(base, ast.Name):
            if base.id == rollout_config.RolloutConfig.__name__:
                return True
    return False


def add_used_dependencies(to_add: Set[str], to_visit: List[str], possible_dependencies: Dict[str, str]) -> None:
    if not len(to_visit):
        return
    code = possible_dependencies[to_visit.pop()]
    root = ast.parse(code)
    inspected_node = root.body[0]
    if not types.is_pasteable_code_node(inspected_node):
        raise RuntimeError(f"Unexpected code node in user-written infer function dependencies: {inspected_node}")

    referenced_names = get_referenced_unshadowed_names(inspected_node, set())  # type: ignore

    for name in referenced_names:
        if name in possible_dependencies and name not in to_add:
            to_add.add(name)
            to_visit.append(name)
    add_used_dependencies(to_add, to_visit, possible_dependencies)


def get_referenced_unshadowed_names(
        node: types.FunctionOrClassDefOrLambdaType, shadowed_names_in_outer_scope: Set[str]
) -> Set[str]:
    referenced_names: Set[str] = set()
    shadowed_names_in_current_scope = shadowed_names.get_shadowed_names(node).union(
        shadowed_names_in_outer_scope
    )

    for child_node in ast_utils.walk_disregarding_root(node):
        if types.is_function_or_class_def(child_node) or isinstance(child_node, ast.Lambda):
            referenced_names = referenced_names.union(
                get_referenced_unshadowed_names(
                    child_node, shadowed_names_in_current_scope  # type: ignore
                )
            )
        if isinstance(child_node, ast.Name):
            if isinstance(child_node.ctx, ast.Load):
                if child_node.id not in shadowed_names_in_current_scope:
                    referenced_names.add(child_node.id)

    return referenced_names
