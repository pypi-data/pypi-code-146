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
from .power_law import power_law
from .sutherland import sutherland
from .user_defined_function import user_defined_function
from .real_gas_nist_mixture import real_gas_nist_mixture
class viscosity(Group):
    """
    'viscosity' child.
    """

    fluent_name = "viscosity"

    child_names = \
        ['option', 'value', 'piecewise_linear', 'piecewise_polynomial',
         'polynomial', 'expression', 'power_law', 'sutherland',
         'user_defined_function', 'real_gas_nist_mixture']

    option: option = option
    """
    option child of viscosity.
    """
    value: value = value
    """
    value child of viscosity.
    """
    piecewise_linear: piecewise_linear = piecewise_linear
    """
    piecewise_linear child of viscosity.
    """
    piecewise_polynomial: piecewise_polynomial = piecewise_polynomial
    """
    piecewise_polynomial child of viscosity.
    """
    polynomial: polynomial = polynomial
    """
    polynomial child of viscosity.
    """
    expression: expression = expression
    """
    expression child of viscosity.
    """
    power_law: power_law = power_law
    """
    power_law child of viscosity.
    """
    sutherland: sutherland = sutherland
    """
    sutherland child of viscosity.
    """
    user_defined_function: user_defined_function = user_defined_function
    """
    user_defined_function child of viscosity.
    """
    real_gas_nist_mixture: real_gas_nist_mixture = real_gas_nist_mixture
    """
    real_gas_nist_mixture child of viscosity.
    """
