#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .number_of_coefficients import number_of_coefficients
from .coefficients import coefficients
class polynomial(Group):
    """
    'polynomial' child.
    """

    fluent_name = "polynomial"

    child_names = \
        ['number_of_coefficients', 'coefficients']

    number_of_coefficients: number_of_coefficients = number_of_coefficients
    """
    number_of_coefficients child of polynomial.
    """
    coefficients: coefficients = coefficients
    """
    coefficients child of polynomial.
    """
