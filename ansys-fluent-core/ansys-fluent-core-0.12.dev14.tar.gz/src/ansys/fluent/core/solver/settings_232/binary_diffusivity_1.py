#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .option_9 import option
from .value import value
from .film_averaged import film_averaged
from .piecewise_linear import piecewise_linear
from .piecewise_polynomial import piecewise_polynomial
from .polynomial import polynomial
from .user_defined_function import user_defined_function
class binary_diffusivity(Group):
    """
    'binary_diffusivity' child.
    """

    fluent_name = "binary-diffusivity"

    child_names = \
        ['option', 'value', 'film_averaged', 'piecewise_linear',
         'piecewise_polynomial', 'polynomial', 'user_defined_function']

    option: option = option
    """
    option child of binary_diffusivity.
    """
    value: value = value
    """
    value child of binary_diffusivity.
    """
    film_averaged: film_averaged = film_averaged
    """
    film_averaged child of binary_diffusivity.
    """
    piecewise_linear: piecewise_linear = piecewise_linear
    """
    piecewise_linear child of binary_diffusivity.
    """
    piecewise_polynomial: piecewise_polynomial = piecewise_polynomial
    """
    piecewise_polynomial child of binary_diffusivity.
    """
    polynomial: polynomial = polynomial
    """
    polynomial child of binary_diffusivity.
    """
    user_defined_function: user_defined_function = user_defined_function
    """
    user_defined_function child of binary_diffusivity.
    """
