import ast
import inspect
from collections import namedtuple
from types import ModuleType
from typing import Any, Dict, Optional, List, Set, Iterator, Tuple

from cinnaroll_internal import utils
from cinnaroll_internal.infer_func_deps_finder.modules import (
    get_module_origin,
    ModuleOrigin,
)

Import = namedtuple("Import", ["module", "name", "alias"])


def get_used_imports_and_import_statements_to_paste_to_infer_py(
    infer_func_code: str, main_module_members: Dict[str, Any], main_module: ModuleType
) -> Tuple[Dict[str, Import], str]:
    all_imports = get_module_imports(main_module)
    used_imports_aliases = build_set_of_used_import_aliases(infer_func_code, all_imports)
    used_imports = {
        aliased_name: imp
        for aliased_name, imp in all_imports.items()
        if aliased_name in used_imports_aliases
    }
    used_import_statements = build_list_of_non_local_import_statements(
        used_imports, main_module_members
    )
    return used_imports, "\n".join(used_import_statements)


# non-local here means not from user defined module - can be from built-ins, Python lib and 3rd party packages
def build_non_local_import_statement(imported_thing: Any, imp: Import) -> Optional[str]:
    if inspect.ismodule(imported_thing):
        if get_module_origin(imported_thing) == ModuleOrigin.LOCAL:
            return None
    else:
        things_module = inspect.getmodule(imported_thing)
        # module of the imported object  might not be determinable
        if not things_module:
            return None
        if get_module_origin(things_module) == ModuleOrigin.LOCAL:
            return None

    if not imp.module:
        statement = f"import {imp.name}"
    else:
        statement = f"from {imp.module} import {imp.name}"
    if imp.alias:
        statement += f" as {imp.alias}"
    return statement


def build_list_of_non_local_import_statements(
    used_imports: Dict[str, Import], members: Dict[str, Any]
) -> List[str]:
    import_statements: List[str] = []
    for aliased_name, imp in used_imports.items():
        # if you eg. `import PIL.Image`, PIL.Image should be the import but there's only PIL in members
        if "." in aliased_name:
            member = members[aliased_name.split(".")[0]]
        else:
            member = members[aliased_name]

        utils.append_if_not_none(
            import_statements,
            build_non_local_import_statement(member, imp),
        )
    return import_statements


def code_imports(code: str) -> Iterator[Import]:
    root = ast.parse(code)

    for node in ast.walk(root):
        if isinstance(node, ast.Import):
            module = None
        elif isinstance(node, ast.ImportFrom):
            module = node.module  # .split('.')
        else:
            continue

        for n in node.names:  # type: ignore
            yield Import(
                module,
                n.name,
                n.asname,
            )
            # yield Import(module, n.name.split('.'), n.asname)


# creates dict with Import values and key being whatever the imported thing is referred to as
def get_imports_from_code(code: str) -> Dict[str, Import]:
    module_imports = {}
    for imp in code_imports(code):
        if imp.alias:
            module_imports[imp.alias] = imp
        elif imp.name:
            module_imports[imp.name] = imp
        else:
            module_imports[imp.module] = imp
    return module_imports


# this expects non-built-in module since built-ins have no __file__ attr
def get_module_imports(module: ModuleType) -> Dict[str, Import]:
    try:
        module_sourcefile = module.__file__
        if not module_sourcefile:
            return {}
        fp = open(module_sourcefile)
        code = fp.read()
        fp.close()
    except AttributeError:
        return {}
    return get_imports_from_code(code)


def get_possibly_imported_string_from_attribute(node: ast.Attribute) -> str:
    if isinstance(node.value, ast.Attribute):
        return f"{get_possibly_imported_string_from_attribute(node.value)}.{node.attr}"
    elif isinstance(node.value, ast.Name):
        return f"{node.value.id}.{node.attr}"
    else:
        # Value property of ast.Attribute can be any arbitrary ast.Expression
        # (what can be an expression is listed in the grammar
        # https://docs.python.org/3/library/ast.html#abstract-grammar
        # but I currently don't think cases other than nested Attributes and Names are worth
        # further inspection since eg.
        # module.Class.function(some_arg) is code containing a valid Attribute but
        # import statements only contain name-ish entities.
        return ""


def build_set_of_used_import_aliases(code: str, imps: Dict[str, Import]) -> Set[str]:
    imports_aliases = imps.keys()
    root = ast.parse(code)
    used = set()

    for node in ast.walk(root):
        if isinstance(node, ast.Name):
            if node.id in imports_aliases:
                used.add(node.id)
        # todo: handle case with a.b.c when a.b.c or a.b is an imported name - it's a nested attribute
        elif isinstance(node, ast.Attribute):
            attribute_string = get_possibly_imported_string_from_attribute(node)
            if attribute_string in imports_aliases:
                used.add(attribute_string)
        else:
            continue
    return used
