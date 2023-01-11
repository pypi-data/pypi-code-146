import pathlib
import importlib.util
from types import ModuleType


def load_local_module(name: str, path: pathlib.Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    return module


def convert_snake_case_to_pascal_case(snaked_string: str) -> str:
    components = snaked_string.split("_")
    return "".join([component.capitalize() for component in components])
