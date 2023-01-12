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
class mass_flux(Group):
    """
    'mass_flux' child.
    """

    fluent_name = "mass-flux"

    child_names = \
        ['option', 'value', 'profile_name', 'field_name', 'udf']

    option: option = option
    """
    option child of mass_flux.
    """
    value: value = value
    """
    value child of mass_flux.
    """
    profile_name: profile_name = profile_name
    """
    profile_name child of mass_flux.
    """
    field_name: field_name = field_name
    """
    field_name child of mass_flux.
    """
    udf: udf = udf
    """
    udf child of mass_flux.
    """
