from sourcery.ast import FunctionDef, Node


def not_in_equality_dunder(node: Node) -> bool:
    scope = node.scope()
    return not (
        isinstance(scope, FunctionDef) and scope.name.id in {"__eq__", "__ne__"}
    )
