#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .option_9 import option
from .value import value
from .user_defined_function import user_defined_function
class tmelt(Group):
    """
    'tmelt' child.
    """

    fluent_name = "tmelt"

    child_names = \
        ['option', 'value', 'user_defined_function']

    option: option = option
    """
    option child of tmelt.
    """
    value: value = value
    """
    value child of tmelt.
    """
    user_defined_function: user_defined_function = user_defined_function
    """
    user_defined_function child of tmelt.
    """
