#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .file_suffix_type import file_suffix_type
from .file_decimal_digit import file_decimal_digit
class append_file_name_with(Group):
    """
    Set the suffix for auto-saved files. The file name can be appended by flow-time, time-step value or by user specified flags in file name.
    """

    fluent_name = "append-file-name-with"

    child_names = \
        ['file_suffix_type', 'file_decimal_digit']

    file_suffix_type: file_suffix_type = file_suffix_type
    """
    file_suffix_type child of append_file_name_with.
    """
    file_decimal_digit: file_decimal_digit = file_decimal_digit
    """
    file_decimal_digit child of append_file_name_with.
    """
