"""mfire.utils module

This module manages the processing of common modules

"""

from mfire.utils.dict_utils import FormatDict, recursive_format, dict_diff
from mfire.utils.json_diff import json_diff
from mfire.utils.json_utils import JsonFile
from mfire.utils.hash import MD5
from mfire.utils.parallel import Parallel, current_process

__all__ = [
    "FormatDict",
    "recursive_format",
    "JsonFile",
    "MD5",
    "dict_diff",
    "json_diff",
    "Parallel",
    "current_process",
]
