#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .option_9 import option
from .value import value
class thermal_conductivity(Group):
    """
    'thermal_conductivity' child.
    """

    fluent_name = "thermal-conductivity"

    child_names = \
        ['option', 'value']

    option: option = option
    """
    option child of thermal_conductivity.
    """
    value: value = value
    """
    value child of thermal_conductivity.
    """
