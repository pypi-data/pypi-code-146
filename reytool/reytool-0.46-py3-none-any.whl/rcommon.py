# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time    : 2022-12-08 13:11:09
@Author  : Rey
@Contact : reyxbo@163.com
@Explain : Rey's common methods
"""


from typing import Any, List, Tuple, Dict, Iterable, Literal, Optional, Union
import os
import time
import random
from pandas import DataFrame, Series
from traceback import format_exc

from .rbasic import error, is_iterable, check_least_one, convert_type
from .rtext import rprint
from .rtime import now


def exc(title: str = "Error", to_print: bool = True) -> str:
    """
    Print and return error messages, must used in 'except' syntax.

    Parameters
    ----------
    title : Print title.

    to_print : Whether print error messages.

    Returns
    -------
    Error messages.
    """

    error = format_exc()
    error = error.strip()
    if to_print:
        rprint(error, title=title, frame="half")
    return error

def flatten(data: Any, flattern_data: List = []) -> List:
    """
    Flatten data.
    """

    data_type = type(data)
    if data_type == dict:
        for element in data.values():
            _ = flatten(element, flattern_data)
    elif is_iterable(data):
        for element in data:
            _ = flatten(element, flattern_data)
    else:
        flattern_data.append(data)
    return flattern_data

def log(records: Union[List[Iterable], List[Dict], DataFrame, Series], fields: Optional[Iterable] = None, path: str = "log.csv") -> None:
    """
    Write or create log file.
    """
    

    if not len(records):
        return
    records_type = type(records)
    exists_bool = os.path.exists(path)
    if not exists_bool:
        start_id = 0
        if fields:
            fields = ["id", "datetime"] + fields
        else:
            fields = ["id", "datetime"]
            if records_type == list:
                element_type = type(records[0])
                if element_type == dict:
                    fields.extend(records[0].keys())
                else:
                    fields.extend([""] * len(records[0]))
            elif records_type == DataFrame:
                fields.extend(records.columns)
            elif records_type == Series:
                name = records.name
                name = str(name) if name else ""
                fields.append(name)
        fields_text = ",".join(fields)
    else:
        with open(path, "r", encoding="utf-8") as f:
            log_texts = f.readlines()
        start_id = int(log_texts[-1].split(",")[0]) + 1
        fields_text = ""
    records_len = len(records)
    records_ids = range(start_id, start_id + records_len)
    datetime_now = now()
    if records_type == list:
        element_type = type(records[0])
        if element_type == dict:
            records = [row.values() for row in records]
        values_texts = [
            ",".join(
                [
                    str(id),
                    datetime_now,
                    *[str(element) for element in row]
                ]
            )
            for id, row in list(zip(records_ids, records))
        ]
        values_text = "\n".join(values_texts)
    elif records_type == DataFrame:
        records = records.fillna("")
        records.insert(0, "id", records_ids, allow_duplicates=True)
        records.insert(1, "datetime", datetime_now, allow_duplicates=True)
        records = records.astype(str)
        func = lambda ser: ser.str.cat(sep=",")
        values_ser = records.apply(func=func, axis=1)
        values_text = values_ser.str.cat(sep="\n")
    elif records_type == Series:
        records = records.fillna("")
        records = DataFrame(records)
        records.insert(0, "id", records_ids, allow_duplicates=True)
        records.insert(1, "datetime", datetime_now, allow_duplicates=True)
        records = records.astype(str)
        func = lambda ser: ser.str.cat(sep=",")
        values_ser = records.apply(func=func, axis=1)
        values_text = values_ser.str.cat(sep="\n")
    records_text = "\n".join([fields_text, values_text])
    with open(path, "a", encoding="utf-8") as f:
        f.write(records_text)

def digits(number: Union[int, float]) -> Tuple:
    """
    Judge the number of integer digits and deciaml digits.

    Parameters
    ----------
    number : Judge number.

    Returns
    -------
    Integer digits and deciaml digits.
    """

    number_str = str(number)
    if "." in number_str:
        integer_str, decimal_str = number_str.split(".")
        integer_digits = len(integer_str)
        deciaml_digits = len(decimal_str)
    else:
        integer_digits = len(number_str)
        deciaml_digits = 0
    return integer_digits, deciaml_digits

def randn(*thresholds: Union[int, float], precision: Optional[int] = None) -> Union[int, float]:
    """
    Get random number.

    Parameters
    ----------
    *thresholds : Low and high thresholds of random range, range contains thresholds.
        - When length is 0, then low and high thresholds is 0 and 10.
        - When length is 1, then low and high thresholds is 0 and thresholds[0].
        - When length is 2, then low and high thresholds is thresholds[0] and thresholds[1].

    precision : Precision of random range, that is maximum decimal digits of return value.
        - None : Set to Maximum decimal digits of element of parameter *thresholds.
        - int : Set to this value.
    
    Returns
    -------
    Random number.
        - When parameters precision is 0, then return int.
        - When parameters precision is greater than 0, then return float.
    """
    
    thresholds_len = len(thresholds)
    if thresholds_len == 0:
        threshold_low = 0
        threshold_high = 10
    elif thresholds_len == 1:
        threshold_low = 0
        threshold_high = thresholds[0]
    elif thresholds_len == 2:
        threshold_low = thresholds[0]
        threshold_high = thresholds[1]
    else:
        error("number of parameter '*thresholds' must is 0 or 1 or 2", ValueError)
    if precision == None:
        threshold_low_desimal_digits = digits(threshold_low)[1]
        threshold_high_desimal_digits = digits(threshold_high)[1]
        desimal_digits_max = max(threshold_low_desimal_digits, threshold_high_desimal_digits)
        precision = desimal_digits_max
    magnifier = 10 ** precision
    threshold_low *= magnifier
    threshold_high *= magnifier
    number = random.randint(threshold_low, threshold_high)
    number = number / magnifier
    if precision == 0:
        number = int(number)
    return number

def sleep(*thresholds: Union[int, float], precision: Optional[int] = None) -> Union[int, float]:
    """
    Sleep random seconds.

    Parameters
    ----------
    *thresholds : Low and high thresholds of random range, range contains thresholds.
        - When length is 0, then low and high thresholds is 0 and 10.
        - When length is 1, then sleep this value.
        - When length is 2, then low and high thresholds is thresholds[0] and thresholds[1].
    
    precision : Precision of random range, that is maximum decimal digits of sleep seconds.
        - None : Set to Maximum decimal digits of element of parameter *thresholds.
        - int : Set to this value.
    
    Returns
    -------
    Random seconds.
        - When parameters precision is 0, then return int.
        - When parameters precision is greater than 0, then return float.
    """

    thresholds_len = len(thresholds)
    if thresholds_len == 0:
        second = randn(0, 10, precision=precision)
    elif thresholds_len == 1:
        second = thresholds[0]
    elif thresholds_len == 2:
        second = randn(thresholds[0], thresholds[1], precision=precision)
    else:
        error("number of parameter '*thresholds' must is 0 or 1 or 2", ValueError)
    time.sleep(second)
    return second

def split_array(array: Iterable, bin_size: Optional[int] = None, share: int = 10) -> List:
    """
    Split array into multiple array.
    """

    check_least_one(bin_size, share)

    array = list(array)
    array_len = len(array)
    arrays = []
    arrays_len = 0
    if bin_size == None:
        average = array_len / share
        for n in range(share):
            bin_size = int(average * (n + 1)) - int(average * n)
            _array = array[arrays_len:arrays_len + bin_size]
            arrays.append(_array)
            arrays_len += bin_size
    else:
        while True:
            _array = array[arrays_len:arrays_len + bin_size]
            arrays.append(_array)
            arrays_len += bin_size
            if arrays_len > array_len:
                break
    return arrays

def get_paths(path: Optional[str] = None, target: Literal["all", "file", "folder"] = "all", recursion: bool = True) -> List:
    """
    Get the path of files and folders in the path.

    Parameters
    ----------
    path : When None, then work path.

    target : Target data.
        - "all" : Return file and folder path.
        - "file : Return file path.
        - "folder" : Return folder path.

    recursion : Is recursion directory.

    Returns
    -------
    String is path.
    """

    if path == None:
        path = ""
    path = os.path.abspath(path)
    paths = []
    if recursion:
        obj_walk = os.walk(path)
        if target == "all":
            targets_path = [
                os.path.join(path, file_name)
                for path, folders_name, files_name in obj_walk
                for file_name in files_name + folders_name
            ]
            paths.extend(targets_path)
        elif target == "file":
            targets_path = [
                os.path.join(path, file_name)
                for path, folders_name, files_name in obj_walk
                for file_name in files_name
            ]
            paths.extend(targets_path)
        elif target in ["all", "folder"]:
            targets_path = [
                os.path.join(path, folder_name)
                for path, folders_name, files_name in obj_walk
                for folder_name in folders_name
            ]
            paths.extend(targets_path)
    else:
        names = os.listdir(path)
        if target == "all":
            for name in names:
                target_path = os.path.join(path, name)
                paths.append(target_path)
        elif target == "file":
            for name in names:
                target_path = os.path.join(path, name)
                is_file = os.path.isfile(target_path)
                if is_file:
                    paths.append(target_path)
        elif target == "folder":
            for name in names:
                target_path = os.path.join(path, name)
                is_dir = os.path.isdir(target_path)
                if is_dir:
                    paths.append(target_path)
    return paths