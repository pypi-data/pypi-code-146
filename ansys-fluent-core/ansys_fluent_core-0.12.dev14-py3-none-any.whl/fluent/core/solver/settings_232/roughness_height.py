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
class roughness_height(Group):
    """
    'roughness_height' child.
    """

    fluent_name = "roughness-height"

    child_names = \
        ['option', 'value', 'profile_name', 'field_name', 'udf']

    option: option = option
    """
    option child of roughness_height.
    """
    value: value = value
    """
    value child of roughness_height.
    """
    profile_name: profile_name = profile_name
    """
    profile_name child of roughness_height.
    """
    field_name: field_name = field_name
    """
    field_name child of roughness_height.
    """
    udf: udf = udf
    """
    udf child of roughness_height.
    """
