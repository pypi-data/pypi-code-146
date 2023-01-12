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
class heat_transfer_coeff(Group):
    """
    'heat_transfer_coeff' child.
    """

    fluent_name = "heat-transfer-coeff"

    child_names = \
        ['option', 'value', 'profile_name', 'field_name', 'udf']

    option: option = option
    """
    option child of heat_transfer_coeff.
    """
    value: value = value
    """
    value child of heat_transfer_coeff.
    """
    profile_name: profile_name = profile_name
    """
    profile_name child of heat_transfer_coeff.
    """
    field_name: field_name = field_name
    """
    field_name child of heat_transfer_coeff.
    """
    udf: udf = udf
    """
    udf child of heat_transfer_coeff.
    """
