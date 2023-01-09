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
from .expression import expression
from .user_defined_function import user_defined_function
class saturation_pressure(Group):
    """
    'saturation_pressure' child.
    """

    fluent_name = "saturation-pressure"

    child_names = \
        ['option', 'value', 'piecewise_linear', 'piecewise_polynomial',
         'polynomial', 'expression', 'user_defined_function']

    option: option = option
    """
    option child of saturation_pressure.
    """
    value: value = value
    """
    value child of saturation_pressure.
    """
    piecewise_linear: piecewise_linear = piecewise_linear
    """
    piecewise_linear child of saturation_pressure.
    """
    piecewise_polynomial: piecewise_polynomial = piecewise_polynomial
    """
    piecewise_polynomial child of saturation_pressure.
    """
    polynomial: polynomial = polynomial
    """
    polynomial child of saturation_pressure.
    """
    expression: expression = expression
    """
    expression child of saturation_pressure.
    """
    user_defined_function: user_defined_function = user_defined_function
    """
    user_defined_function child of saturation_pressure.
    """
