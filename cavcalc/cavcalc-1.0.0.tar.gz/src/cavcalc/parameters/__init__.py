"""
A sub-package containing the Parameter classes, and some functions
for retrieving useful information from these.
"""

from .enums import ParameterType, ParameterCategory
from .parameter import ArgParameter, TargetParameter
from .tools import get_default_units, get_valid_arguments, get_valid_targets

# TODO (sjr) Get rid of below eventually, see note in .tools

valid_arguments = get_valid_arguments()
valid_targets = get_valid_targets()
