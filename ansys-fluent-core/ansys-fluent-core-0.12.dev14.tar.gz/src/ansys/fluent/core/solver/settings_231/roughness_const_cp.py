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
class roughness_const_cp(Group):
    """
    'roughness_const_cp' child.
    """

    fluent_name = "roughness-const-cp"

    child_names = \
        ['option', 'value', 'profile_name', 'field_name', 'udf']

    option: option = option
    """
    option child of roughness_const_cp.
    """
    value: value = value
    """
    value child of roughness_const_cp.
    """
    profile_name: profile_name = profile_name
    """
    profile_name child of roughness_const_cp.
    """
    field_name: field_name = field_name
    """
    field_name child of roughness_const_cp.
    """
    udf: udf = udf
    """
    udf child of roughness_const_cp.
    """
