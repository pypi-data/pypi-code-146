import ast
import sys
from pathlib import Path
from typing import Any, Dict
import traceback

from cinnaroll_internal import constants
from cinnaroll_internal.rollout_config import RolloutConfig

INFER_MODEL_OBJECT_ARG_NAME = "model_object"
INFER_INPUT_DATA_ARG_NAME = "input_data"
INFER_ERRORS_LOG_FILENAME = "generated_file_error_log"


def verify_infer_works_for_sample_input(
        infer_file_content: str,
        user_defined_globals: Dict[str, Any],
        rollout_config: RolloutConfig,
        cache_dir_path: Path
) -> None:
    globals_for_exec = {
        constants.GLOBAL_VARS_DICT_NAME: user_defined_globals,
        INFER_INPUT_DATA_ARG_NAME: rollout_config.infer_func_input_sample,
        INFER_MODEL_OBJECT_ARG_NAME: rollout_config.model_object,
    }
    tree = ast.parse(infer_file_content)
    try:
        exec(compile(tree, filename="infer_func_test", mode="exec"), globals_for_exec)
    except Exception:
        log_file_path = cache_dir_path / INFER_ERRORS_LOG_FILENAME
        with open(log_file_path, "w") as file:
            traceback.print_exc(file=file)
        print("\nGenerated code is faulty. "
              "Check documentation and verify infer function satisfies current constraints.\n"
              f"Please report this issue to cinnaroll support, attaching error traceback from {log_file_path} "
              f"and code from the script you're doing rollout from.")
        sys.exit(1)
