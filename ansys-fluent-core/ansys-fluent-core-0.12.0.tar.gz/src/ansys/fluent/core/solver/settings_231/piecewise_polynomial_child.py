#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .minimum import minimum
from .maximum import maximum
from .number_of_coefficients import number_of_coefficients
from .coefficients import coefficients
class piecewise_polynomial_child(Group):
    """
    'child_object_type' of piecewise_polynomial.
    """

    fluent_name = "child-object-type"

    child_names = \
        ['minimum', 'maximum', 'number_of_coefficients', 'coefficients']

    minimum: minimum = minimum
    """
    minimum child of piecewise_polynomial_child.
    """
    maximum: maximum = maximum
    """
    maximum child of piecewise_polynomial_child.
    """
    number_of_coefficients: number_of_coefficients = number_of_coefficients
    """
    number_of_coefficients child of piecewise_polynomial_child.
    """
    coefficients: coefficients = coefficients
    """
    coefficients child of piecewise_polynomial_child.
    """
