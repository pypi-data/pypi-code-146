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
class scattering_factor(Group):
    """
    'scattering_factor' child.
    """

    fluent_name = "scattering-factor"

    child_names = \
        ['option', 'value', 'user_defined_function']

    option: option = option
    """
    option child of scattering_factor.
    """
    value: value = value
    """
    value child of scattering_factor.
    """
    user_defined_function: user_defined_function = user_defined_function
    """
    user_defined_function child of scattering_factor.
    """
