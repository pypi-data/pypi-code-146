#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Set of methods useful in any module.

This module gathers a set of methods that are useful in many other modules. When a method is widely 
used in different modules, a general version of it is created and can be found here.

Typical usage example:
  FileHandler().read_file(path)
"""

# Generic/Built-in modules
import configparser
import collections
import csv
import hashlib
import json
import os
import shutil
import sys
import xml

# Third-party modules
import untangle

# Owned modules
from ..Context import Context
from ..enums.ErrorEnum import ErrorMessage
from ..Log import Log


class SingletonMeta(type):
    """This pattern restricts the instantiation of a class to one object. 
    
    It is a type of creational pattern and involves only one class to create methods and specified objects. It provides a global point of access to the instance created.
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(SingletonMeta,
                                        cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class FileHandler(object, metaclass=SingletonMeta):
    """A class used to run file and directories related tasks across all modules.

    Attributes:
        _config_extensions {list[string]} -- List of supported extensions for configuration files.
        _text_extensions {list[string]} -- List of supported extensions for text files.

    Methods:
        read_file(path) -- Opens and reads a file.
        write_file(path, content, mode) -- Writes content to the file.
        copy_file(src, dst) -- Copies the source file to its given destination.
        delete_file(path) -- Deletes the file.
        check_extension(path, extension) -- Checks of the given file has the correct extension.

        create_directory(path) -- Creates the given directory if it does not already exists.
        move_directory (src, dst) -- Moves the source directory to its given destination.
        delete_directory(path) -- Deletes an entire directory tree, whether it is empty or not.
        is_a_directory(path) -- Evaluates if the given path is a directory or not.
        
        check_path_exists(path) -- Evaluates if the given path exists or not.
        check_write_access (path) -- Evaluates if the user has write access on the given path.
        get_files (path) -- Gets the list of files in a given path.
        get_duplicates(path, pattern) -- Gets duplicate files and folders in given path.
        get_creation_times(path) -- Gets modified timestamp of the input path(s).
    """

    def __init__(self):
        """Initialize class attributes.
        """
        self._config_extensions = ['cfg', 'conf', 'ini', 'prof', 'toml']
        self._text_extensions = ['log', 'tip', 'txt']

    # File related methods

    def read_file(self, path):
        """Opens and reads the file.

        It saves the file's content in a variable.

        Arguments:
            path {string} -- Absolute path of the file.

        Returns:
            Parsed file, the type depends on the extension of the processed file.

        Raises:
            SystemError -- Exception raised if the file is empty.
            IsADirectoryError -- Exception raised if a directory is specified instead of a file.
            FileNotFoundError -- Exception raised if the file does not exist or is not found.
            PermissionError -- Exception raised if the user does not have the required permissions to read the file.
            IndexError -- Exception raised if the file extension is not found.
            TypeError --  Exception raised if the file extension is not supported.
            OSError -- Exception raised if an error didn't already raised one of the previous exceptions.

            MissingSectionHeaderError -- Exception raised if there is no section in the config file specified.
            DuplicateSectionError -- Exception raised if there are two sections with the same name in the 
                config file specified.
            DuplicateOptionError -- Exception raised if there is a duplicate option in one of the sections 
                of the config file specified.
            
            JSONDecodeError -- Exception raised if there is an error decoding the JSON file specified.
            ValueError -- Exception raised if the first argument is None / empty string.
            AttributeError -- Exception raised if a requested xml.sax feature is not found in xml.sax.handler.
            xml.sax.SAXParseException -- Exception raised if something goes wrong during parsing.
        """
        try:
            path_expand = os.path.expandvars(path)

            if os.path.isfile(path_expand):
                # Check on file size
                if os.path.getsize(path_expand) <= 0:
                    raise SystemError()

                with open(path_expand, mode='r') as fd:
                    extension = path_expand.rsplit('.', 1)[1]

                    if extension in self._config_extensions:
                        file_data = configparser.ConfigParser(
                            dict_type=collections.OrderedDict)
                        file_data.optionxform = str
                        file_data.read(path_expand)
                    elif extension == 'csv':
                        out = csv.reader(fd, delimiter=',')
                        file_data = []
                        for row in out:
                            file_data.append(row)
                    elif extension == 'json':
                        file_data = json.load(fd)
                    elif extension in self._text_extensions:
                        file_data = fd.read()
                    elif extension == 'xml':
                        file_data = untangle.parse(path_expand)
                    else:
                        raise TypeError()
            elif os.path.isdir(path_expand):
                raise IsADirectoryError()
            else:
                raise FileNotFoundError()

        except IsADirectoryError:
            Log().logger.critical(ErrorMessage.IS_A_DIRECTORY.value % path)
            sys.exit(-1)
        except FileNotFoundError:
            Log().logger.critical(ErrorMessage.FILE_NOT_FOUND.value % path)
            sys.exit(-1)
        except SystemError:
            Log().logger.critical(ErrorMessage.SYSTEM_EMPTY.value % path)
            sys.exit(-1)
        except PermissionError:
            Log().logger.critical(ErrorMessage.PERMISSION.value % path)
            sys.exit(-1)
        except IndexError:
            Log().logger.critical(ErrorMessage.INDEX_EXTENSION.value % path)
            sys.exit(-1)
        except TypeError:
            Log().logger.critical(ErrorMessage.TYPE_EXTENSION.value % path)
            sys.exit(-1)
        except OSError as error:
            Log().logger.critical(ErrorMessage.OS_READ.value % error)
            sys.exit(-1)
        # configparser module related exceptions
        except configparser.MissingSectionHeaderError as error:
            Log().logger.critical(ErrorMessage.MISSING_SECTION_HEADER.value %
                                  error)
            sys.exit(-1)
        except configparser.DuplicateSectionError as error:
            Log().logger.critical(ErrorMessage.DUPLICATE_SECTION.value % error)
            sys.exit(-1)
        except configparser.DuplicateOptionError as error:
            Log().logger.critical(ErrorMessage.DUPLICATE_OPTION.value % error)
            sys.exit(-1)
        # json module related exceptions
        except json.JSONDecodeError as error:
            Log().logger.critical(ErrorMessage.JSON_DECODE.value % error)
            sys.exit(-1)
        # untangle related exceptions
        except ValueError as error:
            Log().logger.critical(ErrorMessage.VALUE.value % error)
            sys.exit(-1)
        except AttributeError as error:
            Log().logger.critical(ErrorMessage.ATTRIBUTE.value % error)
            sys.exit(-1)
        except xml.sax.SAXParseException as error:
            Log().logger.critical(ErrorMessage.XML_SAX_PARSE.value % error)
            sys.exit(-1)
        else:
            return file_data

    def write_file(self, path, content, mode='w'):
        """Writes content to the file.
        
        Arguments:
            path {string} -- Absolute path of the file.
            content {string or list[string]} -- Content that needs to be written to the file.
            mode {string} -- Mode used to write the file. Most common values: 'a' or 
            'w'.

        Returns:
            integer -- Return code of the method.
        
        Raises:
            IsADirectoryError -- Exception raised if a directory is specified instead of a file.
            PermissionError -- Exception raised if  the user does not have the required permissions to write to the file.
            IndexError -- Exception raised if the file extension is not found.
            TypeError -- Exception raised if the file extension is not supported.
        """
        try:
            path_expand = os.path.expandvars(path)

            if os.path.isdir(path_expand) is False:

                with open(path_expand, mode) as fd:
                    extension = path_expand.rsplit('.', 1)[1]

                    if extension in self._config_extensions:
                        content.write(fd)
                    elif extension == 'csv':
                        writer = csv.writer(fd, delimiter=',')
                        if isinstance(content, list):
                            writer.writerow(content)
                        elif isinstance(content[0], list):
                            writer.writerows(content)
                    elif extension == 'json':
                        json.dump(content, fd)
                    elif extension in self._text_extensions:
                        if isinstance(content, str):
                            fd.write(content)
                        elif isinstance(content, list):
                            for line in content:
                                fd.write(line)
                    else:
                        raise TypeError()
                rc = 0
            else:
                raise IsADirectoryError()

        except IsADirectoryError:
            Log().logger.critical(ErrorMessage.IS_A_DIRECTORY.value % path)
            rc = -1
        except PermissionError:
            Log().logger.critical(ErrorMessage.PERMISSION.value % path)
            rc = -1
        except IndexError:
            Log().logger.critical(ErrorMessage.INDEX_EXTENSION.value % path)
            rc = -1
        except TypeError:
            Log().logger.critical(ErrorMessage.TYPE_EXTENSION.value % path)
            rc = -1

        return rc

    @staticmethod
    def copy_file(src, dst):
        """Copies the source file to its given destination.

        Arguments:
            src {string} -- Absolute path of the source file.
            dst {string} -- Absolute path of the destination file.

        Returns:
            integer -- Return code of the method.
        
        Raises:
            shutil.SameFileError -- Exception raised if the file already exist.
            OSError -- Exception raised if an error didn't already raised one of the previous exceptions.
        """
        try:
            src_expand = os.path.expandvars(src)
            dst_expand = os.path.expandvars(dst)

            shutil.copy(src_expand, dst_expand)
            Log().logger.debug('Successful copy of ' + src + ' to ' + dst)
            rc = 0
        except shutil.SameFileError:
            Log().logger.debug(ErrorMessage.SHUTIL_SAME_FILE.value % (src, dst))
            rc = 1
        except OSError as error:
            Log().logger.critical(ErrorMessage.OS_COPY.value % error)
            rc = -1

        return rc

    @staticmethod
    def delete_file(path):
        """Deletes the file.

        Arguments:
            path {string} -- Absolute path of the file.

        Returns:
            integer -- Return code of the method.
        
        Raises:
            IsADirectoryError -- Exception raised if the given path is a directory and not a file.
            FileNotFoundError -- Exception raised if the file does not exist or is not found.
        """
        try:
            os.remove(path)
            rc = 0
        except IsADirectoryError:
            Log().logger.debug(ErrorMessage.IS_A_DIRECTORY.value % path)
            sys.exit(-1)
        except FileNotFoundError:
            Log().logger.debug(ErrorMessage.FILE_NOT_FOUND.value % path)
            sys.exit(-1)
        else:
            return rc

    @staticmethod
    def check_extension(path, extension):
        """Checks if the file has the correct extension.

        Arguments:
            path {string} -- Absolute path of the file.
            extension {string} -- File extension that needs to match.

        Returns:
            boolean -- True if the file extension is correct and False otherwise.
        
        Raises:
            IndexError -- Exception raised if the given file has an incorrect extension.
            TypeError -- Exception raised if the extension does not match.
        """
        try:
            path_expand = os.path.expandvars(path)
            ext = path_expand.rsplit('.', 1)[1]

            if ext == extension:
                is_valid_ext = True
            else:
                raise TypeError()
        except IndexError:
            Log().logger.critical(ErrorMessage.INDEX_EXTENSION.value %
                                  (extension, path))
            Log().logger.critical(ErrorMessage.ABORT.value)
            sys.exit(-1)
        except TypeError:
            Log().logger.error(ErrorMessage.TYPE_EXTENSION.value %
                               (ext, path_expand))
            is_valid_ext = False

        return is_valid_ext

    # Directory related methods

    @staticmethod
    def create_directory(path, path_type='default'):
        """Creates the given directory if it does not already exists.

        Arguments:
            path {string} -- Absolute path of the directory.
            path_type {string} -- Type of directory being created.

        Returns:
            integer -- Return code of the method.
        
        Raises:
            FileExistsError -- Exception raised if the directory already exists.
            OSError -- Exception raised if an error didn't already raised one of the previous exceptions.
        """
        try:
            path_expand = os.path.expandvars(path)

            # Check if the directory already exists
            if os.path.isdir(path_expand) is False:
                Log().logger.debug(
                    'Directory does not exist: Creating new directory: ' + path)
                os.mkdir(path_expand)

                Log().logger.debug('Directory successfully created: ' + path)
                rc = 0
            else:
                raise FileExistsError()
        except FileExistsError:
            if path_type == 'group':
                Log().logger.error(ErrorMessage.FILE_EXISTS.value % path)
            # else:
            #     Log().logger.debug(ErrorMessage.FILE_EXISTS.value % path)
            rc = 1
        except OSError as error:
            Log().logger.critical(ErrorMessage.OS_DIRECTORY_CREATION.value %
                                  error)
            sys.exit(-1)

        return rc

    @staticmethod
    def move_directory(src, dst):
        """Moves the source directory to its given destination.

        Arguments:
            src {string} -- Absolute path of the source directory.
            dst {string} -- Absolute path of the destination directory.

        Returns:
            integer -- Return code of the method.

        Raises:
            FileNotFoundError -- Exception raised if the directory does not exist or is not found.
        """
        try:
            shutil.move(src, dst)
            rc = 0
        except FileNotFoundError:
            Log().logger.warning(ErrorMessage.FILE_NOT_FOUND.value % src)
            Log().logger.warning('Skipping directory')
            sys.exit(-1)
        except shutil.Error as error:
            Log().logger.warning('Error: ' + str(error) +
                                 '. Skipping directory move command')
            sys.exit(-1)
        else:
            return rc

    @staticmethod
    def delete_directory(path):
        """Deletes an entire directory tree, whether it is empty or not.

        Arguments:
            path {string} -- Absolute path of the directory.

        Returns:
            integer -- Return code of the method.

        Raises:
            FileNotFoundError -- Exception raised if the directory does not exist or is not found.
            NotADirectoryError -- Exception raised if the path is not a directory.
            PermissionError -- Exception raised if the user does not have the required permissions to delete the directory.
            OSError -- Exception raised if an error didn't already raised one of the previous exceptions.
        """
        try:
            path_expand = os.path.expandvars(path)

            if os.path.exists(path_expand):
                if os.path.isdir(path_expand):

                    # Check if directory is empty
                    if len(os.listdir(path_expand)) == 0:
                        Log().logger.debug('Directory empty: ' + path)
                        os.rmdir(path_expand)
                    else:
                        # Check on directory size
                        size = sum(
                            os.path.getsize(element)
                            for element in os.scandir(path_expand)
                            if element.is_file(follow_symlinks=True))
                        if size == 0:
                            Log().logger.debug(
                                'Size of directory equal to 0: ' + path)

                        shutil.rmtree(path_expand, ignore_errors=False)

                    Log().logger.debug('Directory successfully removed: ' +
                                       path)
                    rc = 0
                else:
                    raise NotADirectoryError()
            else:
                raise FileNotFoundError()

        except FileNotFoundError:
            Log().logger.critical(ErrorMessage.FILE_NOT_FOUND.value % path)
            sys.exit(-1)
        except NotADirectoryError:
            Log().logger.critical(ErrorMessage.NOT_A_DIRECTORY.value % path)
            sys.exit(-1)
        except PermissionError:
            Log().logger.critical(ErrorMessage.PERMISSION.value % path)
            sys.exit(-1)
        except OSError as error:
            Log().logger.critical(ErrorMessage.OS_DELETE.value % error)
            sys.exit(-1)
        else:
            return rc

    @staticmethod
    def is_a_directory(path):
        """Evaluates if the given path is a directory or not.
        
        Arguments:
            path {string} -- Absolute path of the directory.

        Returns:
            boolean -- True if the path is a directory, False otherwise.

        Raises:
            NotADirectoryError -- Exception raised if the path is not a directory.
        """
        try:
            path_expand = os.path.expandvars(path)

            if os.path.isdir(path_expand):
                is_a_directory = True
            else:
                raise NotADirectoryError()
        except NotADirectoryError:
            Log().logger.critical(ErrorMessage.NOT_A_DIRECTORY.value % path)
            is_a_directory = False

        return is_a_directory

    # Other

    @staticmethod
    def check_path_exists(path):
        """Evaluates if the given path exists or not.
        
        Arguments:
            path {string} -- Absolute path of the file or directory.

        Returns:
            boolean -- True of the path exists, False otherwise.

        Raises:
            FileNotFoundError -- Exception raised if the path does not exist or is not found.
        """
        try:
            path_expand = os.path.expandvars(path)

            if os.path.exists(path_expand):
                path_exists = True
            else:
                raise FileNotFoundError()
        except FileNotFoundError:
            if Context().skip:
                Log().logger.info(ErrorMessage.FILE_NOT_FOUND.value % path)
                path_exists = False
            else:
                Log().logger.critical(ErrorMessage.FILE_NOT_FOUND.value % path)
                sys.exit(-1)

        return path_exists

    @staticmethod
    def check_write_access(path):
        """Evaluates if the user has write access on the given path.

        Arguments:
            path {string} -- Absolute path of the file or directory.

        Returns:
            boolean -- True if the user has write access on the path, False otherwise.

        Raises:
            PermissionError -- Exception raised if the user does not have the 
            required permissions to write the file.
        """
        try:
            path_expand = os.path.expandvars(path)

            if os.access(path_expand, os.W_OK):
                write_access = True
            else:
                raise PermissionError()
        except PermissionError:
            Log().logger.critical(ErrorMessage.PERMISSION_WRITE.value % path)
            write_access = False

        return write_access

    @staticmethod
    def get_files(path):
        """Gets the list of files in the path.

        Arguments:
            path {string} -- Absolute path of the file or directory.

        Returns:
            list[string] -- List of file absolute paths.

        Raises:
            FileNotFoundError -- Exception raised if the path does not exist or is not found.
        """
        try:
            path_expand = os.path.expandvars(path)

            if os.path.isfile(path_expand):
                file_paths = [os.path.abspath(path_expand)]

            elif os.path.isdir(path_expand):
                file_paths = [
                    os.path.abspath(os.path.join(root, filename))
                    for root, _, files in os.walk(path_expand)
                    for filename in files
                    if not filename.startswith('.')
                ]
                # Sort the list alphabetically
                file_paths.sort()
            else:
                raise FileNotFoundError()
        except FileNotFoundError:
            Log().logger.critical(ErrorMessage.FILE_NOT_FOUND.value % path)
            sys.exit(-1)

        return file_paths

    @staticmethod
    def get_duplicates(path, pattern):
        """Gets duplicate files and folders in the path.

        Arguments:
            path {string} -- Absolute path of the directory.
            pattern {string} -- Pattern to identify duplicates.

        Returns:
            tuple -- Tuple with two lists of strings, one for duplicate directories and one for duplicate files.
        
        Raises:
            FileNotFoundError -- Exception raised if the path does not exist or is not found.
            NotADirectoryError -- Exception raised if the path is not a directory.
            PermissionError -- Exception raised if the user does not have the required permissions to access the path.
            OSError -- Exception raised if an error didn't already raised one of the previous exceptions.
        """
        duplicate_directories = []
        # duplicate_files = []

        try:
            path_expand = os.path.expandvars(path)

            if os.path.exists(path_expand):
                if os.path.isdir(path_expand):
                    for root, dir_names, _ in os.walk(path_expand):
                        for dir_name in dir_names:
                            if pattern in dir_name:
                                duplicate = os.path.join(root, dir_name)
                                duplicate_directories.append(duplicate)
                        # for file_name in file_names:
                        #     if pattern in file_name:
                        #         duplicate = os.path.join(root, file_name)
                        #         duplicate_files.append(duplicate)
                else:
                    raise NotADirectoryError()
            else:
                raise FileNotFoundError()

        except FileNotFoundError:
            Log().logger.error(ErrorMessage.FILE_NOT_FOUND.value % path)
            sys.exit(-1)
        except NotADirectoryError:
            Log().logger.error(ErrorMessage.NOT_A_DIRECTORY.value % path)
            sys.exit(-1)
        except PermissionError:
            Log().logger.error(ErrorMessage.PERMISSION.value % path)
            sys.exit(-1)
        except OSError as error:
            Log().logger.error(ErrorMessage.OS_DUPLICATE.value % error)
            sys.exit(-1)
        else:
            return duplicate_directories

    @staticmethod
    def get_modified_times(path):
        """Gets modified timestamp of the input path(s).

        Arguments:
            path {string or list[string]} - One or several absolute path(s) to files or directories.

        Returns:
            float or list[float] -- Creation time(s) of the input path(s).

        Raises:
            FileNotFoundError -- Exception raised if the path does not exist or is not found.
            PermissionError -- Exception raised if the user does not have the required permissions to access the path.
            OSError -- Exception raised if an error didn't already raised one of the previous exceptions.
        """
        try:
            if isinstance(path, str):
                path_expand = os.path.expandvars(path)
                creation_times = .0
                if os.path.exists(path_expand):
                    creation_times = os.path.getmtime(path_expand)
                else:
                    raise FileNotFoundError()
            elif isinstance(path, list):
                paths = path
                creation_times = []

                for element in paths:
                    path_expand = os.path.expandvars(element)
                    if os.path.exists(path_expand):
                        creation_time = os.path.getmtime(element)
                        creation_times.append(creation_time)
                    else:
                        raise FileNotFoundError()

        except FileNotFoundError:
            Log().logger.error(ErrorMessage.FILE_NOT_FOUND.value % path)
            sys.exit(-1)
        except PermissionError:
            Log().logger.critical(ErrorMessage.PERMISSION.value % path)
            sys.exit(-1)
        except OSError as error:
            Log().logger.critical(ErrorMessage.OS_CREATION_TIMES.value % error)
            sys.exit(-1)
        else:
            return creation_times
