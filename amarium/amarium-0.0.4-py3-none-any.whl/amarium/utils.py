"""
Collection of utitly functions for file I/O operations. The purpose is
especially for scientific computing, thus numpy is involved in some functions.
Copyright (C) 2022 Julian M. Kleber This program comes with ABSOLUTELY NO
WARRANTY; for details type 'show w'. This is free software, and you are welcome
to redistribute it under certain conditions; type 'show c' for details.".

author: Julian M. Kleber
"""

import os
import json
import time
import logging
from typing import Tuple, List, Dict, Any, Optional, Union, Type

import numpy as np
import numpy.typing as npt

LOGGER = logging.getLogger(__name__)


timestr = time.strftime("%Y%m%d-%H%M%S")


def prepare_file_name_saving(prefix: str, file_name: str, suffix: str) -> str:
    """The prepare_file_name_saving function takes a prefix and file name as
    input. It checks to see if the directory exists, and makes it if not. Then
    it returns the full path of the file.

    :param prefix:str: Used to Specify the folder where the file will be saved.
    :param file_name:str: Used to Specify the name of the file to be saved.
    :return: The full path of the file name.

    :doc-author: Trelent
    """
    check_make_dir(prefix)
    file_name = make_full_filename(prefix, file_name)
    file_name = check_file_name(file_name, suffix)
    return file_name


def insert_string_in_file_name(file_name: str, insertion: str, suffix: str) -> str:
    """
    The insert_string_in_file_name function takes a file_name and inserts a string into the name.
        The insertion is placed before the extension of the file_name, or if there is no extension,
        it will be placed at the end of the file_name with an suffix specified by you.


    :param file_name:str: Used to Specify the file name that you want to insert a string into.
    :param insertion:str: Used to Specify the string that will be inserted into the file name.
    :param suffix:str: Used to Specify the file suffix.
    :return: A string.

    :doc-author: Julian M. Kleber
    """

    root, ext = os.path.splitext(file_name)

    if suffix is None and not ext:
        raise ValueError(
            "You must either specify an suffix in the file_name or pass an suffix through the \
            suffix argument. For example the file_name could be 'foo.bar' or you pass \
            file_name'foo' with suffix = '.bar'"
        )
    if suffix is not None:
        if not suffix.startswith("."):
            suffix = "." + suffix

    if not ext:
        file_name = file_name + "_" + insertion + suffix
    else:
        file_name = root + "_" + insertion + ext
    return file_name


def check_file_name(file_name: str, suffix: str) -> str:
    """The check_name_plot function checks that the file_name ends with .png.
    If it does not, then check_name_plot appends .png to the end of the
    file_name.

    :param file_name: Used to Specify the name of the file to be plotted.
    :return: The file_name with the correct file extension.

    :doc-author: Trelent
    """
    name = file_name
    ext = os.path.splitext(file_name)[1]
    if not ext:
        if not suffix.startswith("."):
            suffix = "." + suffix
        name += suffix
    return name


def make_full_filename(prefix: str, file_name: str) -> str:
    """
    The make_full_filename function takes a prefix and a file_name as input.
    If the prefix is None, then the file_name is returned unchanged.
    Otherwise, if the file name starts with 'http://' or 'ftp://', then it's assumed to be an URL
    and the full_filename will contain both the prefix and file_name; otherwise,
    only return full_filename = file_name.

    :param prefix: Used to Add a prefix to the file_name.
    :param file_name: Used to Create a full file_name for the file to be downloaded.
    :return: The full file_name with the prefix added to the beginning of the file_name.

    :doc-author: Trelent
    """
    if prefix is None:
        return file_name
    if prefix.endswith("/") and file_name.startswith("/"):
        file_name = prefix + file_name[1:]
    elif prefix.endswith("/") or file_name.startswith("/"):
        file_name = prefix + file_name
    else:
        file_name = prefix + "/" + file_name
    return file_name


def check_make_dir(dir_name: str) -> None:
    """The check_make_dir function checks if a directory exists. If it does not
    exist, the function creates it.

    :param dir_name:str: Used to Specify the folder name.
    :return: None.

    :doc-author: Trelent
    """

    # You should change 'test' to your preferred folder.
    check_folder = os.path.isdir(dir_name)
    logging.info("Checked the directory %s", dir_name)
    # If folder doesn't exist, then create it.
    if not check_folder:
        os.makedirs(dir_name)
        logging.info("Created folder : %s", dir_name)

    else:
        logging.info("%s folder already exists.", dir_name)


def load_json_from_file(file_name: str) -> Dict[Any, Any]:
    """
    The load_json_from_file function takes a file name as input and returns the contents of that
    file in JSON format.

    :param file_name:str: Used to Specify the file name of the json file to be loaded.
    :return: A dictionary of the data in the file.

    :doc-author: Julian M. Kleber
    """

    with open(file_name, "r", encoding="utf-8") as json_file:
        data = dict(json.load(json_file))
    return data


def save_json_to_file(
    dictionary: Dict[Any, Any], file_name: Optional[str] = None, suffix: str = ".json"
) -> None:
    """The save_json function saves a dictionary to a json file.

    :param dictionary: Used to store the data that will be saved.
    :param file_name:str=None: Used to specify a file name.
    :return: A string with the name of the file that was just created.

    :doc-author: Julian M. Kleber
    """

    def convert(np_data: Union[npt.NDArray[Any], Type[np.generic]]) -> Any:
        """The convert function takes in a numpy object and returns the value
        of that object. If the input is an array, it will return a list of
        values. If it is not an array, it will return just the value.

        :param o:Union[Type(np.ndarray): Used to Specify the type of object that will be passed to
        the function.
        :param Type(np.generic)]: Used to Specify the type of object that is being passed into
        the function.
        :return: The value of the input object.

        :doc-author: Trelent
        """

        val = None
        if isinstance(np_data, np.generic):
            val = np_data.item()
        elif isinstance(np_data, np.ndarray):
            val = list(np_data)
        return val

    if file_name is None:

        file_name = make_date_file_name(suffix=suffix)
    with open(file_name, "w", encoding="utf-8") as out_file:
        json.dump(dictionary, out_file, default=convert)
        logging.info("Saved json %s", file_name)


def make_date_file_name(prefix: str = "", file_name: str = "", suffix: str = "") -> str:
    """The make_date_file_name function creates a file name with the date and
    time stamp in the format YYYY-MM-DD_HH:MM:SS.out.  The prefix, file_name,
    and suffix are optional arguments that can be used to specify what string
    should precede the date stamp in the file_name (prefix), what string should
    be appended after the date stamp (suffix), or both (file_name).   If no
    arguments are provided, then make_date_file_name will use default values
    for all three arguments.

    :param prefix:str="": Used to ddd a prefix to the file name.
    :param file_name:str="": Used to specify the name of the file.
    :param suffix:str=".out": Used to specify the file extension.
    :return: A string that is the combination of prefix, file_name and suffix.

    :doc-author: Julian M. Kleber
    """
    time_str = time.strftime("%Y%m%d-%H%M%S" + prefix + file_name + suffix)
    return time_str


def delete_file(file_name: str) -> None:
    """
    The delete_file function deletes a file from the local directory.

        Raises:
            Exception if there is an error deleting the specified file.
            This function will not catch any exceptions, so it should be
            called within a try/except block.

    :param file_name:str: Used to Specify the name of the file that will be deleted.
    :return: None.

    :doc-author: Julian M. Kleber
    """

    try:
        os.remove(file_name)
        logging.info("Deleted file %s", file_name)
    except Exception as exc:
        raise exc


def get_grid_positions(rows: int, cols: int) -> List[Tuple[int, int]]:
    """
    The get_grid_positions function takes in the number of rows and columns in a grid,
    and returns a list of tuples containing all possible positions on that grid.

    :param rows:int: Used to specify the number of rows in the grid.
    :param cols:int: Used to specify the number of columns in the grid.
    :return: A list of tuples.

    :doc-author: Julian M. Kleber
    """

    grid = []
    for i in range(2, rows):
        for j in range(cols):
            grid.append((int(i), int(j)))
    return grid


def search_subdirs(dir_name: str) -> Tuple[List[str], List[str]]:
    """The search_subdirs function takes a directory name as input and returns
    a tuple of two lists. The first list contains all the files in the
    directory, including those in subdirectories. The second list contains all
    the subdirectories.

    :param dir_name:str: Used to Specify the directory that we want to search.
    :return: A tuple of two lists.

    :doc-author: Julian M. Kleber
    """
    if not dir_name.endswith("/"):
        dir_name += "/"

    result_files = []
    sub_dirs = []
    for path, subdirs, files in os.walk(dir_name):
        for name in files:
            result_files.append(os.path.join(path, name))
        for subdir in subdirs:
            sub_dirs.append(os.path.join(path, subdir))

    return (result_files, sub_dirs)
