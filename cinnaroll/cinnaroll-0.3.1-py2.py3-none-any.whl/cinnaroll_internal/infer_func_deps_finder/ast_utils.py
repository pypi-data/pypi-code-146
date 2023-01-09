import ast
from typing import Generator


def walk_disregarding_root(node: ast.AST) -> Generator[ast.AST, None, None]:
    """
    Recursively yield all descendant nodes in the tree starting at *node*
    (EXCLUDING *node* itself), in no specified order.  This is useful if you
    only want to modify nodes in place and don't care about the context.
    """
    from collections import deque
    todo = deque([node])
    node = todo.popleft()
    todo.extend(ast.iter_child_nodes(node))
    while todo:
        node = todo.popleft()
        todo.extend(ast.iter_child_nodes(node))
        yield node
