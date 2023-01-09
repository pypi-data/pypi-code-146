#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .option_9 import option
from .value import value
class averaging_coefficient_y(Group):
    """
    'averaging_coefficient_y' child.
    """

    fluent_name = "averaging-coefficient-y"

    child_names = \
        ['option', 'value']

    option: option = option
    """
    option child of averaging_coefficient_y.
    """
    value: value = value
    """
    value child of averaging_coefficient_y.
    """
