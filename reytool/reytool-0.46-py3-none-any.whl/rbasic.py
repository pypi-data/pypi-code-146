# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time    : 2022-12-05 14:09:42
@Author  : Rey
@Contact : reyxbo@163.com
@Explain : Rey"s basic methods
"""


from typing import Any, List, Tuple, Iterable, Callable, NoReturn, Type, Literal, Optional, Union
from warnings import warn as warnings_warn
from varname import argname


def error(error_info: Optional[Any] = None, error_type: Type[BaseException] = AssertionError) -> NoReturn:
    """
    Throw error.

    Parameters
    ----------
    error_info : Error information.
    
    error_type : Error type.
    """
    
    if error_info == None:
        raise error_type
    raise error_type(error_info)

def warn(*warn_infos: Any, warn_type: Type[BaseException] = UserWarning, stacklevel: int = 3) -> None:
    """
    Throw warning.

    Parameters
    ----------
    *warn_info : Warn informations.

    warn_type : Warn type.

    stacklevel : Warning code location, number of recursions up the code level.
    """
    
    
    if warn_infos == ():
        warn_infos = "Warning!"
    elif len(warn_infos) == 1:
        warn_info_type = type(warn_infos[0])
        if warn_info_type == str:
            warn_infos = warn_infos[0]
        else:
            warn_infos = str(warn_infos[0])
    else:
        warn_infos = str(warn_infos)
    warnings_warn(warn_infos, warn_type, stacklevel)

def check_parm(value: Any, *targets: Union[Any, Literal["_iterable"]], check_element: bool = False) -> None:
    """
    Check the content or type of the value, when check fail, then throw error.

    Parametes
    ---------
    value : Check object.

    *targets : Correct target, can be type.
        - Any : Check whether it is the target.
        - Literal['_iterable'] : Check whether it can be iterable.

    check_element : Whether check element in value.
    """

    if check_element:
        values = value
    else:
        values = [value]
    for element in values:
        if "_iterable" in targets and is_iterable(element):
            continue
        if type(element) in targets:
            continue
        targets_id = [id(target) for target in targets]
        if id(element) in targets_id:
            continue
        var_name = get_name(value)
        if var_name != None:
            var_name = " '%s'" % var_name
        else:
            var_name = ""
        correct_targets_str = ", ".join([repr(target) for target in targets])
        if check_element:
            error_text = "parameter%s the elements content or type must in [%s], now: %s" % (var_name, correct_targets_str, repr(value))
        else:
            error_text = "parameter%s the content or type must in [%s], now: %s" % (var_name, correct_targets_str, repr(value))
        error(error_text, ValueError)

def check_least_one(*values: Any) -> None:
    """
    Check that at least one of multiple values is not None, when check fail, then throw error.

    Parameters
    ----------
    *values : Check values.
    """

    for value in values:
        if value != None:
            return
    vars_name = get_name(values)
    if vars_name != None:
        vars_name = de_duplicate(vars_name)
        vars_name_str = " " + " and ".join(["\"%s\"" % var_name for var_name in vars_name])
    else:
        vars_name_str = ""
    error_text = "at least one of parameters%s is not None" % vars_name_str
    error(error_text, ValueError)

def check_only_one(*values: Any) -> None:
    """
    Check that at most one of multiple values is not None, when check fail, then throw error.

    Parameters
    ----------
    *values : Check values.
    """

    none_count = 0
    for value in values:
        if value != None:
            none_count += 1
    if none_count > 1:
        vars_name = get_name(values)
        if vars_name != None:
            vars_name = de_duplicate(vars_name)
            vars_name_str = " " + " and ".join(["\"%s\"" % var_name for var_name in vars_name])
        else:
            vars_name_str = ""
        error_text = "at most one of parameters%s is not None" % vars_name_str
        error(error_text, ValueError)

def is_iterable(obj: Any, exclude_type: Iterable = [str, bytes]) -> bool:
    """
    Judge whether it is iterable.

    Parameters
    ----------
    obj : Judge object.

    exclude_type : Exclusion type.

    Returns
    -------
    Judgment result.
    """

    obj_type = type(obj)
    if obj_type in exclude_type:
        return False
    try:
        obj_dir = obj.__dir__()
    except TypeError:
        return False
    if "__iter__" in obj_dir:
        return True
    else:
        return False

def is_number_str(text: str, return_value: bool = False) -> Union[bool, int, float]:
    """
    Judge whether it is number string.

    Parameters
    ----------
    text : Judge text.

    return_value : Whether return value.
    
    Returns
    -------
    Judgment result or transformed value.
    """

    try:
        if "." in text:
            number = float(text)
        else:
            number = int(text)
    except ValueError:
        return False
    if return_value:
        return number
    return True

def get_first_notnull(*values: Any, default: Optional[Union[Any, Literal["error"]]] = None, none_values: List = [None]) -> Any:
    """
    Get the first value that is not null.

    Parameters
    ----------
    *values : Check values.

    default : When all are None, then return this is value, or throw error.
        - Any : Return this is value.
        - Literal['error'] : Throw error.

    none_values : Range of None values.

    Returns
    -------
    When all are None, then return default value.
    """
    
    for value in values:
        if value not in none_values:
            return value
    if default == "error":
        vars_name = get_name(values)
        if vars_name != None:
            vars_name = de_duplicate(vars_name)
            vars_name_str = " " + " and ".join(["\"%s\"" % var_name for var_name in vars_name])
        else:
            vars_name_str = ""
        error_text = "at least one of parameters%s is not None" % vars_name_str
        error(error_text, ValueError)
    return default

def ins(obj: Any, *arrays: Iterable) -> bool:
    """
    Judge whether the object is in multiple array.

    Parameters
    ----------
    obj : Judge object.

    *arrays : Array.

    Returns
    -------
    Judge result.
    """

    for array in arrays:
        if obj in array:
            return True
    return False

def mutual_in(*arrays: Iterable) -> bool:
    """
    Whether the same element exists in multiple array.

    Parameters
    ----------
    *arrays : Array.

    Returns
    -------
    Judge result.
    """
    
    arrays = list(arrays)
    for n, array in enumerate(arrays):
        for after_array in arrays[n+1:]:
            for element in array:
                if ins(element, after_array):
                    return True
    return False

def convert_type(obj: Any, to_type: Type, method: Optional[Callable] = None) -> Any:
    """
    Convert object type.

    Parameters
    ----------
    obj : Convert object.

    to_type : Target type.

    method : Convert method.
        - Callable : Use this method.
        - None : Use value of parameter to_type.

    Returns
    -------
    Converted object.
    """

    if type(obj) == to_type:
        return obj
    if method != None:
        return method(obj)
    else:
        return to_type(obj)

def get_name(obj: Any, frame: int = 2) -> Optional[Union[str, Tuple[str, ...]]]:
    """
    Get object name.

    Parameters
    ----------
    obj : Object.

    frame : Number of code to upper level.

    Returns
    -------
    Object name or None.
    """

    try:
        name = obj.__name__
    except AttributeError:
        name = "obj"
        try:
            for _frame in range(1, frame + 1):
                name = argname(name, frame=_frame)
            if type(name) != str:
                if "".join(name) == "":
                    name = None
        except:
            name = None
    return name

def de_duplicate(array: Iterable) -> List:
    """
    De duplication of array.

    Parameters
    ----------
    array : Iterable object.

    Returns
    -------
    List after de duplication.
    """

    array = convert_type(array, list)
    de_duplicate_array = list(set(array))
    de_duplicate_array.sort(key=array.index)
    return de_duplicate_array