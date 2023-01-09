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
from .rgp_table import rgp_table
from .real_gas_nist import real_gas_nist
class thermal_conductivity(Group):
    """
    'thermal_conductivity' child.
    """

    fluent_name = "thermal-conductivity"

    child_names = \
        ['option', 'value', 'piecewise_linear', 'piecewise_polynomial',
         'polynomial', 'expression', 'user_defined_function', 'rgp_table',
         'real_gas_nist']

    option: option = option
    """
    option child of thermal_conductivity.
    """
    value: value = value
    """
    value child of thermal_conductivity.
    """
    piecewise_linear: piecewise_linear = piecewise_linear
    """
    piecewise_linear child of thermal_conductivity.
    """
    piecewise_polynomial: piecewise_polynomial = piecewise_polynomial
    """
    piecewise_polynomial child of thermal_conductivity.
    """
    polynomial: polynomial = polynomial
    """
    polynomial child of thermal_conductivity.
    """
    expression: expression = expression
    """
    expression child of thermal_conductivity.
    """
    user_defined_function: user_defined_function = user_defined_function
    """
    user_defined_function child of thermal_conductivity.
    """
    rgp_table: rgp_table = rgp_table
    """
    rgp_table child of thermal_conductivity.
    """
    real_gas_nist: real_gas_nist = real_gas_nist
    """
    real_gas_nist child of thermal_conductivity.
    """
