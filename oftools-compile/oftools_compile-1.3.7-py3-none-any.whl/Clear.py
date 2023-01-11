#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""This module can be used for test purposes, to clear all generated files and check only of the 
compilation process is running fine.

  Typical usage example:

  clear = Clear()
  clear.run()
"""

# Generic/Built-in modules

# Third-party modules

# Owned modules
from .Context import Context
from .handlers.FileHandler import FileHandler


class Clear(object):
    """A class used to remove all generated files during compilation.

    Methods:
        __init__() -- Initializes the class with all the attributes.
        run() -- General run method to execute the clear option.
    """

    def __init__(self):
        """Initializes the class with all the attributes.
        """
        self._file_name_out = ''

    @property
    def file_name_out(self):
        """Getter method for the attribute _file_name_out.
        """
        return self._file_name_out

    def run(self, file_name_in):
        """General run method to execute the clear option.

        Removes the current working directory created during the given execution.

        Returns:
            integer -- Return code of the method.
        """
        self._file_name_out = file_name_in
        rc = FileHandler().delete_directory(Context().current_workdir)

        return rc
