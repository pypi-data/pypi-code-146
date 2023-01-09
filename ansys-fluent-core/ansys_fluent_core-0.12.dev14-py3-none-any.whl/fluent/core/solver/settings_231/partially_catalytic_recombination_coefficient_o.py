#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .option_2 import option
from .value import value
from .profile_name import profile_name
from .field_name import field_name
from .udf import udf
class partially_catalytic_recombination_coefficient_o(Group):
    """
    'partially_catalytic_recombination_coefficient_o' child.
    """

    fluent_name = "partially-catalytic-recombination-coefficient-o"

    child_names = \
        ['option', 'value', 'profile_name', 'field_name', 'udf']

    option: option = option
    """
    option child of partially_catalytic_recombination_coefficient_o.
    """
    value: value = value
    """
    value child of partially_catalytic_recombination_coefficient_o.
    """
    profile_name: profile_name = profile_name
    """
    profile_name child of partially_catalytic_recombination_coefficient_o.
    """
    field_name: field_name = field_name
    """
    field_name child of partially_catalytic_recombination_coefficient_o.
    """
    udf: udf = udf
    """
    udf child of partially_catalytic_recombination_coefficient_o.
    """
