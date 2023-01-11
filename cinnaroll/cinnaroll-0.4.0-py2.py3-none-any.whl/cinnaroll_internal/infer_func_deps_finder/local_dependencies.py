import ast
import inspect
from types import ModuleType
from typing import Dict, Any

from cinnaroll_internal.infer_func_deps_finder import modules
from cinnaroll_internal.post_training_validation import InferFunctionError


class LocalModuleInInferDependenciesError(InferFunctionError):
    def __init__(self, module: ModuleType) -> None:
        super().__init__(
            f"In infer func or its dependencies, "
            f"you've referenced a local module (code in your local file): \n"
            f"{module} \n"
            f"Handling stuff from other files in infer func is not yet implemented.\n"
            f"For now, paste referenced code to the file containing infer func and config. "
        )


class LocalClassOrFunctionInInferDependenciesError(InferFunctionError):
    def __init__(self, class_or_function: Any, module_of_dependency: ModuleType) -> None:
        super().__init__(
            f"In infer func or its dependencies, "
            f"you've referenced {class_or_function}\n"
            f"from local module (code in your local file) {module_of_dependency} \n"
            f"Handling stuff from other files in infer func is not yet implemented.\n"
            f"For now, paste referenced code to the file containing infer func and config. "
        )


def find_function_main_module_class_and_function_dependencies(
    func_code: str,
    main_module_members: Dict[str, Any],
    main_module_class_and_function_deps_code: Dict[str, str],
) -> None:
    root = ast.parse(func_code)
    for node in ast.walk(root):
        if isinstance(node, ast.Name):
            if node.id in main_module_members:
                if node.id in main_module_class_and_function_deps_code:
                    return None
                thing_to_paste = main_module_members[node.id]
                if inspect.ismodule(thing_to_paste):
                    if (
                        modules.get_module_origin(thing_to_paste)
                        == modules.ModuleOrigin.LOCAL
                    ):
                        raise LocalModuleInInferDependenciesError(thing_to_paste)
                if inspect.isfunction(thing_to_paste) or inspect.isclass(
                    thing_to_paste
                ):
                    things_module = inspect.getmodule(thing_to_paste)
                    if not things_module:
                        return None
                    if (
                        modules.get_module_origin(things_module)
                        == modules.ModuleOrigin.LOCAL
                    ):
                        if things_module.__name__ != "__main__":
                            raise LocalClassOrFunctionInInferDependenciesError(
                                thing_to_paste, things_module
                            )
                        else:
                            things_code = inspect.getsource(thing_to_paste)
                            main_module_class_and_function_deps_code[
                                node.id
                            ] = things_code
                            find_function_main_module_class_and_function_dependencies(
                                things_code,
                                main_module_members,
                                main_module_class_and_function_deps_code,
                            )


def get_functions_and_classes_from_main_script_to_paste_to_infer_py(
    infer_func_code: str, main_module_members: Dict[str, Any]
) -> str:
    func_and_class_deps_code = ""
    main_module_class_and_function_deps_code: Dict[str, str] = {}
    find_function_main_module_class_and_function_dependencies(
        infer_func_code, main_module_members, main_module_class_and_function_deps_code
    )
    for name, code in main_module_class_and_function_deps_code.items():
        func_and_class_deps_code = "\n".join([func_and_class_deps_code, code])
    return func_and_class_deps_code
