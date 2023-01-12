#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .option_9 import option
from .user_defined_function import user_defined_function
from .value import value
class specific_heat(Group):
    """
    'specific_heat' child.
    """

    fluent_name = "specific-heat"

    child_names = \
        ['option', 'user_defined_function', 'value']

    option: option = option
    """
    option child of specific_heat.
    """
    user_defined_function: user_defined_function = user_defined_function
    """
    user_defined_function child of specific_heat.
    """
    value: value = value
    """
    value child of specific_heat.
    """
