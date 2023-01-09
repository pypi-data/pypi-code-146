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
from .biaxial import biaxial
from .cyl_orthotropic_1 import cyl_orthotropic
from .orthotropic_1 import orthotropic
from .principal_axes_values import principal_axes_values
from .anisotropic_1 import anisotropic
from .user_defined_function import user_defined_function
class thermal_conductivity(Group):
    """
    'thermal_conductivity' child.
    """

    fluent_name = "thermal-conductivity"

    child_names = \
        ['option', 'value', 'piecewise_linear', 'piecewise_polynomial',
         'polynomial', 'expression', 'biaxial', 'cyl_orthotropic',
         'orthotropic', 'principal_axes_values', 'anisotropic',
         'user_defined_function']

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
    biaxial: biaxial = biaxial
    """
    biaxial child of thermal_conductivity.
    """
    cyl_orthotropic: cyl_orthotropic = cyl_orthotropic
    """
    cyl_orthotropic child of thermal_conductivity.
    """
    orthotropic: orthotropic = orthotropic
    """
    orthotropic child of thermal_conductivity.
    """
    principal_axes_values: principal_axes_values = principal_axes_values
    """
    principal_axes_values child of thermal_conductivity.
    """
    anisotropic: anisotropic = anisotropic
    """
    anisotropic child of thermal_conductivity.
    """
    user_defined_function: user_defined_function = user_defined_function
    """
    user_defined_function child of thermal_conductivity.
    """
