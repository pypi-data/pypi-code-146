import site
from typing import List, Any, Callable
import PIL.Image

from cinnaroll_internal.infer_func_deps_finder.deps_finder import build_deps_finder
from cinnaroll_internal.rollout_config import RolloutConfig
from tests.infer_func_deps_finder.utils import assert_lines_of_string_in_string


some_lambda: Callable[[], None] = lambda: print("plep")  # noqa


# shadows imported PIL.Image - this class should be included and not import
class PIL:  # type: ignore[no-redef] # noqa
    Image = ""


class SomeClass:
    def __init__(self) -> None:
        self.some_attribute = "123"

    def fizz(self) -> str:
        return self.some_attribute + "456"


def function_using_imported_stuff(x: int, y: str) -> List[Any]:
    print(site.getsitepackages())
    return [x, y]


def function_not_used_in_infer_using_function_using_imported_stuff() -> None:
    print(function_using_imported_stuff(1, "2"))


def function_used_in_infer_using_function_using_imported_stuff() -> None:
    print(function_using_imported_stuff(1, "2"))


def function_using_local_class() -> str:
    some_object = SomeClass()
    return some_object.fizz()


class Config(RolloutConfig):
    @staticmethod
    def train_eval(model_object: Any) -> None:
        pass

    @staticmethod
    def infer(model_object: Any, input_data: str) -> str:
        print(PIL.Image)
        some_lambda()
        function_using_imported_stuff(42, "some string")
        function_used_in_infer_using_function_using_imported_stuff()
        return function_using_local_class()


def check_building_infer_func_file_content() -> None:
    required_imports = """
import site
from typing import List
from typing import Any
from typing import Callable
"""
    infer_code = """
def infer(model_object: Any, input_data: str) -> str:
    print(PIL.Image)
    some_lambda()
    function_using_imported_stuff(42, "some string")
    function_used_in_infer_using_function_using_imported_stuff()
    return function_using_local_class()
"""
    functions_and_classes = """
some_lambda: Callable[[], None] = lambda: print("plep")  # noqa

class PIL:  # type: ignore[no-redef] # noqa
    Image = ""

class SomeClass:
    def __init__(self) -> None:
        self.some_attribute = "123"

    def fizz(self) -> str:
        return self.some_attribute + "456"

def function_using_imported_stuff(x: int, y: str) -> List[Any]:
    print(site.getsitepackages())
    return [x, y]

def function_using_local_class() -> str:
    some_object = SomeClass()
    return some_object.fizz()

def function_used_in_infer_using_function_using_imported_stuff() -> None:
    print(function_using_imported_stuff(1, "2"))
"""
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
