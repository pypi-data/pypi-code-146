#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .option_9 import option
from .value import value
from .piecewise_linear import piecewise_linear
from .piecewise_polynomial import piecewise_polynomial
from .polynomial import polynomial
from .nasa_9_piecewise_polynomial import nasa_9_piecewise_polynomial
from .user_defined_function import user_defined_function
class specific_heat(Group):
    """
    'specific_heat' child.
    """

    fluent_name = "specific-heat"

    child_names = \
        ['option', 'value', 'piecewise_linear', 'piecewise_polynomial',
         'polynomial', 'nasa_9_piecewise_polynomial',
         'user_defined_function']

    option: option = option
    """
    option child of specific_heat.
    """
    value: value = value
    """
    value child of specific_heat.
    """
    piecewise_linear: piecewise_linear = piecewise_linear
    """
    piecewise_linear child of specific_heat.
    """
    piecewise_polynomial: piecewise_polynomial = piecewise_polynomial
    """
    piecewise_polynomial child of specific_heat.
    """
    polynomial: polynomial = polynomial
    """
    polynomial child of specific_heat.
    """
    nasa_9_piecewise_polynomial: nasa_9_piecewise_polynomial = nasa_9_piecewise_polynomial
    """
    nasa_9_piecewise_polynomial child of specific_heat.
    """
    user_defined_function: user_defined_function = user_defined_function
    """
    user_defined_function child of specific_heat.
    """
