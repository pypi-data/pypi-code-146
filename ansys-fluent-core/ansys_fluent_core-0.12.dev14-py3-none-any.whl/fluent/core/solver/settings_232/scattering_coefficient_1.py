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
from .gray_band_coefficients import gray_band_coefficients
from .user_defined_function import user_defined_function
class scattering_coefficient(Group):
    """
    'scattering_coefficient' child.
    """

    fluent_name = "scattering-coefficient"

    child_names = \
        ['option', 'value', 'piecewise_linear', 'piecewise_polynomial',
         'polynomial', 'expression', 'gray_band_coefficients',
         'user_defined_function']

    option: option = option
    """
    option child of scattering_coefficient.
    """
    value: value = value
    """
    value child of scattering_coefficient.
    """
    piecewise_linear: piecewise_linear = piecewise_linear
    """
    piecewise_linear child of scattering_coefficient.
    """
    piecewise_polynomial: piecewise_polynomial = piecewise_polynomial
    """
    piecewise_polynomial child of scattering_coefficient.
    """
    polynomial: polynomial = polynomial
    """
    polynomial child of scattering_coefficient.
    """
    expression: expression = expression
    """
    expression child of scattering_coefficient.
    """
    gray_band_coefficients: gray_band_coefficients = gray_band_coefficients
    """
    gray_band_coefficients child of scattering_coefficient.
    """
    user_defined_function: user_defined_function = user_defined_function
    """
    user_defined_function child of scattering_coefficient.
    """
