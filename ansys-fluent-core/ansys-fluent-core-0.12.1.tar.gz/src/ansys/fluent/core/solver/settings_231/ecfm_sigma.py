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
class ecfm_sigma(Group):
    """
    'ecfm_sigma' child.
    """

    fluent_name = "ecfm-sigma"

    child_names = \
        ['option', 'value', 'profile_name', 'field_name', 'udf']

    option: option = option
    """
    option child of ecfm_sigma.
    """
    value: value = value
    """
    value child of ecfm_sigma.
    """
    profile_name: profile_name = profile_name
    """
    profile_name child of ecfm_sigma.
    """
    field_name: field_name = field_name
    """
    field_name child of ecfm_sigma.
    """
    udf: udf = udf
    """
    udf child of ecfm_sigma.
    """
