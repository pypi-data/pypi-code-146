import rjsonnet
import os
from typing import Optional, Union, List, Dict, Tuple, Callable, overload


ImportCallback = Callable[[str, str], Tuple[str, Optional[str]]]


def try_path(dir: str, rel: str):
    """
    Returns content if worked, None if file not found, or throws an exception
    """

    full_path = os.path.join(dir, rel)

    if not os.path.isfile(full_path):
        return full_path, None
    with open(full_path) as f:
        return full_path, f.read()


def default_import_callback(dir: str, rel: str):
    full_path, content = try_path(dir, rel)
    if content:
        return full_path, content
    raise RuntimeError('File not found')


@overload
def evaluate_file(
    filename: str,
    jpathdir: Optional[Union[str, List[str]]] = None,
    max_stack: int = 500,
    gc_min_objects: int = 1000,
    gc_growth_trigger: float = 2.0,
    ext_vars: Dict[str, str] = {},
    ext_codes: Dict[str, str] = {},
    tla_vars: Dict[str, str] = {},
    tla_codes: Dict[str, str] = {},
    max_trace: int = 20,
    import_callback: ImportCallback = default_import_callback,
    native_callbacks: Dict[str, Tuple[str, Callable]] = {},
) -> str: ...


def evaluate_file(
    filename: str,
    import_callback=default_import_callback,
    **kwargs,
) -> str:
    """eval file
    Args:
        filename: jsonnet file
    """
    return rjsonnet.evaluate_file(filename, import_callback=import_callback, **kwargs)


@overload
def evaluate_snippet(
    filename: str,
    snippet: str,
    jpathdir: Optional[Union[str, List[str]]] = None,
    max_stack: int = 500,
    gc_min_objects: int = 1000,
    gc_growth_trigger: float = 2.0,
    ext_vars: Dict[str, str] = {},
    ext_codes: Dict[str, str] = {},
    tla_vars: Dict[str, str] = {},
    tla_codes: Dict[str, str] = {},
    max_trace: int = 20,
    import_callback: ImportCallback = default_import_callback,
    native_callbacks: Dict[str, Tuple[str, Callable]] = {},
) -> str: ...


def evaluate_snippet(
    filename: str,
    snippet: str,
    import_callback=default_import_callback,
    **kwargs,
) -> str:
    """eval snippet
    Args:
        filename: fake name for snippet
        expr: the snippet
    """
    return rjsonnet.evaluate_snippet(filename, snippet, import_callback=import_callback, **kwargs)



