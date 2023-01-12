#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .option_9 import option
from .user_defined_function import user_defined_function
class premix_heat_trans_coeff(Group):
    """
    'premix_heat_trans_coeff' child.
    """

    fluent_name = "premix-heat-trans-coeff"

    child_names = \
        ['option', 'user_defined_function']

    option: option = option
    """
    option child of premix_heat_trans_coeff.
    """
    user_defined_function: user_defined_function = user_defined_function
    """
    user_defined_function child of premix_heat_trans_coeff.
    """
