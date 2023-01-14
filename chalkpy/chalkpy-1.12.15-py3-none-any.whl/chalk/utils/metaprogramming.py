import builtins
import types
from typing import Any, Dict, List, Mapping, Optional, Type


# A sentinel object to detect if a parameter is supplied or not.
# Use a class to give it a better repr.
class _MISSING_TYPE:
    def __repr__(self):
        return "<MISSING>"


MISSING = _MISSING_TYPE()


def create_fn(
    name: str,
    args: List[str],
    body: List[str],
    *,
    _globals: Optional[Dict[str, Any]] = None,
    _locals: Optional[Dict[str, Any]] = None,
    return_type: Any = MISSING,
):
    # Note that we mutate locals when exec() is called.  Caller
    # beware!  The only callers are internal to this module, so no
    # worries about external callers.
    if _locals is None:
        _locals = {}
    if "BUILTINS" not in _locals:
        _locals["BUILTINS"] = builtins
    return_annotation = ""
    if return_type is not MISSING:
        _locals["_return_type"] = return_type
        return_annotation = "->_return_type"
    body_text = "\n".join(f"  {b}" for b in body)

    # Compute the text of the entire function.
    txt = f' def {name}({",".join(args)}){return_annotation}:\n{body_text}'

    local_vars = ", ".join(_locals.keys())
    txt = f"def __create_fn__({local_vars}):\n{txt}\n return {name}"
    ns: Mapping[str, Any] = {}
    exec(txt, _globals, ns)
    return ns["__create_fn__"](**_locals)


def set_new_attribute(cls: Type, name: str, value: Any):
    # Never overwrites an existing attribute.  Returns True if the
    # attribute already exists.
    if name in cls.__dict__:
        return True
    if isinstance(value, types.FunctionType):
        value.__qualname__ = f"{cls.__qualname__}.{value.__name__}"
    setattr(cls, name, value)
    return False


def field_assign(name: str, value: str, self_name: str):
    # self_name is what "self" is called in this function: don't
    # hard-code "self", since that might be a field name.
    # Only assigning values that are not "MISSING" so attempting to access
    # a missing value will immediately raise an AttributeError rather than return MISSING
    return f"if {value} is not MISSING: {self_name}.{name}={value}"
