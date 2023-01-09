
from typing import (Any, Iterable, Optional, GenericAlias, # type: ignore
                     _UnionGenericAlias) # type: ignore


def _basic(fieldtype, value, name: str) -> Optional[str]:
    if not isinstance(value, fieldtype):
        return f"'{name}' must be instance of type '{fieldtype.__name__}', not '{type(value).__name__}.'"

def _tuple(types, value, name: str) -> Optional[str]:
    if not types and not value:
        return
    if types and types[-1] is not Ellipsis:
        if len(types) != len(value):
            return f'Length of the tuple {value} not {len(types)}'
    errormessages = []
    for _type, subvalue in zip(types, value):
        errormessage = _validate(_type, subvalue, name)
        if errormessage is not None:
            errormessages.append(errormessage)
    if errormessages:
        return ' '.join(errormessages)

def _set(fieldtype, values, name: str) -> Optional[str]:
    errormessages = []
    for item in values:
        errormessage = _validate(fieldtype, item, name)
        if errormessage is not None:
            errormessages.append(errormessage)
    if errormessages:
        return ' '.join(errormessages)

def _dict(types: tuple[type, type], value, name: str) -> Optional[str]:
    type_key, type_value = types
    key, value = next(iter(value.items()))

    errormessages = []
    errormessage_key = _validate(type_key, key, name)
    if errormessage_key is not None:
        errormessages.append(errormessage_key)
    errormessage_value = _validate(type_value, value, name)
    if errormessage_value is not None:
        errormessages.append(errormessage_value)

    if errormessages:
        return ' '.join(errormessages)

def _generic_alias(fieldtype, value, name: str) -> Optional[str]:
    basetype = fieldtype.__origin__

    if (errormessage := _basic(basetype, value, name)) is not None:
        return errormessage
    if basetype is tuple:
        return _tuple(fieldtype.__args__, value, name)
    elif basetype is list and value:
        return _validate(fieldtype.__args__[0], value[0], name)
    elif basetype is set and value:
        return _set(fieldtype.__args__[0], value, name)
    elif basetype is dict and value:
        return _dict(fieldtype.__args__, value, name)

def _union(types: tuple[type, ...], value, name: str) -> Optional[str]:
    errormessages = []
    for _type in types:
        errormessage = _validate(_type, value, name)
        if errormessage is None:
            return
        errormessages.append(errormessage)
    else:
        return ' '.join(errormessages)

def _iterable(value) -> Optional[str]:
    if not hasattr(value, '__iter__'):
        return f"'{type(value).__name__}' object is not iterable"

def _validate(fieldtype, value, name: str) -> Optional[str]:
    if fieldtype == Any:
        return
    if isinstance(fieldtype, _UnionGenericAlias):
        return _union(fieldtype.__args__, value, name)
    if fieldtype == Iterable:
        return _iterable(value)
    if isinstance(fieldtype, GenericAlias):
        return _generic_alias(fieldtype, value, name)
    if isinstance(fieldtype, type):
        return _basic(fieldtype, value, name)

def _validate_fields(obj) -> None:
    '''Checks types of the attributes of the class
    '''
    # TODO probably should be recursive
    errormessages = []
    for name, field_def in obj.__dataclass_fields__.items():
        errormessage = _validate(field_def.type,
                                 getattr(obj, name),
                                 name)
        if errormessage is not None:
            errormessages.append(errormessage)
    if errormessages:
        raise TypeError('\n'.join(errormessages))