import importlib.util
from importlib import import_module
from pathlib import Path
from types import ModuleType
from typing import Callable

import daiquiri
from parsy import regex, seq, string

logger = daiquiri.getLogger(__name__)


def load_function_from_module(function_name: str, *, module_name: str) -> Callable | None:
    module = import_module(module_name)
    return getattr(module, function_name, None)


def load_python_module_from_path(module_path: Path, *, module_name: str) -> ModuleType:
    logger.debug("Loading Python module from path %r", str(module_path))
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    if spec is None:
        raise ValueError(f"Could not build module spec from file location {str(module_path)}")
    module = importlib.util.module_from_spec(spec)
    if spec.loader is None:
        raise ValueError(f"Module spec built from file location {str(module_path)} has no loader")
    spec.loader.exec_module(module)
    return module


def parse_callable(callable_ref: str) -> Callable | None:
    module_name = regex(r"(\w|\.)+").desc("module name")
    function_name = regex(r"(\w|\.)+").desc("function name")
    parser = seq(module_name << string(":"), function_name)
    module_name, function_name = parser.parse(callable_ref)
    return load_function_from_module(function_name, module_name=module_name)
