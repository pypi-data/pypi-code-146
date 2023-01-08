#!/usr/bin/env python3
"""utility to move/delete duplicate files of the same size and context in specified folder.

command string parameters:
first parameter:    full_path_to_folder - folder where duplicates are searched.
second parameter:   optional - folder for storage duplicate files """

import argparse
import logging
import pathlib
import sys
import remove_duplicates.my_utils as my_utils


def _win32_behavior(pth: str) -> str:
    """Костыль для платформы win32. Если в функцию передан путь который не является ни файлом и не папкой,
    то возвращается путь к родительскому каталогу"""
    path = pathlib.Path(pth)
    if not path.is_file() and not path.is_dir():
        return str(path.parent.resolve())
    return str(path.resolve())


def recursive_process_folder(start_folder: str, trash_folder: str, file_name_pattern: list):
    """
    :param start_folder: Search for duplicate files starts from this folder.
    :param trash_folder: found copies of files are transferred to this folder.
    :param file_name_pattern: Only files matching the pattern are processed.
    :return: count file copies deleted/moved.
    """
    ret_val = 0
    try:
        ret_val = my_utils.delete_duplicate_file(start_folder, file_name_pattern, trash_folder, logging)
    except PermissionError as ex:
        logging.warning(f"Folder {start_folder}. OS Error code: {ex.errno}. Error message: {ex.strerror}!")
    else:
        logging.info(f"Folder {start_folder} processed. Found {ret_val} copies!")

    # enumerating
    pth = pathlib.Path(start_folder)
    for child in pth.iterdir():
        try:
            if child.is_dir():
                ret_val += recursive_process_folder(str(child.resolve()), trash_folder, file_name_pattern)
        except PermissionError:
            folder_name = str(child.resolve())
            logging.warning(f"Access is denied! Folder: {folder_name}")
    # return value
    return ret_val


def main() -> int:
    """return: count file copies deleted/moved!
    If error return my_utils.INVALID_VALUE."""
    str_storage_folder, str_search_folder, log_file_name = None, None, None     # default values

    if "win32" == sys.platform:
        # На платформе win32 аргумент sys.argv[0] содержит не имя выполняемого файла,
        # а имя несуществующего файла python скрипта!
        # Проверял под python 3.10 в Win10. В Debian 11 все в порядке.
        str_search_folder = _win32_behavior(sys.argv[0])
    else:  # other platform
        str_search_folder = my_utils.get_folder_name_from_path(sys.argv[0])

    parser = argparse.ArgumentParser(description="""Utility to recursive search and move/delete duplicate files 
                                                of the same size and context in specified folder.""",
                                     epilog="""If the storage folder is not specified, 
                                                then duplicate files will be deleted!
                                                If the number of command line parameters is zero, 
                                                then the search folder = current folder.""")

    parser.add_argument("--start_folder", type=str, help="The folder with which the recursive search begins.")
    parser.add_argument("--recycle_bin", type=str, help="Folder for storing duplicate files.")
    parser.add_argument("--log_file", type=str, help="Log file name.")
    parser.add_argument("--fn_pattern", type=str,
                        help="File name pattern. Only files matching the pattern are processed! "
                             "Provides support for Unix shell-style wildcards.", default="*.*")

    args = parser.parse_args()

    fn_pattern = ""
    if args.fn_pattern:
        fn_pattern = args.fn_pattern.replace(" ", "")  # удаляю все пробелы из строки
        fn_pattern = fn_pattern.split(",")  # создаю список

    if args.log_file:
        log_file_name = args.log_file
    # setup logger start
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)

    # Если пользователь не задал имя файла-журнала, поэтому журналом становится sys.stdout
    handler = logging.StreamHandler(sys.stdout)
    if log_file_name:
        handler = logging.FileHandler(log_file_name, "w", "utf-8")

    formatter = logging.Formatter("%(asctime)s: %(levelname)s: %(message)s")
    handler.setFormatter(formatter)  # Pass handler as a parameter, not assign
    root_logger.addHandler(handler)
    # setup logger end

    if args.start_folder:
        str_search_folder = args.start_folder
        if not my_utils.is_folder_exist(str_search_folder):
            logging.critical(f"Invalid path to search folder: {str_search_folder}. Exit!")
            return my_utils.INVALID_VALUE

    if args.recycle_bin:
        str_storage_folder = args.recycle_bin
        if not my_utils.is_folder_exist(args.recycle_bin):
            logging.critical(f"Invalid path to storage folder: {args.recycle_bin}. Exit!")
            return my_utils.INVALID_VALUE

    # START
    logging.info(f"Search for duplicate files in the folder: {str_search_folder}")
    logging.info(f"Pattern file name: {fn_pattern}")
    if log_file_name:
        logging.info(f"Log file name: {log_file_name}")
    if str_storage_folder:
        logging.info(f"Storage folder: {str_storage_folder}")

    ret_val = recursive_process_folder(str_search_folder, str_storage_folder, fn_pattern)

    action = "deleted"
    if args.recycle_bin:
        action = "moved"

    logging.info(f"Total found {ret_val} copies of files.")

    if ret_val:
        logging.info(f"{ret_val} copies of files have been {action}.")

    return ret_val


if __name__ == "__main__":
    sys.exit(main())
