from enum import EnumMeta
from typing import Any, Collection, Mapping


def subscripted_type(generic_alias: Any) -> type:
    """
    convert an instance of a subscripted ``typing._GenericAlias`` to a subscripted type

    :param generic_alias: generic alias
    :return: simple type

    >>> from typing import List
    >>> subscripted_type(List[str])
    [str]

    >>> from typing import Dict
    >>> subscripted_type(Dict[str, float])
    {str: float}

    >>> from typing import Dict, Tuple
    >>> subscripted_type({str: (Dict[int, str], str)})
    {str: ({int: str}, str)}

    """

    if hasattr(generic_alias, '__origin__') \
            and ((hasattr(generic_alias.__origin__, '_name') and generic_alias.__origin__._name == 'Union') \
                 or (hasattr(generic_alias.__origin__, '__name__') and generic_alias.__origin__.__name__ == 'Union')):
        raise NotImplementedError('Union subscription is not supported')

    if (
            hasattr(generic_alias, "__origin__")
            or isinstance(generic_alias, Collection)
            and not isinstance(generic_alias, (EnumMeta, str))
    ):
        if hasattr(generic_alias, "__origin__"):
            type_class = generic_alias.__origin__
            if hasattr(generic_alias, "__args__"):
                members = generic_alias.__args__
                if issubclass(type_class, Mapping):
                    members = [members]
            else:
                members = ()
        elif isinstance(generic_alias, Collection) and not isinstance(
                generic_alias, (EnumMeta, str)
        ):
            type_class = generic_alias.__class__
            members = generic_alias.items() if issubclass(type_class, Mapping) else generic_alias

        members = [subscripted_type(member) for member in members]
        if type_class != generic_alias.__class__ or members != generic_alias:
            return type_class(members)
        return generic_alias
    return generic_alias
