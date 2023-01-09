import ast
from typing import Iterable, Any

ERROR_CODE = "UUG001"
CHECK = "unused global variable"
VERSION = "0.1.9"


class GlobalVariableLoadCounter(ast.NodeVisitor):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.id_to_loads = {}
        self.id_to_store_info = {}

    def visit_Name(self, name: ast.Name) -> None:
        if isinstance(name.ctx, ast.Load) and name.id in self.id_to_loads:
            self.id_to_loads[name.id] += 1
        elif isinstance(name.ctx, ast.Store):
            self.id_to_loads[name.id] = 0
            self.id_to_store_info[name.id] = {
                "end_lineno": name.end_lineno,
                "col_offset": name.col_offset
            }


class Plugin:
    name = "flake8-unused-globals"
    version = VERSION

    def __init__(self, tree: ast.Module) -> None:
        self.tree = tree

    @property
    def global_variables(self) -> set[str]:
        variables: set[str] = set()

        for assignment in self.tree.body:
            if isinstance(assignment, ast.Assign):
                for target in assignment.targets:
                    if isinstance(target, ast.Name):
                        variables.add(target.id)
            elif (
                isinstance(assignment, ast.AnnAssign)
                and isinstance(assignment.target, ast.Name)
            ):
                variables.add(assignment.target.id)

        return variables

    def run(self) -> Iterable[tuple[int, int, str, str]]:
        errors_by_id = {}
        load_counter = GlobalVariableLoadCounter()
        load_counter.visit(self.tree)

        for id_, loads in load_counter.id_to_loads.items():
            if id_ in self.global_variables and loads == 0:
                store_info = load_counter.id_to_store_info[id_]
                text = f"{ERROR_CODE} Unused global variable '{id_}'"
                error_info = (
                    store_info["end_lineno"],
                    store_info["col_offset"],
                    text,
                    CHECK
                )
                errors_by_id[id_] = error_info

        for item in self.tree.body[::-1]:
            if isinstance(item, ast.Assign):
                for target in item.targets:
                    if (
                        isinstance(target, ast.Name)
                        and target.id in errors_by_id
                    ):
                        errors_by_id.pop(target.id)
            elif (
                isinstance(item, ast.AnnAssign)
                and isinstance(item.target, ast.Name)
                and item.target.id in errors_by_id
            ):
                errors_by_id.pop(item.target.id)
            else:
                break

        return list(errors_by_id.values())
