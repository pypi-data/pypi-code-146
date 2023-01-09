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
from .user_defined_function import user_defined_function
class planar_conductivity(Group):
    """
    'planar_conductivity' child.
    """

    fluent_name = "planar-conductivity"

    child_names = \
        ['option', 'value', 'piecewise_linear', 'piecewise_polynomial',
         'polynomial', 'user_defined_function']

    option: option = option
    """
    option child of planar_conductivity.
    """
    value: value = value
    """
    value child of planar_conductivity.
    """
    piecewise_linear: piecewise_linear = piecewise_linear
    """
    piecewise_linear child of planar_conductivity.
    """
    piecewise_polynomial: piecewise_polynomial = piecewise_polynomial
    """
    piecewise_polynomial child of planar_conductivity.
    """
    polynomial: polynomial = polynomial
    """
    polynomial child of planar_conductivity.
    """
    user_defined_function: user_defined_function = user_defined_function
    """
    user_defined_function child of planar_conductivity.
    """
