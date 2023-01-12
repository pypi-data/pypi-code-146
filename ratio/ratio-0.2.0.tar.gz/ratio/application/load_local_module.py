import pathlib
import importlib.util
from types import ModuleType


def load_local_module(name: str, path: pathlib.Path) -> ModuleType | None:
    return None
    spec = importlib.util.spec_from_file_location(name, path)

    if spec is None:
        return None

    module = importlib.util.module_from_spec(spec)

    if module is None:
        return None

    spec.loader.exec_module(module)

    return module
