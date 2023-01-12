#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .option_9 import option
from .value import value
class therm_exp_coeff(Group):
    """
    'therm_exp_coeff' child.
    """

    fluent_name = "therm-exp-coeff"

    child_names = \
        ['option', 'value']

    option: option = option
    """
    option child of therm_exp_coeff.
    """
    value: value = value
    """
    value child of therm_exp_coeff.
    """
