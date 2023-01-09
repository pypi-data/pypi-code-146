#!/usr/bin/env python3
"""service utils"""

import hashlib
import pathlib
import datetime
import os
import calc_files_control_sum.my_strings as my_strings
import calc_files_control_sum.config as config


def get_hash_file(full_path_to_file: str, algorithm="md5", buff_size=4096) -> str:
    """return hash of file"""
    h = hashlib.new(algorithm)
    with open(full_path_to_file, "rb") as f:
        for chunk in iter(lambda: f.read(buff_size), b""):
            h.update(chunk)

    return h.hexdigest().upper()


def is_folder_exist(full_folder_path: str) -> bool:
    """check folder for exist and is folder
    return value is Boolean!"""
    folder = pathlib.Path(full_folder_path)
    return folder.is_dir() and folder.exists()


def is_file_exist(filename: str) -> bool:
    """check file for exist"""
    p = pathlib.Path(filename)
    return p.is_file()


def get_owner_folder_path(full_path_to_file: str) -> str:
    """ return owner folder path from full path file name """
    # mypath = pathlib.Path(full_path_to_file).absolute()
    mypath = pathlib.Path(full_path_to_file)
    return str(mypath.parent)


def get_file_name_from_path(full_path_to_file: str) -> str:
    """ return filename from full path file name """
    path = pathlib.Path(full_path_to_file)
    return path.name


def get_file_extension_from_path(full_path_to_file: str) -> str:
    """ return file extension from full path file name """
    path = pathlib.Path(full_path_to_file)
    return path.suffix


def split_path(full_path_to_file: str) -> tuple[str, str, str]:
    """Divides the file path into three parts: parent (owner folder name),
    name (file name), suffix(ext)"""
    path = pathlib.Path(full_path_to_file)
    return str(path.parent), path.name, path.suffix


class DeltaTime:
    """time interval measurement"""
    @staticmethod
    def get_time() -> datetime.datetime:
        """return time in second"""
        return datetime.datetime.now()

    def __init__(self):
        self._start = DeltaTime.get_time()
        self._stop = None

    def start(self):
        """call start before measurement"""
        self.__init__()

    def delta(self) -> float:
        """return delta time in second"""
        self._stop = DeltaTime.get_time()
        return self._stop.timestamp() - self._start.timestamp()

    @property
    def start_time(self) -> datetime.datetime:
        return self._start

    @property
    def stop_time(self) -> datetime.datetime:
        return self._stop


def settings_from_file(filename: str, check_crc: bool = True) -> dict:
    """Read all settings from file and convert it into dict"""
    res = None
    try:
        cr = config.ConfigReader(filename, check_crc=check_crc)
        res = dict(cr.read(my_strings.str_settings_header))
        if isinstance(res["ext"], str):
            # преобразование строки в список с расширениями!
            lst = res["ext"].replace("[", "").replace("]", "").split(sep=",")
            res["ext"] = lst
    except OSError as e:
        print(f"{my_strings.strOsError}: {e}")
    return res


def get_file_stat(filename: str) -> os.stat_result:
    """Return statistic of file. Pls. see: https://docs.python.org/3.9/library/os.html#os.stat_result"""
    path = pathlib.Path(filename)
    return path.stat()
