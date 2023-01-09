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
class premix_laminar_thickness(Group):
    """
    'premix_laminar_thickness' child.
    """

    fluent_name = "premix-laminar-thickness"

    child_names = \
        ['option', 'value', 'user_defined_function']

    option: option = option
    """
    option child of premix_laminar_thickness.
    """
    value: value = value
    """
    value child of premix_laminar_thickness.
    """
    user_defined_function: user_defined_function = user_defined_function
    """
    user_defined_function child of premix_laminar_thickness.
    """
