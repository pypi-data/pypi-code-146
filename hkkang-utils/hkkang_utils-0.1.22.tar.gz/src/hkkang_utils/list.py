import operator
import functools


from typing import List, Any
def do_flatten_list(list_of_list: List[List[Any]])-> List[Any]:
    """Flatten a list of list to a list

    :param list_of_list: list to flatten
    :type list_of_list: List[List[Any]]
    :return: flatten list
    :rtype: List[Any]
    """
    return functools.reduce(operator.iconcat, list_of_list, [])