import __main__
import abc
import ast
import importlib
import inspect
from modulefinder import ModuleFinder
from types import ModuleType
from typing import Any, Dict, Optional, Set, List, Tuple

import asttokens.util

from cinnaroll_internal import utils
from cinnaroll_internal.infer_func_deps_finder import (
    modules,
    imports,
    infer_func_file,
    types
)
from cinnaroll_internal.infer_func_deps_finder.global_variables import UsedGlobalVariables
from cinnaroll_internal.infer_func_deps_finder.local_dependencies import (
    get_functions_and_classes_from_main_script_to_paste_to_infer_py,
)
from cinnaroll_internal.infer_func_deps_finder.notebook_local_dependencies import add_used_dependencies, \
    is_rollout_config_subclass_def
from cinnaroll_internal.jupyter_notebook import Notebook
from cinnaroll_internal.rollout_config import RolloutConfig


class Infer:
    def __init__(self, output_file_content: str, test_file_content: str, global_variables: Dict[str, Any]) -> None:
        self.output_file_content = output_file_content
        self.test_file_content = test_file_content
        self.global_variables = global_variables


class DependenciesFinder:
    def __init__(self, rollout_config: RolloutConfig) -> None:
        self.main_module_members = {
            member[0]: member[1] for member in modules.get_relevant_module_members(__main__)
        }
        self.rollout_config = rollout_config

    def get_infer_with_used_global_variables(self) -> Infer:
        infer_code_with_dependencies = self.get_infer_code_with_user_code_dependencies_from_main_module()

        used_imports, used_import_statements = self.get_imports_and_used_import_statements(
            infer_code_with_dependencies
        )

        infer = self.build_infer(infer_code_with_dependencies, used_imports, used_import_statements)

        return infer

    def build_infer(
            self, infer_code_with_dependencies: str, used_imports: Dict[str, imports.Import], used_import_statements: str
    ) -> Infer:
        used_global_vars = UsedGlobalVariables(
            infer_code_with_dependencies, self.main_module_members, used_imports
        )

        infer_files_content = infer_func_file.build_infer_py_files_content(
            infer_code_with_dependencies,
            used_import_statements,
            (used_global_vars.locations if used_global_vars.variables else None),
        )

        return Infer(infer_files_content.output, infer_files_content.test, used_global_vars.variables)

    @abc.abstractmethod
    def get_infer_code_with_user_code_dependencies_from_main_module(self) -> str:
        pass

    @abc.abstractmethod
    def get_imports_and_used_import_statements(
            self, infer_code_with_dependencies: str
    ) -> Tuple[Dict[str, imports.Import], str]:
        pass


class NotebookDepsFinder(DependenciesFinder):
    def __init__(self, current_notebook: Notebook, rollout_config: RolloutConfig) -> None:
        super().__init__(rollout_config)
        self.infer_func_name = rollout_config.infer.__name__
        self.notebook_path = current_notebook.path
        self.notebook_code = current_notebook.get_notebook_code()
        self.cut_non_python_statements_from_code()

    def get_infer_code_with_user_code_dependencies_from_main_module(self) -> str:
        functions_and_classes = self.get_class_and_function_names_from_code()
        # classes, functions and lambda assignments that user wrote and are used by infer or its dependencies
        infer_with_used_code_dependencies_code = self.get_used_user_dependencies_code(functions_and_classes)
        return infer_with_used_code_dependencies_code

    def get_imports_used_by_code(self, infer_code_with_dependencies: str) -> Dict[str, imports.Import]:
        all_imports = imports.get_imports_from_code(self.notebook_code)
        used_imports_aliases = imports.build_set_of_used_import_aliases(
            infer_code_with_dependencies, all_imports
        )
        used_imports = {
            aliased_name: imp
            for aliased_name, imp in all_imports.items()
            if aliased_name in used_imports_aliases
        }
        return used_imports

    def build_used_import_statements(self, used_imports: Dict[str, imports.Import]) -> str:
        return "\n".join(imports.build_list_of_non_local_import_statements(
            used_imports, self.main_module_members
        ))

    def get_imports_and_used_import_statements(
            self, infer_code_with_dependencies: str
    ) -> Tuple[Dict[str, imports.Import], str]:
        used_imports = self.get_imports_used_by_code(infer_code_with_dependencies)
        used_import_statements = self.build_used_import_statements(used_imports)
        return used_imports, used_import_statements

    def cut_non_python_statements_from_code(self) -> None:
        lines = self.notebook_code.splitlines()
        clean_code: List[str] = []
        for line in lines:
            if not line.lstrip().startswith(("%", "!")):
                clean_code.append(line)
        self.notebook_code = "\n".join(clean_code)

    def get_class_and_function_names_from_code(self) -> Set[str]:
        # this only gets classes and functions from outer scope since they are visible from infer
        # this won't see stuff defined in expressions such as loops, conditionals etc.
        # which is kind of a pickle, but should be really rare
        names = set()
        root = ast.parse(self.notebook_code)
        for node in root.body:
            if types.is_lambda_assignment(node):
                if isinstance(node, ast.AnnAssign):
                    if isinstance(node.target, ast.Name):
                        names.add(node.target.id)
                elif isinstance(node, ast.Assign):
                    for target in node.targets:
                        if isinstance(target, ast.Name):
                            names.add(target.id)
            if types.is_function_or_class_def(node):
                names.add(node.name)  # type: ignore
        return names

    def get_used_user_dependencies_code(self, possible_dependency_names: Set[str]) -> str:
        final_code = ""
        user_code_lines = self.notebook_code.splitlines()
        # definitions and lambda assignments
        functions_lambdas_classes_code: Dict[str, str] = {}
        tokens = asttokens.ASTTokens(self.notebook_code, parse=True)

        for node in asttokens.util.walk(tokens.tree):  # type: ignore
            if is_rollout_config_subclass_def(node):
                functions_lambdas_classes_code[
                    self.infer_func_name
                ] = self.get_infer_code_from_rollout_config_subclass_def(node, tokens, user_code_lines)  # type: ignore
            if types.is_function_or_class_def(node):
                if node.name in possible_dependency_names:  # type: ignore
                    (start_lineno, _), (end_lineno, _) = (tokens.get_text_positions(node, padded=False))
                    functions_lambdas_classes_code[node.name] = "\n".join(  # type: ignore
                        user_code_lines[start_lineno - 1: end_lineno]
                    )
            if types.is_lambda_assignment(node):
                if isinstance(node, ast.AnnAssign):
                    if isinstance(node.target, ast.Name):
                        if node.target.id in possible_dependency_names:
                            (start_lineno, _), (end_lineno, _) = (tokens.get_text_positions(node, padded=False))
                            functions_lambdas_classes_code[node.target.id] = "\n".join(
                                user_code_lines[start_lineno - 1: end_lineno]
                            )
                if isinstance(node, ast.Assign):
                    for target in node.targets:
                        if isinstance(target, ast.Name):
                            if target.id in possible_dependency_names:
                                (start_lineno, _), (end_lineno, _) = (tokens.get_text_positions(node, padded=False))
                                functions_lambdas_classes_code[node.target.id] = "\n".join(  # type: ignore
                                    user_code_lines[start_lineno - 1: end_lineno]
                                )

        to_visit: List[str] = [self.infer_func_name]
        to_add: Set[str] = {self.infer_func_name}
        add_used_dependencies(to_add, to_visit, functions_lambdas_classes_code)

        for name in to_add:
            final_code += functions_lambdas_classes_code[name] + "\n\n"
        return final_code

    def get_infer_code_from_rollout_config_subclass_def(
            self, config_class_node: ast.ClassDef, tokens: asttokens.ASTTokens, user_code_lines: List[str]
    ) -> str:
        for node in asttokens.util.walk(config_class_node):
            if isinstance(node, ast.FunctionDef):
                if node.name is self.infer_func_name:
                    (start_lineno, _), (end_lineno, _) = (tokens.get_text_positions(node, padded=False))
                    return utils.remove_surplus_indent_and_comments_from_function_code(
                        "\n".join(user_code_lines[start_lineno - 1: end_lineno]), self.infer_func_name
                    )
        raise RuntimeError("infer function code could not be fetched from config.")


class ScriptDepsFinder(DependenciesFinder):
    def __init__(self, rollout_config: RolloutConfig) -> None:
        super().__init__(rollout_config)
        self.infer_code = utils.get_function_code_without_comments(rollout_config.infer)

    def get_infer_code_with_user_code_dependencies_from_main_module(self) -> str:
        classes_and_functions_code = get_functions_and_classes_from_main_script_to_paste_to_infer_py(
            self.infer_code, self.main_module_members
        )
        infer_code_with_class_and_function_deps = infer_func_file.infer_code_with_class_and_function_deps(
            self.infer_code, classes_and_functions_code
        )
        return infer_code_with_class_and_function_deps

    def get_imports_and_used_import_statements(
            self, infer_code_with_dependencies: str
    ) -> Tuple[Dict[str, imports.Import], str]:
        (
            used_imports, non_local_import_statements,
        ) = imports.get_used_imports_and_import_statements_to_paste_to_infer_py(
            infer_code_with_dependencies, self.main_module_members, __main__
        )
        return used_imports, non_local_import_statements


def build_deps_finder(
        current_notebook: Optional[Notebook],
        rollout_config: RolloutConfig) -> DependenciesFinder:
    if current_notebook:
        return NotebookDepsFinder(current_notebook, rollout_config)
    else:
        return ScriptDepsFinder(rollout_config)


def extract_modules(this_script: str) -> Dict[str, str]:
    extracted_modules = {}
    finder = ModuleFinder()
    finder.run_script(this_script)
    found_modules = finder.modules.items()

    for name, module in found_modules:
        # filtering out dunder functions
        if not name.startswith("__"):
            try:
                imported_module: ModuleType = importlib.import_module(name)
                source_code = inspect.getsource(imported_module)
                extracted_modules[name] = source_code
            except Exception:
                pass

    return extracted_modules
