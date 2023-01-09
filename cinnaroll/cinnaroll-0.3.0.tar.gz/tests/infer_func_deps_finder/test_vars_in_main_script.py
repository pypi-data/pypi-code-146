from typing import Any, Callable
import PIL.Image

from cinnaroll_internal.infer_func_deps_finder.deps_finder import build_deps_finder
from cinnaroll_internal.rollout_config import RolloutConfig
from tests.infer_func_deps_finder.utils import assert_lines_of_string_in_string


x = "foo"
y = "bar"
z = "baz"
somewhat_long_variable_name = "also foo"

model_object = "foo"
var_in_function_scope = "bar"  # used later in function scope

# x is an arg, y is from outer scope
some_lambda: Callable[[str], None] = lambda x: print(x + y)  # noqa


class PIL:  # type: ignore[no-redef] # noqa
    class ImageClass:
        def open(self) -> None:
            print("opened")
    Image = ImageClass()


class SomeClass:
    m = "foo"

    def __init__(self) -> None:
        print(x)

    def class_func(self) -> None:
        print(self.m)


def function_using_global_var(x: str) -> None:
    def nested_function(y: str) -> None:
        def next_nested_function() -> None:
            print(k + y + z)  # z not in scope
        print(y + k)  # both names in scope
    k = "foo"
    print(y + x)  # y not in scope (inner func arg)


def function_defining_a_class() -> None:
    var_in_function_scope = "foo"

    class ClassInsideFunction:
        def __init__(self) -> None:
            print(var_in_function_scope)  # shouldn't be global
            print(x)  # this should be


def function_with_var_declaration_inside_an_expression() -> None:
    for i in range(10):
        x = i
    print(x)


class Config(RolloutConfig):
    @staticmethod
    def train_eval(model_object: Any) -> None:
        pass

    @staticmethod
    def infer(model_object: Any, input_data: str) -> str:
        PIL.Image.open()
        function_using_global_var(x)
        function_with_var_declaration_inside_an_expression()
        _ = SomeClass()
        some_lambda("foo")
        function_defining_a_class()
        print(model_object)  # in scope - argument
        print(input_data)  # in scope - argument
        # x in scope, y from outer scope
        _ = lambda x: print(x + y)  # noqa
        return somewhat_long_variable_name + x + y + z  # everything from outer scope


def check_building_infer_func_file_content() -> None:
    required_imports = """
from typing import Any
from typing import Callable
import pickle
"""

    loading_global_vars_dict = """
user_globals_file = open("user_defined_globals.pickle", "rb")
user_globals = pickle.load(user_globals_file)
user_globals_file.close()
"""

    infer_code = """
def infer(model_object: Any, input_data: str) -> str:
    PIL.Image.open()
    function_using_global_var(user_globals['x'])
    function_with_var_declaration_inside_an_expression()
    _ = SomeClass()
    some_lambda("foo")
    function_defining_a_class()
    print(model_object)
    print(input_data)
    _ = lambda x: print(x + user_globals['y'])
    return user_globals['somewhat_long_variable_name'] + user_globals['x'] + user_globals['y'] + user_globals['z']
"""
    functions_and_classes = """
def function_using_global_var(x: str) -> None:
    def nested_function(y: str) -> None:
        def next_nested_function() -> None:
            print(k + y + user_globals['z'])  # z not in scope
        print(y + k)  # both names in scope
    k = "foo"
    print(user_globals['y'] + x)  # y not in scope (inner func arg)


class PIL:  # type: ignore[no-redef] # noqa
    class ImageClass:
        def open(self) -> None:
            print("opened")
    Image = ImageClass()

class SomeClass:
    m = "foo"

    def __init__(self) -> None:
        print(user_globals['x'])

    def class_func(self) -> None:
        print(self.m)

def function_defining_a_class() -> None:
    var_in_function_scope = "foo"

    class ClassInsideFunction:
        def __init__(self) -> None:
            print(var_in_function_scope)  # shouldn't be global
            print(user_globals['x'])  # this should be

some_lambda: Callable[[str], None] = lambda x: print(x + user_globals['y'])  # noqa

def function_with_var_declaration_inside_an_expression() -> None:
    for i in range(10):
        x = i
    print(x)
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

    expect = "\n".join([required_imports, loading_global_vars_dict, infer_code, functions_and_classes])

    deps_finder = build_deps_finder(None, config)

    got = deps_finder.get_infer_with_used_global_variables().output_file_content

    assert_lines_of_string_in_string(expect, got)


if __name__ == "__main__":
    check_building_infer_func_file_content()
