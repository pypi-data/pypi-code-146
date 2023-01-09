import os
import sys
from typing import Callable

import papermill as pm
import scrapbook as sb
from pymbse.commons import text_file

from pymbse.query.model_api.executor.executor import Executor

MODEL_RESULTS_KEYWORD = "model_results"


class ScriptExecutor(Executor):
    """ScriptExecutor class is implementing Executor abstract class and, particularly, the execute method for
    scripts obtained from notebooks.

    """

    def execute(self) -> dict:
        write_input_files(self.model_dependency_config.get_root_dir(), self.input_files)

        script = self.model_dependency_config.get_script_name_without_ext()
        cwd = os.getcwd()

        os.chdir(self.model_dependency_config.get_root_dir())

        # Unload a module to allow for its modification between subsequent calls
        if script in sys.modules.keys():
            sys.modules.pop(script)
        run = ScriptExecutor._import_function_from_module(script, "run_" + script)
        try:
            fom_model = run(**self.input_parameters)
        except:
            raise
        finally:
            os.chdir(cwd)

        return fom_model

    @staticmethod
    def _import_function_from_module(module: str, function: str) -> Callable:
        return getattr(__import__(module), function)


class NotebookExecutor(Executor):
    """NotebookExecutor class is implementing Executor abstract class and, particularly, the execute method for
    notebooks.

    """

    def execute(self) -> dict:
        write_input_files(self.model_dependency_config.get_root_dir(), self.input_files)
        model_out_abs_path = self.model_dependency_config.get_ipynb_out_abs_path()
        pm.execute_notebook(
            self.model_dependency_config.model_abs_path,
            model_out_abs_path,
            cwd=self.model_dependency_config.get_root_dir(),
            parameters=self.input_parameters,
        )

        return sb.read_notebook(model_out_abs_path).scraps[MODEL_RESULTS_KEYWORD].data


def write_input_files(root_dir: str, input_files: dict) -> None:
    for input_file_rel_path, input_file_content in input_files:
        input_file_abs_path = os.path.join(root_dir, input_file_rel_path)
        text_file.write(input_file_abs_path, input_file_content)