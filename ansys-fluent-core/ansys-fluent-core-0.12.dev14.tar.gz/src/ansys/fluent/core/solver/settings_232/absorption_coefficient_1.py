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
from .path_length import path_length
from .gray_band_coefficients import gray_band_coefficients
from .user_defined_function import user_defined_function
class absorption_coefficient(Group):
    """
    'absorption_coefficient' child.
    """

    fluent_name = "absorption-coefficient"

    child_names = \
        ['option', 'value', 'piecewise_linear', 'piecewise_polynomial',
         'polynomial', 'expression', 'path_length', 'gray_band_coefficients',
         'user_defined_function']

    option: option = option
    """
    option child of absorption_coefficient.
    """
    value: value = value
    """
    value child of absorption_coefficient.
    """
    piecewise_linear: piecewise_linear = piecewise_linear
    """
    piecewise_linear child of absorption_coefficient.
    """
    piecewise_polynomial: piecewise_polynomial = piecewise_polynomial
    """
    piecewise_polynomial child of absorption_coefficient.
    """
    polynomial: polynomial = polynomial
    """
    polynomial child of absorption_coefficient.
    """
    expression: expression = expression
    """
    expression child of absorption_coefficient.
    """
    path_length: path_length = path_length
    """
    path_length child of absorption_coefficient.
    """
    gray_band_coefficients: gray_band_coefficients = gray_band_coefficients
    """
    gray_band_coefficients child of absorption_coefficient.
    """
    user_defined_function: user_defined_function = user_defined_function
    """
    user_defined_function child of absorption_coefficient.
    """
