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
class ec_mass_flow(Group):
    """
    'ec_mass_flow' child.
    """

    fluent_name = "ec-mass-flow"

    child_names = \
        ['option', 'value', 'profile_name', 'field_name', 'udf']

    option: option = option
    """
    option child of ec_mass_flow.
    """
    value: value = value
    """
    value child of ec_mass_flow.
    """
    profile_name: profile_name = profile_name
    """
    profile_name child of ec_mass_flow.
    """
    field_name: field_name = field_name
    """
    field_name child of ec_mass_flow.
    """
    udf: udf = udf
    """
    udf child of ec_mass_flow.
    """
