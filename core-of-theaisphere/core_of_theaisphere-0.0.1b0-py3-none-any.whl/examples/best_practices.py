"""
This script illustrates how to follow some best-practices for coding
"""

# Imports
from typing import List, Any
import logging
from colorlog import ColoredFormatter

LOG_LEVEL = logging.DEBUG
logging.root.setLevel(LOG_LEVEL)
formatter = ColoredFormatter('%(log_color)s[%(levelname).1s %(log_color)s%(asctime)s] - %(log_color)s%(name)s - '
                             '%(reset)s%(message)s')
stream = logging.StreamHandler()
stream.setLevel(LOG_LEVEL)
stream.setFormatter(formatter)
logger = logging.getLogger(__name__)
logger.setLevel(LOG_LEVEL)
logger.addHandler(stream)

"""
Author: vickyparmar
File: best_practices.py
Created on: 05-10-2022, Wed, 17:38:09

Last modified by: vickyparmar
Last modified on: 13-10-2022, Thu, 17:03:20
"""


# [ ] ToDo: Stuff to do


# Class ListBestPractices
class ListBestPractices:
    """
            Description of the class.

            Parameters
            ----------
            a: List
                Description of variable a.
            b: Any
                Description of variable b.

            Attributes
            ----------
            a: List
                Description of Attribute a.
            b: Any
                Description of Attribute b.

            Methods
            -------
            method1(param='abcd')
                Description of method 1.
            method2(param=xyz)
                Description of method 2.

            Raises
            ------
            type of Exception raised
                Description of raised exception.

            See Also
            -------
            othermodule : Other module to see.

            Notes
            -----
            Notes about your class

            .. deprecated:: version
              `ndobj_old` will be removed in NumPy 2.0

            Example
            -------
            >>> # provide an example on how to use this class
            """

    def __init__(self, a: List, b: Any):
        """
        Initializing the class instance
        Parameters
        ----------
        a: List
            Description of variable a
        b: Any
            Description of variable b
        """
        self.a = a
        self.b = b
        logger.info(f"A: {a}, B: {b}")
