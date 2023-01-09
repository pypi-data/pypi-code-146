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
class premix_adiabatic_temp(Group):
    """
    'premix_adiabatic_temp' child.
    """

    fluent_name = "premix-adiabatic-temp"

    child_names = \
        ['option', 'value', 'user_defined_function']

    option: option = option
    """
    option child of premix_adiabatic_temp.
    """
    value: value = value
    """
    value child of premix_adiabatic_temp.
    """
    user_defined_function: user_defined_function = user_defined_function
    """
    user_defined_function child of premix_adiabatic_temp.
    """
