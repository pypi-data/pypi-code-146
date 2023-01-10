import inspect
import json
from typing import Any
from typing import Dict
from typing import List


"""
ATTENTION: Functions in this util file are highly controversial and we don't encourage use any of these functions.
1. These functions give developers a misconception that they are suitable for comparing certain data structure.
In reality, they are not. They all have limitations and only work on certain scope of data structures. Data structure
such as List and Dict can contain nested data structures and these functions will certainly not do the job well on
nested data structure.
2. There are mature modules if we have to compare two complex data structure, for example, dict_tool, deepdiff.
The functions here are re-inventing the wheel.

Hence, think about twice before you decide to use any of the following functions. There should be no new util function
added to this file and the existing functions should be deprecated at some point.
"""


def are_lists_identical(hub, list1: List, list2: List) -> bool:
    """
    Compare two lists and logs the difference.
    :param list1: first list.
    :param list2: second list.
    :return: true if there is no difference between both lists.
    :raises exception if one of the list  is not of type list
    """
    if (list1 is None or len(list1) == 0) and (list2 is None or len(list2) == 0):
        return True
    if list1 is None or len(list1) == 0 or list2 is None or len(list2) == 0:
        return False

    for l in [list1, list2]:
        if not isinstance(l, List):
            raise TypeError(
                f"Expecting lists to compare. This is expected to be of type List: '{l}'"
            )

    diff = [i for i in list1 + list2 if i not in list1 or i not in list2]
    result = len(diff) == 0
    if not result:
        hub.log.debug(f"There are {len(diff)} differences:\n{diff[:5]}")
    return result


def standardise_json(hub, value: str or Dict, sort_keys: bool = True) -> str:
    # Format json string or dictionary
    if value is None or value is inspect._empty or not value:
        return None

    if isinstance(value, str) and len(value) > 0:
        json_dict = json.loads(value)
    elif isinstance(value, Dict):
        json_dict = value
    else:
        raise TypeError(
            f"Expecting string or dictionary. This value has the wrong type: '{value}'"
        )

    return json.dumps(
        _sorting(json_dict) if sort_keys else json_dict,
        separators=(", ", ": "),
        sort_keys=sort_keys,
    )


def is_json_identical(hub, struct1: str, struct2: str):
    return _sorting(json.loads(struct1)) == _sorting(json.loads(struct2))


def _sorting(obj):
    if isinstance(obj, dict):
        return {k: _sorting(v) for k, v in sorted(obj.items())}
    if isinstance(obj, list):
        if all(isinstance(v, str) for v in obj):
            return sorted(obj)
        else:
            return [_sorting(v) for i, v in sorted(enumerate(obj))]
    return obj


def compare_dicts(hub, source_dict: Dict[str, Any], target_dict: Dict[str, Any]):
    """
    This functions helps in comparing two dicts.
    It compares each key value in both the dicts and return true or false based on the comparison

    Returns:
        {True|False}

    """
    if source_dict is None and target_dict is None:
        return True

    if source_dict is None or target_dict is None:
        return False

    for key, value in source_dict.items():
        if key in target_dict:
            if isinstance(source_dict[key], dict):
                if not compare_dicts(hub, source_dict[key], target_dict[key]):
                    return False
            elif value != target_dict[key]:
                return False
        else:
            return False
    return True
