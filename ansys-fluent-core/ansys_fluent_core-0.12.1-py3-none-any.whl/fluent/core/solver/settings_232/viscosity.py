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
from .blottner_curve_fit import blottner_curve_fit
from .sutherland import sutherland
from .cross import cross
from .herschel_bulkley import herschel_bulkley
from .carreau import carreau
from .non_newtonian_power_law import non_newtonian_power_law
from .user_defined_function import user_defined_function
from .rgp_table import rgp_table
from .real_gas_nist import real_gas_nist
class viscosity(Group):
    """
    'viscosity' child.
    """

    fluent_name = "viscosity"

    child_names = \
        ['option', 'value', 'piecewise_linear', 'piecewise_polynomial',
         'polynomial', 'expression', 'power_law', 'blottner_curve_fit',
         'sutherland', 'cross', 'herschel_bulkley', 'carreau',
         'non_newtonian_power_law', 'user_defined_function', 'rgp_table',
         'real_gas_nist']

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
    blottner_curve_fit: blottner_curve_fit = blottner_curve_fit
    """
    blottner_curve_fit child of viscosity.
    """
    sutherland: sutherland = sutherland
    """
    sutherland child of viscosity.
    """
    cross: cross = cross
    """
    cross child of viscosity.
    """
    herschel_bulkley: herschel_bulkley = herschel_bulkley
    """
    herschel_bulkley child of viscosity.
    """
    carreau: carreau = carreau
    """
    carreau child of viscosity.
    """
    non_newtonian_power_law: non_newtonian_power_law = non_newtonian_power_law
    """
    non_newtonian_power_law child of viscosity.
    """
    user_defined_function: user_defined_function = user_defined_function
    """
    user_defined_function child of viscosity.
    """
    rgp_table: rgp_table = rgp_table
    """
    rgp_table child of viscosity.
    """
    real_gas_nist: real_gas_nist = real_gas_nist
    """
    real_gas_nist child of viscosity.
    """
