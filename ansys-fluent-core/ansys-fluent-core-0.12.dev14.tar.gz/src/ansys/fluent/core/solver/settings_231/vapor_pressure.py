#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .option_9 import option
from .piecewise_linear import piecewise_linear
from .piecewise_polynomial import piecewise_polynomial
from .polynomial import polynomial
from .value import value
from .rgp_table import rgp_table
from .user_defined_function import user_defined_function
class vapor_pressure(Group):
    """
    'vapor_pressure' child.
    """

    fluent_name = "vapor-pressure"

    child_names = \
        ['option', 'piecewise_linear', 'piecewise_polynomial', 'polynomial',
         'value', 'rgp_table', 'user_defined_function']

    option: option = option
    """
    option child of vapor_pressure.
    """
    piecewise_linear: piecewise_linear = piecewise_linear
    """
    piecewise_linear child of vapor_pressure.
    """
    piecewise_polynomial: piecewise_polynomial = piecewise_polynomial
    """
    piecewise_polynomial child of vapor_pressure.
    """
    polynomial: polynomial = polynomial
    """
    polynomial child of vapor_pressure.
    """
    value: value = value
    """
    value child of vapor_pressure.
    """
    rgp_table: rgp_table = rgp_table
    """
    rgp_table child of vapor_pressure.
    """
    user_defined_function: user_defined_function = user_defined_function
    """
    user_defined_function child of vapor_pressure.
    """
