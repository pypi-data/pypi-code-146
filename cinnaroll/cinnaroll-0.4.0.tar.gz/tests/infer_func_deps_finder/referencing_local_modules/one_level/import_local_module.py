from typing import Any
import tests.infer_func_deps_finder.referencing_local_modules.one_level.helpers.other_file as other_file

from cinnaroll_internal.infer_func_deps_finder.deps_finder import build_deps_finder
from cinnaroll_internal.rollout_config import RolloutConfig
from tests.infer_func_deps_finder.utils import assert_lines_of_string_in_string

# todo: rename to test_.... when this test and logic allowing it to pass are implemented


class Config(RolloutConfig):
    @staticmethod
    def train_eval(model_object: Any) -> None:
        pass

    @staticmethod
    def infer(model_object: Any, input_data: str) -> str:
        other_file.func_from_other_file()
        return ""


def check_building_infer_func_file_content() -> None:
    required_imports = """"""
    infer_code = """"""
    functions_and_classes = """"""

    config = Config(
        project_id="5zVm00n97",
        model_name=None,
        model_object=None,
        model_input_sample=None,
        infer_func_input_format="img",
        infer_func_output_format="json",
        infer_func_input_sample=None,
    )

    expect = "\n".join([required_imports, infer_code, functions_and_classes])

    deps_finder = build_deps_finder(None, config)

    got = deps_finder.get_infer_with_used_global_variables().output_file_content

    assert_lines_of_string_in_string(expect, got)


if __name__ == "__main__":
    check_building_infer_func_file_content()
