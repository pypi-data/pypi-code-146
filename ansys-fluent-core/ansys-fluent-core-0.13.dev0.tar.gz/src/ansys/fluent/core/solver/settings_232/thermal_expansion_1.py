#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .option_9 import option
from .value import value
class thermal_expansion_1(Group):
    """
    'thermal_expansion_1' child.
    """

    fluent_name = "thermal-expansion-1"

    child_names = \
        ['option', 'value']

    option: option = option
    """
    option child of thermal_expansion_1.
    """
    value: value = value
    """
    value child of thermal_expansion_1.
    """
