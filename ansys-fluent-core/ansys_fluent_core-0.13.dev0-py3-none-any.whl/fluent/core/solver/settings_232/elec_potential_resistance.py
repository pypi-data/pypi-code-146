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
class elec_potential_resistance(Group):
    """
    'elec_potential_resistance' child.
    """

    fluent_name = "elec-potential-resistance"

    child_names = \
        ['option', 'value', 'profile_name', 'field_name', 'udf']

    option: option = option
    """
    option child of elec_potential_resistance.
    """
    value: value = value
    """
    value child of elec_potential_resistance.
    """
    profile_name: profile_name = profile_name
    """
    profile_name child of elec_potential_resistance.
    """
    field_name: field_name = field_name
    """
    field_name child of elec_potential_resistance.
    """
    udf: udf = udf
    """
    udf child of elec_potential_resistance.
    """
