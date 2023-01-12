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
class d_transmissivity(Group):
    """
    'd_transmissivity' child.
    """

    fluent_name = "d-transmissivity"

    child_names = \
        ['option', 'value', 'profile_name', 'field_name', 'udf']

    option: option = option
    """
    option child of d_transmissivity.
    """
    value: value = value
    """
    value child of d_transmissivity.
    """
    profile_name: profile_name = profile_name
    """
    profile_name child of d_transmissivity.
    """
    field_name: field_name = field_name
    """
    field_name child of d_transmissivity.
    """
    udf: udf = udf
    """
    udf child of d_transmissivity.
    """
