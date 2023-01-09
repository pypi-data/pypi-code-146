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
class charge_density(Group):
    """
    'charge_density' child.
    """

    fluent_name = "charge-density"

    child_names = \
        ['option', 'value', 'user_defined_function']

    option: option = option
    """
    option child of charge_density.
    """
    value: value = value
    """
    value child of charge_density.
    """
    user_defined_function: user_defined_function = user_defined_function
    """
    user_defined_function child of charge_density.
    """
