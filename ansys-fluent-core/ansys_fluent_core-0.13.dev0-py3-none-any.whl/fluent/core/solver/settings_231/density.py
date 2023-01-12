#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .option_9 import option
from .real_gas_nist import real_gas_nist
from .value import value
from .compressible_liquid import compressible_liquid
from .piecewise_linear import piecewise_linear
from .piecewise_polynomial import piecewise_polynomial
from .polynomial import polynomial
from .expression import expression
from .user_defined_function import user_defined_function
from .rgp_table import rgp_table
class density(Group):
    """
    'density' child.
    """

    fluent_name = "density"

    child_names = \
        ['option', 'real_gas_nist', 'value', 'compressible_liquid',
         'piecewise_linear', 'piecewise_polynomial', 'polynomial',
         'expression', 'user_defined_function', 'rgp_table']

    option: option = option
    """
    option child of density.
    """
    real_gas_nist: real_gas_nist = real_gas_nist
    """
    real_gas_nist child of density.
    """
    value: value = value
    """
    value child of density.
    """
    compressible_liquid: compressible_liquid = compressible_liquid
    """
    compressible_liquid child of density.
    """
    piecewise_linear: piecewise_linear = piecewise_linear
    """
    piecewise_linear child of density.
    """
    piecewise_polynomial: piecewise_polynomial = piecewise_polynomial
    """
    piecewise_polynomial child of density.
    """
    polynomial: polynomial = polynomial
    """
    polynomial child of density.
    """
    expression: expression = expression
    """
    expression child of density.
    """
    user_defined_function: user_defined_function = user_defined_function
    """
    user_defined_function child of density.
    """
    rgp_table: rgp_table = rgp_table
    """
    rgp_table child of density.
    """
