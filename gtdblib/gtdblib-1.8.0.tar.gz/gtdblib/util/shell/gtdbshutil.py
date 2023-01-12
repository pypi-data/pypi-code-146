"""Utility functions for copying and archiving files and directory trees."""

import errno
import os
import sys
import tempfile
import mmap

from gtdblib import log


def get_num_lines(file_path):
    """ Calculate the number of lines in a file.

    :param file_path: path to file

    :return: number of lines in file
    """

    fp = open(file_path, "r+")
    buf = mmap.mmap(fp.fileno(), 0)
    lines = 0
    while buf.readline():
        lines += 1

    return lines


def symlink(target: str, link_name: str, overwrite: bool = False):
    '''Create a symbolic link named link_name pointing to target.

    If link_name exists then FileExistsError is raised, unless ``overwrite=True``.
    When trying to overwrite a directory, IsADirectoryError is raised.

    :param target: The target of the link.
    :param link_name: The name of the link.
    :param overwrite: If True, overwrite existing files and directories.

    :raises FileExistsError: If link_name exists and overwrite=False.

    :return: True
    '''

    if not overwrite:
        os.symlink(target, link_name)
        return

    # os.replace() may fail if files are on different filesystems
    link_dir = os.path.dirname(link_name)

    # Create link to target with temporary filename
    while True:
        temp_link_name = tempfile.mktemp(dir=link_dir)

        # os.* functions mimic as closely as possible system functions
        # The POSIX symlink() returns EEXIST if link_name already exists
        # https://pubs.opengroup.org/onlinepubs/9699919799/functions/symlink.html
        try:
            os.symlink(target, temp_link_name)
            break
        except FileExistsError:
            pass

    return True


def check_file_exists(input_file):
    """Check if file exists.This function is copied from `biolib <https://github.com/dparks1134/biolib>`_ on the 09/10/2020.

    :param input_file: path to file

    :return: True if path exists
    """

    if not os.path.exists(input_file) or not os.path.isfile(input_file):
        log.error('Input file does not exists: ' + input_file + '\n')
        sys.exit()

    return True


def check_dir_exists(input_dir):
    """Check if directory exists.This function is copied from `biolib <https://github.com/dparks1134/biolib>`_ on the 09/10/2020.

    :param input_dir: path to directory

    :return: True if path exists
    """

    if not os.path.exists(input_dir) or not os.path.isdir(input_dir):
        log.error('Input directory does not exists: ' + input_dir + '\n')
        sys.exit()

    return True


def make_sure_path_exists(path):
    """Create directory if it does not exist. This function is copied from `biolib <https://github.com/dparks1134/biolib>`_ on the 09/10/2020.

    :param path: path to directory

    :return: True if directory exists or was created
    """

    if not path:
        # lack of a path qualifier is acceptable as this
        # simply specifies the current directory
        return

    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            log.error('Specified path could not be created: ' + path + '\n')
            sys.exit()

    return True
