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
from .combustion_mixture import combustion_mixture
class premix_laminar_speed(Group):
    """
    'premix_laminar_speed' child.
    """

    fluent_name = "premix-laminar-speed"

    child_names = \
        ['option', 'value', 'user_defined_function', 'combustion_mixture']

    option: option = option
    """
    option child of premix_laminar_speed.
    """
    value: value = value
    """
    value child of premix_laminar_speed.
    """
    user_defined_function: user_defined_function = user_defined_function
    """
    user_defined_function child of premix_laminar_speed.
    """
    combustion_mixture: combustion_mixture = combustion_mixture
    """
    combustion_mixture child of premix_laminar_speed.
    """
