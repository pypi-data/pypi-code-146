#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .option_9 import option
from .value import value
class critical_pressure(Group):
    """
    'critical_pressure' child.
    """

    fluent_name = "critical-pressure"

    child_names = \
        ['option', 'value']

    option: option = option
    """
    option child of critical_pressure.
    """
    value: value = value
    """
    value child of critical_pressure.
    """
